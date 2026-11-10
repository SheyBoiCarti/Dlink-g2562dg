"""Pinned SSH handshake and key-only UID/interactive verification."""

import base64
import hashlib
import socket
import time
import uuid
from pathlib import Path
from typing import Any

from .config import Config
from .restore import RestoreError


def fingerprint(key: Any) -> str:
    return "SHA256:" + base64.b64encode(
        hashlib.sha256(key.asbytes()).digest()
    ).decode().rstrip("=")


def trusted_socket(config: Config, port: int) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(config.timeout)
    try:
        s.bind((config.local_address, 0))
        s.connect((config.host, port))
        if s.getsockname()[0] != config.local_address:
            raise RestoreError("untrusted_source_address")
        return s
    except Exception:
        s.close()
        raise RestoreError("offline_or_trusted_lan_unavailable") from None


def handshake(config: Config, port: int, expected: str | None) -> Any:
    import paramiko

    sock = trusted_socket(config, port)
    transport = paramiko.Transport(sock)
    transport.banner_timeout = config.timeout
    transport.auth_timeout = config.timeout
    try:
        # Exact Phase 6 negotiated algorithms, scoped to this fixed device only.
        options = transport.get_security_options()
        options.kex = ("diffie-hellman-group14-sha1",)
        options.key_types = ("ssh-rsa",)
        options.ciphers = ("aes128-ctr",)
        options.digests = ("hmac-sha1",)
        transport.disabled_algorithms = {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]}
        transport.start_client(timeout=config.timeout)
        if not transport.is_active() or transport.get_remote_server_key() is None:
            raise RestoreError("ssh_transport_unavailable")
        if (
            expected is not None
            and fingerprint(transport.get_remote_server_key()) != expected
        ):
            raise RestoreError("host_identity_changed_explicit_trust_required")
        return transport
    except RestoreError:
        transport.close()
        raise
    except paramiko.ssh_exception.IncompatiblePeer:
        transport.close()
        raise RestoreError("ssh_algorithm_incompatible") from None
    except (EOFError, OSError, paramiko.SSHException):
        transport.close()
        raise RestoreError("ssh_transport_unavailable") from None
    except Exception:
        transport.close()
        raise RestoreError("ssh_handshake_failed") from None


def host_identity(config: Config, port: int = 22) -> str:
    transport = handshake(config, port, None)
    try:
        return fingerprint(transport.get_remote_server_key())
    finally:
        transport.close()


def load_private(config: Config, passphrase: str) -> Any:
    import paramiko

    try:
        # A passphrase is mandatory for unattended use; reject unencrypted keys.
        try:
            paramiko.RSAKey.from_private_key_file(config.private_key)
        except paramiko.PasswordRequiredException:
            pass
        else:
            raise RestoreError("private_key_must_be_passphrase_protected")
        key = paramiko.RSAKey.from_private_key_file(
            config.private_key, password=passphrase
        )
        if key.get_bits() < 3072:
            raise RestoreError("rsa_key_requires_3072_bits")
        return key
    except RestoreError:
        raise
    except Exception:
        raise RestoreError("private_key_load_failed") from None


def verify_public_key(public: str, private: Any) -> str:
    fields = public.strip().split()
    try:
        valid = (
            len(fields) >= 2
            and fields[0] == "ssh-rsa"
            and base64.b64decode(fields[1], validate=True) == private.asbytes()
        )
    except ValueError:
        valid = False
    if (
        not valid
        or private.get_bits() < 3072
        or "\n" in public.strip()
        or "\r" in public.strip()
    ):
        raise RestoreError("invalid_or_mismatched_rsa_public_key")
    # Strip comment; exactly one public line reaches the shell asset.
    return "ssh-rsa " + fields[1] + "\n"


class SSH:
    def __init__(self, config: Config, credentials: Any):
        self.config, self.credentials = config, credentials

    def public_key(self) -> str:
        key = load_private(self.config, self.credentials.get("key-passphrase"))
        try:
            public = Path(self.config.public_key).read_text(encoding="ascii")
        except Exception:
            raise RestoreError("public_key_read_failed") from None
        return verify_public_key(public, key)

    def verify(self) -> dict[str, Any]:
        import paramiko

        c = self.config
        transport = handshake(c, 2222, c.host_fingerprint)
        try:
            key = load_private(c, self.credentials.get("key-passphrase"))
            # Old Dropbear only supports ssh-rsa user signatures. Scope to this transport.
            options = transport.get_security_options()
            options.key_types = ("ssh-rsa",)
            transport.disabled_algorithms = {
                "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]
            }
            transport.auth_publickey("admin", key)
            if not transport.is_authenticated():
                raise RestoreError("ssh_auth_failed")
            channel = transport.open_session(timeout=c.timeout)
            try:
                channel.settimeout(c.timeout)
                channel.exec_command("id -u; id")
                output = self._receive(channel, exit_required=True)
                lines = output.replace("\r", "").splitlines()
                if (
                    not lines
                    or lines[0] != "0"
                    or not any("uid=0(admin)" in line for line in lines[1:])
                ):
                    raise RestoreError("ssh_uid_not_zero")
            finally:
                channel.close()
            channel = transport.open_session(timeout=c.timeout)
            try:
                channel.settimeout(c.timeout)
                channel.get_pty(term="xterm", width=80, height=24)
                channel.invoke_shell()
                token = uuid.uuid4().hex
                # Keep channel stdin open, matching the successful Phase 6B technique.
                channel.sendall(
                    "printf '\\nBEGIN"
                    + token
                    + "\\n'; id -u; test -t 0 && test -t 1; printf 'TTY"
                    + token
                    + ':%s\\n\' "$?"\n'
                )
                out = self._receive(channel, until="TTY" + token + ":0\n")
                if (
                    "\nBEGIN" + token + "\n0\n" not in out
                    or "\nTTY" + token + ":0\n" not in out
                ):
                    raise RestoreError("interactive_uid_or_tty_failed")
                channel.sendall("printf '\\nSECOND" + token + "\\n'\n")
                self._receive(channel, until="\nSECOND" + token + "\n")
                channel.sendall("exit\n")
            finally:
                channel.close()
            return {"uid": 0, "interactive": True}
        except RestoreError:
            raise
        except paramiko.AuthenticationException:
            raise RestoreError("ssh_auth_failed") from None
        except (EOFError, OSError):
            raise RestoreError("ssh_transport_unavailable") from None
        except paramiko.SSHException:
            if not transport.is_active():
                raise RestoreError("ssh_transport_unavailable") from None
            raise RestoreError("ssh_interactive_verification_failed") from None
        except Exception:
            raise RestoreError("ssh_auth_or_interactive_verification_failed") from None
        finally:
            transport.close()

    def _receive(
        self, channel: Any, until: str | None = None, exit_required: bool = False
    ) -> str:
        end = time.monotonic() + self.config.timeout
        data = bytearray()
        while time.monotonic() < end:
            if channel.recv_ready():
                chunk = channel.recv(4096)
                if not chunk:
                    break
                data.extend(chunk)
                if len(data) > 65536:
                    raise RestoreError("ssh_output_limit")
                text = data.decode("utf-8", "replace").replace("\r", "")
                if until and until in text:
                    return text
            elif channel.exit_status_ready():
                if exit_required and channel.recv_exit_status() == 0:
                    return data.decode("utf-8", "replace")
                break
            else:
                time.sleep(0.02)
        if not channel.get_transport().is_active():
            raise RestoreError("ssh_transport_unavailable")
        raise RestoreError("ssh_proof_timeout_or_failure")
