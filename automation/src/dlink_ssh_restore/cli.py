"""Explicit CLI entry points. Setup is local only; watch is opt-in."""

import argparse
import json
import logging
import os
import socket
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict
from getpass import getpass
from pathlib import Path
from typing import Any, Callable, Iterator

from .config import Config
from .credentials import Credentials
from .restore import Restore, RestoreError
from .rollback import rollback
from .router import Router
from .ssh import SSH, load_private, verify_public_key

LOG = logging.getLogger("dlink_restore")
TRANSIENT = (
    "offline",
    "offline_or_trusted_lan_unavailable",
    "telnet_disconnected_possible_restart",
    "router_restart",
    "telnet_timeout",
    "telnet_command_transport_failed",
    "ssh_transport_unavailable",
    "connection_lost_cleanup_pending",
)


@contextmanager
def local_lock() -> Iterator[None]:
    # Cross-process/user lock without stale lock files. OS releases it on crash.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            sock.bind(("127.0.0.1", 39482))
            sock.listen(1)
        except OSError:
            raise RestoreError("another_instance_running") from None
        yield
    finally:
        sock.close()


def retry(
    action: Callable[[], Any],
    attempts: int,
    base: int,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    for i in range(attempts):
        try:
            return action()
        except RestoreError as exc:
            if str(exc) not in TRANSIENT or i == attempts - 1:
                raise
            sleep(min(base * 2**i, 300))
    raise RestoreError("retry_exhausted")


def event(code: str, **fields: Any) -> None:
    # Only application-owned codes/fields; never exceptions, commands or remote transcripts.
    LOG.info(json.dumps({"event": code, **fields}, sort_keys=True))


def default_config() -> Path:
    return (
        Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
        / "DLinkSSHRestore"
        / "config.toml"
    )


def write_config(path: Path, config: Config) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        "\n".join(
            k + " = " + (json.dumps(v) if isinstance(v, str) else str(v))
            for k, v in asdict(config).items()
        )
        + "\n"
    )
    temporary = path.with_suffix(".toml.new")
    try:
        with temporary.open("x", encoding="utf-8") as f:
            f.write(body)
        os.replace(temporary, path)
    except Exception:
        raise RestoreError("config_write_failed_check_new_file") from None


def setup(path: Path, update_trust: bool = False) -> None:
    if update_trust:
        c = Config.load(path)
        print(
            "Verify the router's public host fingerprint through your trusted recovery procedure first."
        )
        fp = input("Independently verified SHA256 fingerprint: ").strip()
        if (
            input("Type TRUST followed by a space and that full fingerprint: ").strip()
            != "TRUST " + fp
        ):
            raise RestoreError("trust_update_cancelled")
        values = asdict(c)
        values["host_fingerprint"] = fp
        write_config(path, Config(**values))
        event("trust_updated_explicitly")
        return
    if path.exists():
        raise RestoreError("config_exists_use_setup_update_trust")
    print("Local setup only. No connection or scheduled task will be created.")
    local = input("Windows Ethernet IPv4 address on 10.0.0.0/24: ").strip()
    private = (
        Path(input("Existing passphrase-protected RSA private key path: ").strip())
        .expanduser()
        .resolve(strict=True)
    )
    public = (
        Path(input("Matching RSA public key path: ").strip())
        .expanduser()
        .resolve(strict=True)
    )
    if any("onedrive" in x.lower() for x in private.parts):
        raise RestoreError("private_key_must_be_outside_onedrive")
    fp = input("Independently verified router SHA256 host fingerprint: ").strip()
    if (
        input("Type TRUST followed by a space and that full fingerprint: ").strip()
        != "TRUST " + fp
    ):
        raise RestoreError("trust_setup_cancelled")
    c = Config(
        local_address=local,
        owner=uuid.uuid4().hex,
        host_fingerprint=fp,
        private_key=str(private),
        public_key=str(public),
    )
    passphrase = getpass(
        "SSH private-key passphrase (stored in Windows Credential Manager): "
    )
    if not passphrase:
        raise RestoreError("passphrase_required")
    key = load_private(c, passphrase)
    verify_public_key(public.read_text(encoding="ascii"), key)
    password = getpass(
        "Existing Telnet management password (stored in Windows Credential Manager): "
    )
    if not password or any(v in password for v in ("\r", "\n", "\x00")):
        raise RestoreError("invalid_telnet_credential")
    vault = Credentials(c.owner)
    vault.set("key-passphrase", passphrase)
    vault.set("telnet-password", password)
    write_config(path, c)
    event("local_setup_complete", config=str(path))


def execute(c: Config, command: str) -> dict[str, Any]:
    vault = Credentials(c.owner)
    ssh = SSH(c, vault)
    # Validate public/private pairing before any provisioning or Telnet credentials.
    public = ssh.public_key() if command == "restore" else ""
    router = Router(c, vault, public)
    if command == "restore":
        return Restore(router, ssh, c.host_fingerprint).run()
    if command == "rollback":
        return {"state": rollback(router, c.host_fingerprint)}
    if not router.reachable():
        raise RestoreError("offline")
    if router.identity() != c.host_fingerprint:
        raise RestoreError("host_identity_changed_explicit_trust_required")
    try:
        router.connect()
        state = router.state()
        if state == "owned":
            router.audit()
            proof = ssh.verify()
            return {"state": "ready", **proof}
        return {"state": state}
    finally:
        router.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fixed DSL-G2562DG RAM SSH restoration; live commands require owner authorization."
    )
    parser.add_argument("--config", type=Path, default=default_config())
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("setup", help="local interactive credentials/configuration only")
    s.add_argument(
        "--update-trust",
        action="store_true",
        help="explicitly replace trust after independent verification",
    )
    for name in ("restore", "status", "rollback", "watch"):
        sub.add_parser(name)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Paramiko diagnostics are intentionally suppressed: no raw handshake/auth logs.
    logging.getLogger("paramiko").setLevel(logging.CRITICAL)
    try:
        with local_lock():
            if args.command == "setup":
                setup(args.config, args.update_trust)
                return 0
            c = Config.load(args.config)
            if args.command == "watch":
                while True:
                    try:
                        result = retry(
                            lambda: execute(c, "restore"), c.attempts, c.backoff_seconds
                        )
                        event("restore_verified", **result)
                    except RestoreError as exc:
                        event("restore_failed", reason=str(exc))
                        # Trust/auth/policy/conflict/cleanup errors require a person, not retry loops.
                        if str(exc) not in TRANSIENT:
                            return 1
                    time.sleep(c.monitor_seconds)
            result = retry(
                lambda: execute(c, args.command), c.attempts, c.backoff_seconds
            )
            event(args.command, **result)
            return 0 if result.get("state") != "conflict" else 1
    except KeyboardInterrupt:
        event("stopped_no_implicit_router_cleanup")
        return 130
    except RestoreError as exc:
        event("failed", reason=str(exc))
        return 1
    except (ValueError, TypeError, OSError):
        event("failed", reason="configuration_or_local_file_error")
        return 2
    except Exception:
        event("failed", reason="unexpected_error_details_suppressed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
