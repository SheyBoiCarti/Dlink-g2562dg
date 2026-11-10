"""Bounded Telnet transport and fixed RAM provisioning. No raw transcript logging."""

import base64
import hashlib
import re
import socket
import time
import uuid
from importlib.resources import files
from typing import Any

from .config import Config
from .restore import RestoreError
from .security import check_exposure, check_mounts
from .ssh import host_identity, trusted_socket

P = "/tmp/dlink-phase6a"
R = P + "/root"
ASSETS = ("phase6a_setup.sh", "phase6a_rollback.sh")


def asset(name: str) -> bytes:
    if name not in ASSETS:
        raise RestoreError("invalid_asset")
    return files("dlink_ssh_restore").joinpath("assets", name).read_bytes()


class TelnetCodec:
    """Incremental RFC 854 framing; refuse options and discard subnegotiation."""

    def __init__(self) -> None:
        self.state = "data"
        self.op = 0

    def feed(self, data: bytes) -> tuple[bytes, bytes]:
        output = bytearray()
        reply = bytearray()
        for b in data:
            if self.state == "data":
                if b == 255:
                    self.state = "iac"
                elif b != 0:
                    output.append(b)
            elif self.state == "iac":
                if b == 255:
                    output.append(b)
                    self.state = "data"
                elif b in (251, 252, 253, 254):
                    self.op = b
                    self.state = "option"
                elif b == 250:
                    self.state = "sub"
                else:
                    self.state = "data"
            elif self.state == "option":
                if self.op == 251:
                    reply.extend((255, 254, b))
                elif self.op == 253:
                    reply.extend((255, 252, b))
                self.state = "data"
            elif self.state == "sub":
                if b == 255:
                    self.state = "sub_iac"
            elif self.state == "sub_iac":
                self.state = "data" if b == 240 else "sub"
        return bytes(output), bytes(reply)


def parse_result(raw: str, token: str) -> str:
    lines = raw.replace("\r", "").splitlines()
    try:
        start = lines.index("START" + token)
        end = next(
            i
            for i in range(start + 1, len(lines))
            if re.fullmatch("END" + token + r":\d+", lines[i])
        )
        if lines[end] != "END" + token + ":0":
            raise RestoreError("remote_command_failed")
        return "\n".join(lines[start + 1 : end]).strip()
    except (ValueError, StopIteration):
        raise RestoreError("remote_framing_failed") from None


