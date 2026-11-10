"""State orchestration; transports are injected for offline verification."""

from typing import Any, Protocol


class RestoreError(RuntimeError):
    """A safe public error code; never include remote output or secrets."""


class RouterPort(Protocol):
    def reachable(self) -> bool: ...
    def identity(self) -> str: ...
    def connect(self) -> None: ...
    def close(self) -> None: ...
    def snapshot(self) -> str: ...
    def state(self) -> str: ...
    def preflight(self) -> None: ...
    def provision(self) -> None: ...
    def audit(self) -> None: ...
    def rollback(self) -> None: ...


class SSHPort(Protocol):
    def verify(self) -> dict[str, Any]: ...


class Restore:
    def __init__(self, router: RouterPort, ssh: SSHPort, expected: str):
        self.router, self.ssh, self.expected = router, ssh, expected

    def run(self) -> dict[str, Any]:
        r = self.router
        if not r.reachable():
            raise RestoreError("offline")
        if r.identity() != self.expected:
            raise RestoreError("host_identity_changed_explicit_trust_required")
        boot = None
        created = False
        managed = False
        try:
            r.connect()
            boot = r.snapshot()
            state = r.state()
            if state == "conflict":
                raise RestoreError("conflict_unowned_resources")
            if state == "owned":
                managed = True
                try:
                    r.audit()
                except RestoreError as exc:
                    if str(exc) != "owned_listener_missing":
                        raise
                    r.rollback()
                    state = "absent"
            if state == "absent":
                r.preflight()
                created = True
                managed = True
                r.provision()
            elif state != "owned":
                raise RestoreError("unknown_state")
            r.audit()
            result = self.ssh.verify()
            if result.get("uid") != 0 or result.get("interactive") is not True:
                raise RestoreError("ssh_verification_failed")
            if r.snapshot() != boot:
                raise RestoreError("router_restart")
            if r.identity() != self.expected:
                raise RestoreError("host_identity_changed_explicit_trust_required")
            return {**result, "state": "restored" if created else "already_ready"}
        except Exception:
            if managed:
                try:
                    # Never send cleanup into a different boot or changed identity.
                    if (
                        r.snapshot() == boot
                        and r.identity() == self.expected
                        and r.state() == "owned"
                    ):
                        r.rollback()
                except RestoreError as cleanup_error:
                    if str(cleanup_error) in (
                        "telnet_disconnected_possible_restart",
                        "telnet_timeout",
                        "telnet_command_transport_failed",
                        "offline_or_trusted_lan_unavailable",
                        "ssh_transport_unavailable",
                    ):
                        raise RestoreError("connection_lost_cleanup_pending") from None
                    raise RestoreError(
                        "failed_cleanup_unconfirmed_run_status_then_rollback"
                    ) from None
                except Exception:
                    raise RestoreError(
                        "failed_cleanup_unconfirmed_run_status_then_rollback"
                    ) from None
            raise
        finally:
            r.close()
