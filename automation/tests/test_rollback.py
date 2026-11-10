import pytest

from dlink_ssh_restore.restore import RestoreError
from dlink_ssh_restore.rollback import rollback


def test_owned_rollback(system):
    r, s, x = system
    x.run()
    assert rollback(r, "trusted") == "removed"
    assert not r.listener


def test_absent_rollback(system):
    r, s, x = system
    assert rollback(r, "trusted") == "absent"
    assert r.cleanup == 0


def test_unowned_rollback_refused(system):
    r, s, x = system
    r.listener = True
    with pytest.raises(RestoreError, match="conflict"):
        rollback(r, "trusted")
    assert r.cleanup == 0


def test_rollback_repairs_incomplete_copy_in_bounded_chunks():
    import base64
    import re
    import shlex

    from dlink_ssh_restore.config import Config
    from dlink_ssh_restore.router import P, Router, asset

    canonical = asset("phase6a_rollback.sh")
    remote = {P + "/phase6a_rollback.sh": b"incomplete"}
    owned = [True]
    commands = []
    r = Router(Config(owner="a" * 32), None, "")
    r.snapshot = lambda: "boot"
    r.state = lambda: "owned" if owned[0] else "absent"

    def command(text, **kwargs):
        commands.append(text)
        if text.startswith("test ! -e "):
            return ""
        if "md5sum " in text:
            path = re.search(r"md5sum ([^ ]+)", text)[1]
            if remote.get(path) != canonical:
                raise RestoreError("remote_command_failed")
            return ""
        if text.startswith("printf '%s' "):
            parts = shlex.split(text)
            assert parts[-2] == ">>"
            remote[parts[-1]] = remote.get(parts[-1], b"") + base64.b64decode(parts[2])
            return ""
        if text.startswith("sh "):
            assert remote[text[3:]] == canonical
            owned[0] = False
            return ""
        raise AssertionError("Unexpected test transport command")

    r.command = command
    r.rollback()
    assert not owned[0]
    assert remote[P + "/phase6a_rollback.sh"] == b"incomplete"
    assert any(value == canonical for value in remote.values())
    assert all(len(text.encode()) < 850 for text in commands)


def test_valid_staged_rollback_uses_short_verified_path():
    from dlink_ssh_restore.config import Config
    from dlink_ssh_restore.router import P, Router

    r = Router(Config(owner="a" * 32), None, "")
    r.snapshot = lambda: "boot"
    owned = [True]
    commands = []
    r.state = lambda: "owned" if owned[0] else "absent"

    def command(text, **kwargs):
        commands.append(text)
        if text == "sh " + P + "/phase6a_rollback.sh":
            owned[0] = False
        return ""

    r.command = command
    r.rollback()
    assert not owned[0]
    assert "md5sum" in commands[0]
    assert commands[-1] == "sh " + P + "/phase6a_rollback.sh"
    assert not any("base64" in text for text in commands)


def test_rollback_transport_failure_does_not_start_repair_upload():
    from dlink_ssh_restore.config import Config
    from dlink_ssh_restore.router import Router

    r = Router(Config(owner="a" * 32), None, "")
    r.snapshot = lambda: "boot"
    r.state = lambda: "owned"

    def failed_verification(*args):
        raise RestoreError("telnet_disconnected_possible_restart")

    def forbidden_upload(*args):
        raise AssertionError("Repair attempted after lost transport")

    r._check_asset = failed_verification
    r._upload = forbidden_upload
    with pytest.raises(RestoreError, match="telnet_disconnected_possible_restart"):
        r.rollback()
