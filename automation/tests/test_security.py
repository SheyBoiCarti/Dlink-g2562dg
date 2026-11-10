import pytest

from dlink_ssh_restore.config import Config
from dlink_ssh_restore.security import ExposureError, check_exposure

SAFE = "-P INPUT DROP\n-A INPUT -i lo -j ACCEPT\n-A INPUT -i br0 -j ACCEPT\n-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT"
SOCKETS = "tcp 0 0 10.0.0.2:2222 0.0.0.0:* LISTEN\ntcp 0 0 :::22 :::* LISTEN"


def test_ipv4_specific_ipv6_absent():
    check_exposure(SOCKETS, SAFE, "-P INPUT ACCEPT")


@pytest.mark.parametrize("addr", ["0.0.0.0:2222", ":::2222", "10.0.0.3:2222"])
def test_bad_binds(addr):
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS + "\ntcp 0 0 " + addr + " * LISTEN", SAFE, "-P INPUT ACCEPT"
        )


def test_ipv4_wan_accept_rejected():
    with pytest.raises(ExposureError):
        check_exposure(SOCKETS, "-P INPUT ACCEPT", "-P INPUT ACCEPT")


def test_unknown_match_rejected():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS, "-P INPUT DROP\n-A INPUT -m mystery -j ACCEPT", "-P INPUT ACCEPT"
        )


def test_chain_accept_rejected():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS,
            "-P INPUT DROP\n-N service\n-A INPUT -j service\n-A service -j ACCEPT",
            "-P INPUT ACCEPT",
        )


def test_config_injection_rejected():
    with pytest.raises(ValueError):
        Config(host="10.0.0.2;reboot")


def test_wildcard_bridge_is_not_all_trusted():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS, "-P INPUT DROP\n-A INPUT -i br+ -j ACCEPT", "-P INPUT ACCEPT"
        )


def test_no_private_key_or_remote_secret_reaches_logs(caplog):
    from dlink_ssh_restore.cli import main

    caplog.set_level("INFO")
    assert main(["--config", "this-file-does-not-exist.toml", "status"]) == 2
    assert "configuration_or_local_file_error" in caplog.text


def test_low_ram_prevents_any_provisioning(system):
    from dlink_ssh_restore.restore import RestoreError

    r, s, x = system
    r.fail = "ram"
    with pytest.raises(RestoreError, match="ram"):
        x.run()
    assert r.installs == 0 and r.cleanup == 0


def test_encrypted_key_required(tmp_path):
    import paramiko

    from dlink_ssh_restore.restore import RestoreError
    from dlink_ssh_restore.ssh import load_private

    path = tmp_path / "private"
    key = paramiko.RSAKey.generate(3072)
    key.write_private_key_file(str(path))
    with pytest.raises(RestoreError, match="passphrase_protected"):
        load_private(Config(private_key=str(path)), "")
    key.write_private_key_file(str(path), password="only-a-test-passphrase")
    assert (
        load_private(Config(private_key=str(path)), "only-a-test-passphrase").asbytes()
        == key.asbytes()
    )
    with pytest.raises(RestoreError, match="load_failed"):
        load_private(Config(private_key=str(path)), "incorrect-test-passphrase")


def test_owned_mount_inventory_requires_all_six_private_targets():
    from dlink_ssh_restore.security import check_mounts

    targets = ["bin", "lib", "usr", "dev", "var", "dev/pts"]
    rows = [
        "1 0 31:0 / / ro - jffs2 mtd:rootfs ro",
        "2 1 0:1 / /tmp rw - tmpfs none rw",
    ]
    for i, name in enumerate(targets, 3):
        rows.append(f"{i} 1 0:1 / /tmp/dlink-phase6a/root/{name} rw - tmpfs none rw")
    check_mounts("\n".join(rows), staged=True)
    with pytest.raises(ExposureError, match="mount"):
        check_mounts("\n".join(rows[:-1]), staged=True)
    rows[-1] = rows[-1].replace("rw -", "rw shared:1 -")
    with pytest.raises(ExposureError, match="propagation"):
        check_mounts("\n".join(rows), staged=True)


def test_stock_multicast_empty_and_drop_only_chains():
    policy = """-P INPUT DROP
-N ipsec_vpn
-N anti_attack
-N ANTI_TARGET
-N service_list
-N dhcp_relay
-A INPUT -m pkttype --pkt-type multicast -j ACCEPT
-A INPUT -j ipsec_vpn
-A INPUT -j anti_attack
-A INPUT -j service_list
-A INPUT -j dhcp_relay
-A anti_attack -i br0 -j RETURN
-A anti_attack -p tcp -m tcp --tcp-flags SYN,ACK SYN -m hashlimit --hashlimit-above 30/sec --hashlimit-burst 30 --hashlimit-name syncookies -j ANTI_TARGET
-A ANTI_TARGET -j DROP
-A service_list -i lo -j ACCEPT
-A service_list -i br0 -j ACCEPT
-A service_list -m state --state RELATED,ESTABLISHED -j ACCEPT
-A dhcp_relay -p udp -m udp --dport 67 -j ACCEPT"""
    check_exposure(SOCKETS, policy, "-P INPUT ACCEPT")


def test_unicast_accept_is_not_multicast_exception():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS,
            "-P INPUT DROP\n-A INPUT -m pkttype --pkt-type unicast -j ACCEPT",
            "-P INPUT ACCEPT",
        )


def test_unknown_drop_matches_cannot_hide_later_accept():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS,
            "-P INPUT DROP\n-A INPUT -m mystery -j DROP\n-A INPUT -j ACCEPT",
            "-P INPUT ACCEPT",
        )


def test_chain_with_unknown_accept_is_never_ignored():
    with pytest.raises(ExposureError):
        check_exposure(
            SOCKETS,
            "-P INPUT DROP\n-N anti\n-A INPUT -j anti\n-A anti -m mystery -j ACCEPT",
            "-P INPUT ACCEPT",
        )


@pytest.mark.parametrize(
    "policy",
    [
        "-P INPUT DROP\n-N loop\n-A INPUT -j loop\n-A loop -j loop",
        "-P INPUT DROP\n-N anti\n-N deny\n-A INPUT -j anti\n-A anti -g deny\n-A deny -j DROP",
        "-P INPUT DROP\n-N anti\n-A INPUT -j anti\n-A anti -j MARK --set-mark 1",
        "-P INPUT DROP\n-N anti\n-A INPUT -j anti\n-A INPUT -j ACCEPT\n-A anti -j RETURN\n-A anti -j DROP",
    ],
)
def test_deny_only_optimization_preserves_boundary_refusals(policy):
    with pytest.raises(ExposureError):
        check_exposure(SOCKETS, policy, "-P INPUT ACCEPT")
