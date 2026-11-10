"""In-process encrypted SSH integration; never contacts the router or Windows vault."""

import re
import socket
import threading

import paramiko
import pytest

from dlink_ssh_restore.config import Config
from dlink_ssh_restore.restore import RestoreError
from dlink_ssh_restore.ssh import SSH, fingerprint


@pytest.fixture(scope="module")
def keys():
    return paramiko.RSAKey.generate(3072), paramiko.RSAKey.generate(2048)


class Vault:
    def get(self, name):
        return "offline-test-passphrase"


class Server(paramiko.ServerInterface):
    def __init__(self, key, uid, pty):
        self.key, self.uid, self.pty = key, uid, pty

    def check_auth_publickey(self, user, key):
        return (
            paramiko.AUTH_SUCCESSFUL
            if user == "admin" and key == self.key
            else paramiko.AUTH_FAILED
        )

    def get_allowed_auths(self, user):
        return "publickey"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_channel_pty_request(self, *args):
        return self.pty

    def check_channel_exec_request(self, channel, command):
        def reply():
            if self.uid == -99:
                channel.get_transport().close()
                return
            channel.sendall(
                f"{self.uid}\nuid={self.uid}(admin) gid=0(admin)\n".encode()
            )
            channel.send_exit_status(0)
            channel.shutdown_write()

        threading.Thread(target=reply, daemon=True).start()
        return True

    def check_channel_shell_request(self, channel):
        def reply():
            try:
                data = b""
                while True:
                    part = channel.recv(4096)
                    if not part:
                        return
                    data += part
                    while b"\n" in data:
                        line, data = data.split(b"\n", 1)
                        text = line.decode()
                        m = re.search(r"BEGIN([a-f0-9]{32})", text)
                        if m:
                            channel.sendall(
                                f"\nBEGIN{m[1]}\n{self.uid}\nTTY{m[1]}:0\n".encode()
                            )
                        m = re.search(r"SECOND([a-f0-9]{32})", text)
                        if m:
                            channel.sendall(f"\nSECOND{m[1]}\n".encode())
                        if text == "exit":
                            return
            except (EOFError, OSError):
                pass

        threading.Thread(target=reply, daemon=True).start()
        return True


@pytest.mark.parametrize(
    "uid,pty,match",
    [
        (0, True, None),
        (1, True, "uid_not_zero"),
        (0, False, "verification_failed"),
        (0, True, "host_identity_changed"),
        (0, True, "ssh_auth_failed"),
        (-99, True, "ssh_transport_unavailable"),
    ],
)
def test_encrypted_publickey_uid_and_interactive(
    monkeypatch, tmp_path, keys, uid, pty, match
):
    clientkey, hostkey = keys
    private = tmp_path / "testkey"
    clientkey.write_private_key_file(str(private), password="offline-test-passphrase")
    c = Config(
        timeout=3,
        private_key=str(private),
        host_fingerprint=(
            "SHA256:" + "A" * 43
            if match == "host_identity_changed"
            else fingerprint(hostkey)
        ),
    )
    client_socket, server_socket = socket.socketpair()
    transport = paramiko.Transport(server_socket)
    transport.add_server_key(hostkey)
    errors = []

    def serve():
        try:
            transport.start_server(
                server=Server(
                    hostkey if match == "ssh_auth_failed" else clientkey,
                    uid,
                    pty,
                )
            )
            while transport.is_active():
                channel = transport.accept(0.1)
                if channel is not None:
                    channel.settimeout(3)
        except (EOFError, OSError, paramiko.SSHException) as exc:
            errors.append(type(exc).__name__)

    worker = threading.Thread(target=serve, daemon=True)
    worker.start()
    monkeypatch.setattr(
        "dlink_ssh_restore.ssh.trusted_socket", lambda *args: client_socket
    )
    try:
        if match:
            with pytest.raises(RestoreError, match=match):
                SSH(c, Vault()).verify()
        else:
            assert SSH(c, Vault()).verify() == {"uid": 0, "interactive": True}
    finally:
        transport.close()
        client_socket.close()
        server_socket.close()
        worker.join(4)
        assert not worker.is_alive()
