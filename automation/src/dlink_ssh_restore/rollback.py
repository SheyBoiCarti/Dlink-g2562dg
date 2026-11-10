"""Only the exact owned RAM tree can be removed."""

from .restore import RestoreError, RouterPort


def rollback(router: RouterPort, expected: str) -> str:
    if not router.reachable():
        raise RestoreError("offline")
    if router.identity() != expected:
        raise RestoreError("host_identity_changed_explicit_trust_required")
    try:
        router.connect()
        state = router.state()
        if state == "absent":
            return "absent"
        if state != "owned":
            raise RestoreError("conflict_unowned_resources")
        router.rollback()
        if router.state() != "absent":
            raise RestoreError("rollback_incomplete")
        return "removed"
    finally:
        router.close()