class Router:
    def __init__(self, config: Config, credentials: Any, public_key: str):
        self.config, self.credentials, self.public_key = config, credentials, public_key
        self.sock: socket.socket | None = None
        self.codec = TelnetCodec()
        self.boot: str | None = None

    def reachable(self) -> bool:
        try:
            s = trusted_socket(self.config, 22)
            s.close()
            return True
        except RestoreError:
            return False

    def identity(self) -> str:
        return host_identity(self.config)

    def _send(self, text: str) -> None:
        if self.sock is None:
            raise RestoreError("telnet_not_connected")
        try:
            self.sock.sendall(
                text.encode("utf-8").replace(b"\xff", b"\xff\xff") + b"\r\n"
            )
        except OSError:
            raise RestoreError("telnet_disconnected_possible_restart") from None

    def _read(self, needle: bytes, timeout: int | None = None) -> str:
        if self.sock is None:
            raise RestoreError("telnet_not_connected")
        end = time.monotonic() + (timeout or self.config.timeout)
        data = bytearray()
        while time.monotonic() < end:
            self.sock.settimeout(max(0.1, end - time.monotonic()))
            try:
                chunk = self.sock.recv(8192)
            except TimeoutError:
                raise RestoreError("telnet_timeout") from None
            except OSError:
                raise RestoreError("telnet_disconnected_possible_restart") from None
            if not chunk:
                raise RestoreError("telnet_disconnected_possible_restart")
            plain, reply = self.codec.feed(chunk)
            if reply:
                self.sock.sendall(reply)
            data.extend(plain)
            if len(data) > 262144:
                raise RestoreError("telnet_output_limit")
            normalized = data.replace(b"\r", b"")
            if b"login info is not correct" in normalized:
                raise RestoreError("telnet_credentials_rejected")
            found = (
                (re.search(re.escape(needle) + rb"[0-9]+\n", normalized) is not None)
                if needle.endswith(b":")
                else needle in normalized
            )
            if found:
                return data.decode("utf-8", "replace").replace("\r", "")
        raise RestoreError("telnet_timeout")

    def connect(self) -> None:
        # Independently pin SSH again immediately before transmitting Telnet secrets.
        if self.identity() != self.config.host_fingerprint:
            raise RestoreError("host_identity_changed_explicit_trust_required")
        try:
            self.sock = trusted_socket(self.config, 23)
            self._read(b"LOGIN#")
            self._send(self.config.telnet_user)
            self._read(b"PASS#")
            password = self.credentials.get("telnet-password")
            if not password or any(x in password for x in ("\r", "\n", "\x00")):
                raise RestoreError("invalid_telnet_credential")
            self._send(password)
            self._read(b"AMS#")
            self._send("sh")
            self._read(b"#")
            self._send("unset HISTFILE; HISTSIZE=0")
            self._read(b"#")
            if self.command("id -u") != "0":
                raise RestoreError("telnet_uid_not_zero")
        except RestoreError:
            self.close()
            raise
        except OSError:
            self.close()
            raise RestoreError("telnet_disconnected_possible_restart") from None
        except Exception:
            self.close()
            raise RestoreError("telnet_auth_or_transport_failed") from None

    def command(
        self,
        command: str,
        timeout: int | None = None,
        failure: str = "remote_command_failed",
    ) -> str:
        if any(v in command for v in ("\n", "\r", "\x00")):
            raise RestoreError("invalid_command_line")
        token = uuid.uuid4().hex
        wire = (
            "printf '\\nSTART"
            + token
            + "\\n'; ( "
            + command
            + " ); x=$?; printf '\\nEND"
            + token
            + ':%s\\n\' "$x"'
        )
        if len(wire.encode("utf-8")) + 2 > 1000:
            raise RestoreError("telnet_command_too_long")
        self._send(wire)
        try:
            raw = self._read(("\nEND" + token + ":").encode(), timeout)
            return parse_result(raw, token)
        except RestoreError as exc:
            if str(exc) == "remote_command_failed":
                raise RestoreError(failure) from None
            raise
        except Exception:
            raise RestoreError("telnet_command_transport_failed") from None

    def snapshot(self) -> str:
        value = self.command("cat /proc/sys/kernel/random/boot_id")
        if not re.fullmatch(r"[a-f0-9-]{36}", value):
            raise RestoreError("boot_id_unavailable")
        return value

    def _same_boot(self) -> None:
        if self.boot is not None and self.snapshot() != self.boot:
            raise RestoreError("router_restart")

    def state(self) -> str:
        owner = self.config.owner
        cmd = (
            f"if [ -e {P} ] || [ -L {P} ]; then "
            f"if [ -d {P} ] && [ ! -L {P} ] && [ ! -L {P}/.phase8-owner ] && "
            f'[ "$(cat {P}/.phase8-owner 2>/dev/null)" = {owner} ]; then echo owned; else echo conflict; fi; '
            "elif netstat -lnt | awk '$4 ~ /:2222$/ {f=1} END {exit !f}'; then echo conflict; "
            rf"elif awk '$5 ~ /^\/tmp\/dlink-phase6a(\/|$)/ {{f=1}} END {{exit !f}}' /proc/self/mountinfo; then echo conflict; else echo absent; fi"
        )
        value = self.command(cmd)
        if value not in ("owned", "absent", "conflict"):
            raise RestoreError("invalid_remote_state")
        return value

    def preflight(self) -> None:
        self.boot = self.snapshot()
        c = self.config
        self.command(
            'test "$(id -u)" = 0 && test "$(uname -srm)" = \'Linux 3.14.18 armv7l\' && test "$(cfgcmd get InternetGatewayDevice.DeviceInfo.SoftwareVersion)" = TK_1.00TK_V1.2.12ak_20221018',
            failure="preflight_firmware_or_uid_mismatch",
        )
        self.command(
            'awk \'$2=="/tmp" && $3=="tmpfs" {ok=1} END {exit !ok}\' /proc/mounts && awk \'$2=="/" && $3=="jffs2" && $4 ~ /(^|,)ro(,|$)/ {ok=1} END {exit !ok}\' /proc/mounts'
        )
        self.command(
            f"awk '/^MemAvailable:/ {{m=$2}} END {{exit !(m>={c.min_ram_kib})}}' /proc/meminfo && test ! -e /etc/dropbear && test -r /var/dropbear/rsa_host_key",
            failure="preflight_ram_or_key_baseline_failed",
        )
        check_mounts(self.command("cat /proc/self/mountinfo"))
        # Validate existing policy BEFORE creating a listener; no firewall mutations.
        check_exposure(
            "tcp 0 0 10.0.0.2:2222 0.0.0.0:* LISTEN",
            self.command("iptables -S"),
            self.command("ip6tables -S"),
        )

    def _owned(self) -> None:
        self._same_boot()
        if self.state() != "owned":
            raise RestoreError("conflict_unowned_resources")

    def _asset_path(self, name: str, remote_name: str | None = None) -> str:
        if name not in ASSETS:
            raise RestoreError("invalid_asset")
        if remote_name is not None and not re.fullmatch(
            r"phase8-rollback-[a-f0-9]{32}\.sh", remote_name
        ):
            raise RestoreError("invalid_remote_asset_name")
        return P + "/" + (remote_name or name)

    def _upload(self, name: str, remote_name: str | None = None) -> None:
        self._owned()
        path = self._asset_path(name, remote_name)
        self.command(f"test ! -e {path} && test ! -L {path}")
        data = asset(name)
        if b"\r" in data:
            raise RestoreError("script_asset_requires_lf")
        for i in range(0, len(data), 384):
            self._owned()
            encoded = base64.b64encode(data[i : i + 384]).decode()
            self.command(f"printf '%s' '{encoded}' | base64 -d >> {path}")
        self._check_asset(name, remote_name)

    def _check_asset(self, name: str, remote_name: str | None = None) -> None:
        path = self._asset_path(name, remote_name)
        digest = hashlib.md5(asset(name)).hexdigest()
        self.command(
            f"test ! -L {path} && test \"$(md5sum {path} | cut -d ' ' -f 1)\" = {digest}"
        )

    def provision(self) -> None:
        self._same_boot()
        if self.state() != "absent":
            raise RestoreError("conflict_before_setup")
        # Atomic mkdir prevents a second controller claiming a pre-existing tree.
        self.command(
            f"umask 077; mkdir {P} && printf '%s' {self.config.owner} > {P}/.phase8-owner && printf '%s' dlink-phase6a-v1 > {P}/.phase6a-owned"
        )
        self._upload("phase6a_rollback.sh")
        self._upload("phase6a_setup.sh")
        self._owned()
        encoded = base64.b64encode(self.public_key.encode("ascii")).decode()
        self.command(
            f"sh {P}/phase6a_setup.sh '{encoded}'",
            timeout=60,
            failure="phase6_setup_failed_rollback_required",
        )

    def audit(self) -> None:
        self._owned()
        self.command(
            f'test ! -L {R} && test "$(cat {P}/.phase6a-owned)" = dlink-phase6a-v1'
        )
        sockets = self.command("netstat -lnt")
        if not any(
            len(t) >= 6 and t[3].endswith(":2222") and t[-1] == "LISTEN"
            for t in (line.split() for line in sockets.splitlines())
        ):
            raise RestoreError("owned_listener_missing")
        check_exposure(
            sockets, self.command("iptables -S"), self.command("ip6tables -S")
        )
        self.command(
            'awk \'$2=="/" && $3=="jffs2" && $4 ~ /(^|,)ro(,|$)/ {ok=1} END {exit !ok}\' /proc/mounts'
        )
        check_mounts(self.command("cat /proc/self/mountinfo"), staged=True)
        # Verify fixed process root and both required key-only/forwarding flags.
        self.command(
            f"n=$(cat {P}/launcher.pid); case $n in ''|*[!0-9]*) exit 1;; esac; test \"$(readlink /proc/$n/root)\" = {R} && tr '\\000' ' ' < /proc/$n/cmdline | grep -q -- '-p 10.0.0.2:2222 -s -j -k'"
        )
        self.command(
            "netstat -lnt | awk '$4 ~ /:22$/ {a=1} $4 ~ /:23$/ {b=1} END {exit !(a && b)}'"
        )

    def rollback(self) -> None:
        if self.boot is None:
            self.boot = self.snapshot()
        self._owned()
        name = "phase6a_rollback.sh"
        remote_name = None
        try:
            self._check_asset(name)
        except RestoreError as exc:
            if str(exc) != "remote_command_failed":
                raise
            # Repair an incomplete upload without overwriting or executing it.
            remote_name = "phase8-rollback-" + uuid.uuid4().hex + ".sh"
            self._upload(name, remote_name)
        self._owned()
        self.command(
            "sh " + self._asset_path(name, remote_name),
            timeout=60,
            failure="canonical_rollback_refused_or_failed",
        )
        if self.state() != "absent":
            raise RestoreError("rollback_incomplete")

    def close(self) -> None:
        if self.sock is not None:
            # Closing the transport cannot delete files or kill Dropbear.
            try:
                self._send("exit")
                self._send("exit")
            except Exception:
                pass
            self.sock.close()
            self.sock = None
