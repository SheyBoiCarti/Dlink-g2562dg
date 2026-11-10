import base64

import pytest

from dlink_ssh_restore.restore import RestoreError
from dlink_ssh_restore.router import Router, TelnetCodec, parse_result
from dlink_ssh_restore.ssh import fingerprint, verify_public_key


def test_fragmented_telnet_negotiation():
    c = TelnetCodec()
    assert c.feed(b"LOG\xff")[0] == b"LOG"
    data, reply = c.feed(b"\xfb\x01IN#")
    assert data == b"IN#"
    assert reply == b"\xff\xfe\x01"


def test_subnegotiation_not_shell_output():
    c = TelnetCodec()
    assert c.feed(b"\xff\xfa\x18hidden")[0] == b""
    assert c.feed(b"\xff\xf0ok\xff\xff")[0] == b"ok\xff"


def test_framing_ignores_echoed_marker():
    raw = "cmd printf 'STARTabc'; echo ENDabc:0\nSTARTabc\n0\nENDabc:0\n~ #"
    assert parse_result(raw, "abc") == "0"


def test_remote_exit_failure():
    with pytest.raises(RestoreError, match="remote_command"):
        parse_result("STARTabc\nerr\nENDabc:1\n", "abc")


def test_public_key_must_match_private():
    class Key:
        def asbytes(self):
            return b"key"

        def get_bits(self):
            return 3072

    assert fingerprint(Key()).startswith("SHA256:")
    with pytest.raises(RestoreError):
        verify_public_key("ssh-rsa " + base64.b64encode(b"other").decode(), Key())


def test_no_secret_in_errors():
    with pytest.raises(RestoreError) as e:
        parse_result("STARTabc\nVERY_SECRET\nENDabc:4\n", "abc")
    assert "VERY_SECRET" not in str(e.value)


def test_dependency_supports_proven_legacy_algorithms():
    import paramiko

    # These algorithms were actually negotiated in Phase 6; without them no connection is possible.
    assert "diffie-hellman-group14-sha1" in paramiko.Transport._kex_info
    assert "ssh-rsa" in paramiko.Transport._key_info


class Wire:
    def __init__(self, chunks):
        self.chunks = iter(chunks)
        self.sent = []

    def settimeout(self, value):
        pass

    def recv(self, count):
        return next(self.chunks, b"")

    def sendall(self, data):
        self.sent.append(data)

    def close(self):
        pass


def test_complete_status_line_across_packets():
    from dlink_ssh_restore.config import Config

    r = Router(Config(), None, "")
    r.sock = Wire([b"\nENDabc:", b"0\r", b"\n~ #"])
    assert "ENDabc:0\n" in r._read(b"\nENDabc:")


def test_actual_wrong_password_is_classified_without_secret():
    from dlink_ssh_restore.config import Config

    r = Router(Config(), None, "")
    r.sock = Wire([b"The login info is not correct, please retry.\nLOGIN#"])
    with pytest.raises(RestoreError, match="credentials_rejected"):
        r._read(b"AMS#")
