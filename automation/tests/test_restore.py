import pytest

from dlink_ssh_restore.restore import RestoreError


def test_success_requires_uid_and_interactive(system):
    r, s, x = system
    assert x.run() == {"uid": 0, "interactive": True, "state": "restored"}
    assert r.listener


def test_offline(system):
    r, s, x = system
    r.available = False
    with pytest.raises(RestoreError, match="offline"):
        x.run()
    assert r.installs == 0


def test_bad_credentials(system):
    r, s, x = system
    r.fail = "credentials"
    with pytest.raises(RestoreError, match="credentials"):
        x.run()
    assert r.installs == 0


def test_host_mismatch_before_login(system):
    r, s, x = system
    x.expected = "different"
    r.fail = "credentials"
    with pytest.raises(RestoreError, match="host_identity"):
        x.run()
    assert r.installs == 0


def test_duplicate_execution(system):
    r, s, x = system
    x.run()
    assert x.run()["state"] == "already_ready"
    assert r.installs == 1


def test_conflicting_listener_untouched(system):
    r, s, x = system
    r.listener = True
    with pytest.raises(RestoreError, match="conflict"):
        x.run()
    assert r.cleanup == 0


def test_ssh_auth_failure_rolls_back(system):
    r, s, x = system
    s.fail = True
    with pytest.raises(RestoreError, match="ssh_auth"):
        x.run()
    assert not r.listener and r.cleanup == 1


def test_nonroot_never_success(system):
    r, s, x = system
    s.uid = 1
    with pytest.raises(RestoreError, match="uid"):
        x.run()
    assert not r.listener


def test_existing_owned_exposure_failure_removes_only_owned_listener(system):
    r, s, x = system
    x.run()
    r.fail = "exposure"
    with pytest.raises(RestoreError, match="exposure"):
        x.run()
    assert not r.listener and r.cleanup == 1


def test_owned_listener_killed_by_vendor_is_recreated(system):
    r, s, x = system
    x.run()
    r.listener = False
    original = r.audit

    def audit():
        if not r.listener:
            raise RestoreError("owned_listener_missing")
        original()

    r.audit = audit
    assert x.run()["state"] == "restored"
    assert r.installs == 2 and r.listener
