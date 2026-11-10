> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# SSH rollback and recovery: Phase 6B

## Actual final state

The approved RAM-only test was fully removed. [Execution evidence](../archive/raw-evidence/PHASE6B_EXECUTION.json) verifies cleanup and a fresh Telnet root login; [independent final checks](../archive/raw-evidence/PHASE6B_FINAL_CHECKS.json) confirm original Dropbear PID 3244, Telnet PID 1037, unchanged host public fingerprint, read-only JFFS2 root and absence of port 2222 and `/tmp/dlink-phase6a`. No `/data/ssh` was installed and no firewall/startup changes were made. There is nothing persistent from this phase to undo.

## Tested temporary cleanup

Keep the original-root Telnet management session open. From that shell, while an approved test is active:

```sh
sh /tmp/dlink-phase6a/phase6a_rollback.sh
```

The [exact reviewed rollback script](../scripts/phase6a_rollback.sh) was executed successfully in Phase 6A and 6B. It verifies the fixed scratch path and ownership marker, sends TERM only to processes whose `/proc/PID/root` equals `/tmp/dlink-phase6a/root`, confirms their exit, then unmounts only:

```text
/tmp/dlink-phase6a/root/dev/pts
/tmp/dlink-phase6a/root/var
/tmp/dlink-phase6a/root/dev
/tmp/dlink-phase6a/root/usr
/tmp/dlink-phase6a/root/lib
/tmp/dlink-phase6a/root/bin
```

It uses `umount -n`, no force/lazy unmount. It refuses deletion if any descendant mount remains; only after those guards does it remove the owned RAM tree. Never run recursive removal through mounted `/var` or `/dev` binds. Never use `killall dropbear`. If the process/mount guards fail, preserve the tree and investigate from original Telnet; do not reboot or escalate to forced removal automatically.

Verify after cleanup:

```sh
test ! -e /tmp/dlink-phase6a && test ! -L /tmp/dlink-phase6a
awk '$5 ~ /^\/tmp\/dlink-phase6a\// {print}' /proc/self/mountinfo
netstat -lnt | awk 'NR<3 || $4 ~ /:(22|23|2222)$/'
awk '$2=="/" && $3=="jffs2" {print $2,$3,$4}' /proc/mounts
dropbearkey -y -f /var/dropbear/rsa_host_key 2>/dev/null | awk '/Fingerprint:/{print}'
id -u
```

Require no scratch mounts/listener, original service PIDs/argv, original public fingerprint and root `ro`. Then perform a **fresh** Telnet login, enter `sh`, verify `id -u` is 0 and close normally. Do not log credentials or private key output. Phase 6B completed these checks.

## Future data-key staging rollback (not executed)

Before any separately approved `/data/ssh` staging, record that the path is absent, create only the reviewed files, retain their exact public-content digest locally and record owner/modes. If staging fails, inspect partial files first. If later removing a newly introduced deployment, verify `/data/ssh` is the expected real directory, has no mounts or unexpected files, and both key file content and directory ownership match the recorded deployment. Then remove only the matching `authorized_keys` (and matching `.new` if present) with individual `rm` commands and `rmdir /data/ssh`. Stop if identity checks fail. Never remove a pre-existing key or use `rm -rf /data`.

File deletion reverses provisioning, not flash wear. No host private key is included in this proposed storage; persisting one requires separate protected backup/restore design. No generic restore/copy of host keys is authorized.

## Future firewall candidate rollback (not executed)

Only if the exact previously absent `DLINK_SSH_LAN` chain and jump were introduced under separate approval, verify their exact contents and remove the corresponding INPUT jump, then the owned chain, in each affected family:

```sh
iptables -D INPUT -p tcp --dport 22 -j DLINK_SSH_LAN
iptables -F DLINK_SSH_LAN
iptables -X DLINK_SSH_LAN
ip6tables -D INPUT -p tcp --dport 22 -j DLINK_SSH_LAN
ip6tables -F DLINK_SSH_LAN
ip6tables -X DLINK_SSH_LAN
```

These operations are conditional inverse commands, not needed now. Do not flush INPUT or any vendor chain. If only one family was installed, remove only its recorded changes. A failed removal must be investigated; do not assume an IPv4 rollback changes IPv6. Verify the original policy/listeners and fresh recovery afterward.

## Recovery limits

Telnet remains the verified recovery route. The restricted local configuration export and boot-file baselines described in [RECOVERY.md](RECOVERY.md) are preserved. They are not a complete firmware/NAND recovery set. Physical UART voltage/pinout, exact-build recovery image, NAND restore and bootloader recovery remain unverified. No reset, restore, reboot, flash rewrite or startup-file edit is part of rollback for this phase. Client private key remains local, ACL-protected and unencrypted; protect it with a passphrase before ongoing use.
