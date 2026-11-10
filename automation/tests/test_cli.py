import pytest

from dlink_ssh_restore.cli import local_lock, retry
from dlink_ssh_restore.restore import RestoreError


def test_bounded_exponential_backoff():
    delays = []
    attempts = []

    def action():
        attempts.append(1)
        if len(attempts) < 4:
            raise RestoreError("offline")
        return "ok"

    assert retry(action, 4, 15, delays.append) == "ok"
    assert delays == [15, 30, 60]


def test_identity_failure_not_retried():
    calls = []

    def action():
        calls.append(1)
        raise RestoreError("host_identity_changed_explicit_trust_required")

    with pytest.raises(RestoreError):
        retry(action, 5, 15, lambda _: None)
    assert len(calls) == 1


def test_concurrent_execution_rejected():
    with local_lock():
        with pytest.raises(RestoreError, match="another_instance"):
            with local_lock():
                pass


def test_startup_ssh_transport_failure_retries_bounded():
    delays = []
    calls = []

    def action():
        calls.append(1)
        if len(calls) < 2:
            raise RestoreError("ssh_transport_unavailable")
        return "ok"

    assert retry(action, 3, 15, delays.append) == "ok"
    assert delays == [15]
