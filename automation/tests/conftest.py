import pytest

from dlink_ssh_restore.restore import Restore, RestoreError


class Router:
    def __init__(self):
        self.available = True
        self.owned = False
        self.listener = False
        self.boot = "a"
        self.cleanup = 0
        self.installs = 0
        self.fail = None

    def reachable(self):
        return self.available

    def identity(self):
        return "trusted"

    def connect(self):
        if self.fail == "credentials":
            raise RestoreError("credentials")

    def close(self):
        pass

    def snapshot(self):
        return self.boot

    def state(self):
        return "owned" if self.owned else ("conflict" if self.listener else "absent")

    def preflight(self):
        if self.fail == "ram":
            raise RestoreError("ram")

    def provision(self):
        self.owned = True
        self.installs += 1
        if self.fail == "reboot":
            self.boot = "b"
            raise RestoreError("restart")
        if self.fail == "partial":
            raise RestoreError("partial")
        self.listener = True

    def audit(self):
        if self.fail == "exposure":
            raise RestoreError("exposure")

    def rollback(self):
        self.owned = False
        self.listener = False
        self.cleanup += 1


class SSH:
    def __init__(self):
        self.fail = False
        self.uid = 0

    def verify(self):
        if self.fail:
            raise RestoreError("ssh_auth")
        if self.uid != 0:
            raise RestoreError("uid")
        return {"uid": 0, "interactive": True}


@pytest.fixture
def system():
    r, s = Router(), SSH()
    return r, s, Restore(r, s, "trusted")


def pytest_addoption(parser):
    parser.addoption(
        "--live-router",
        action="store_true",
        default=False,
        help="OWNER APPROVAL REQUIRED: modify the real router's RAM and clean up",
    )
    parser.addoption(
        "--router-config",
        default=None,
        help="Configured local TOML for approved live test",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: explicitly authorized real-router RAM integration; skipped by default",
    )
