"""Real router integration is opt-in and was NOT run in Phase 8."""

from pathlib import Path

import pytest

from dlink_ssh_restore.cli import execute, local_lock
from dlink_ssh_restore.config import Config


@pytest.mark.live
def test_approved_router_round_trip(request):
    if not request.config.getoption("--live-router"):
        pytest.skip("Real router changes require explicit owner authorization")
    config_path = request.config.getoption("--router-config")
    if not config_path:
        pytest.fail("--router-config is required for an explicitly approved live test")
    c = Config.load(Path(config_path))
    with local_lock():
        assert execute(c, "status")["state"] == "absent", (
            "Refuse to disturb any existing deployment"
        )
        try:
            result = execute(c, "restore")
            assert result == {"uid": 0, "interactive": True, "state": "restored"}
            assert execute(c, "restore")["state"] == "already_ready"
        finally:
            # The normal rollback refuses unknown owners, changed identities and unsafe mounts.
            execute(c, "rollback")
        assert execute(c, "status")["state"] == "absent"
