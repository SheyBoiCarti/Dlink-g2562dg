import pytest

from dlink_ssh_restore.restore import RestoreError


def test_partial_failure_cleanup(system):
    r, s, x = system
    r.fail = "partial"
    with pytest.raises(RestoreError, match="partial"):
        x.run()
    assert not r.owned and r.cleanup == 1


def test_restart_never_cleans_new_boot(system):
    r, s, x = system
    r.fail = "reboot"
    with pytest.raises(RestoreError, match="restart"):
        x.run()
    assert r.cleanup == 0


def test_disconnect_during_setup_is_retryable_without_blind_cleanup(system):
    r, s, x = system

    def provision():
        r.owned = True
        raise RestoreError("telnet_disconnected_possible_restart")

    r.provision = provision

    def snapshot():
        if r.owned:
            raise RestoreError("telnet_disconnected_possible_restart")
        return "a"

    r.snapshot = snapshot
    with pytest.raises(RestoreError, match="connection_lost_cleanup_pending"):
        x.run()
    assert r.cleanup == 0
