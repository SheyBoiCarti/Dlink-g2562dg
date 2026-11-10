import subprocess

from dlink_ssh_restore.config import Config
from dlink_ssh_restore.router import Router


def test_command_wrapper_executes_without_quoting_status():
    r = Router(Config(), None, "")
    commands = []
    r._send = commands.append

    def read(*args):
        return subprocess.run(
            ["C:/Program Files/Git/bin/bash.exe", "-c", commands[-1]],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout

    r._read = read
    assert r.command("printf hello") == "hello"


def test_shell_wrapper_is_one_physical_line():
    r = Router(Config(), None, "")
    sent = []
    r._send = sent.append

    def fail(*args):
        raise RuntimeError("mock disconnected")

    r._read = fail
    try:
        r.command("printf hello")
    except Exception:
        pass
    assert "\n" not in sent[0] and "\x00" not in sent[0]


def test_all_provision_commands_parse_without_executing_router_actions():
    import base64
    from pathlib import Path

    from dlink_ssh_restore.router import asset

    r = Router(
        Config(owner="a" * 32),
        None,
        "ssh-rsa " + base64.b64encode(b"public-test-data").decode() + "\n",
    )
    r.boot = "boot"
    r.snapshot = lambda: "boot"
    owned = [False]
    commands = []
    r.state = lambda: "owned" if owned[0] else "absent"

    def command(text, **kwargs):
        commands.append(text)
        if text.startswith("umask 077; mkdir"):
            owned[0] = True
        if text.startswith("sh /tmp/dlink-phase6a/phase6a_rollback.sh"):
            owned[0] = False
        return ""

    r.command = command
    r.provision()
    r.rollback()
    for text in commands:
        assert "\x00" not in text and "\n" not in text
        result = subprocess.run(
            ["C:/Program Files/Git/bin/bash.exe", "-n", "-c", text],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, result.stderr
    project = Path(__file__).resolve().parents[2]
    for name in ["phase6a_setup.sh", "phase6a_rollback.sh"]:
        assert asset(name) == (project / "scripts" / name).read_bytes()


def test_failure_reports_stage_without_remote_output():
    import pytest

    from dlink_ssh_restore.restore import RestoreError

    r = Router(Config(), None, "")
    commands = []
    r._send = commands.append
    r._read = lambda *args: (
        subprocess.run(
            ["C:/Program Files/Git/bin/bash.exe", "-c", commands[-1]],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout
    )
    with pytest.raises(RestoreError, match="preflight_ram_check_failed"):
        r.command("printf SECRET; false", failure="preflight_ram_check_failed")


def test_overlong_telnet_command_rejected_before_send():
    import pytest

    from dlink_ssh_restore.restore import RestoreError

    r = Router(Config(), None, "")
    sent = []
    r._send = sent.append
    with pytest.raises(RestoreError, match="telnet_command_too_long"):
        r.command("x" * 1500)
    assert not sent
