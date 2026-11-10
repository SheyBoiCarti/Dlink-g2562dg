> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 6 readiness after read-only investigation

**Status: conditional readiness for a precisely scoped temporary public-key test; not ready for unattended persistence, stock-rootfs changes or Telnet removal.** No router write or service change is authorized by the Phase 5 request.

## What is established

- Verified root shell remains available through the existing Telnet management path.
- Unix `admin` is the existing UID 0 account. No new root account, passwd/shadow edit or home-directory change is needed.
- Actual Dropbear code supports key verification and uses `/etc/dropbear/authorized_keys` for UID 0.
- Runtime host identity matches the saved SSH host key.
- Live help supports a separate test listener bound to `10.0.0.2`, password auth disabled with `-s`, forwarding disabled with `-j -k`, and a separate PID file.
- Current firmware, mount types, storage limits, boot call sites and IPv4/IPv6 rules were inspected. Exact local baseline backups exist for three relevant boot files; the prior configuration export passed its integrity check.

## Gates before any write request is reviewable

1. Select and document the exact filesystem approach. `/etc/dropbear` is absent on read-only rootfs; a key in `/data` alone is ineffective. A RAM `/etc` view has system-wide effects; a rootfs link is a persistent stock-filesystem change. Neither has been approved or tested.
2. Choose a dedicated client RSA public key. Keep its private key local and protected. Do not transmit private key bytes or credentials through chat or project files.
3. Specify exact test files, modes, mount operations, daemon command, listener/PID, duration and inverse cleanup. Keep an existing Telnet root session and web access. Do not restart the vendor-managed listener for the initial proof.
4. Pin the current host identity, scope client legacy exceptions, force publickey authentication only and verify UID 0 using a second SSH connection. Signature/key-size compatibility remains a runtime test.
5. For persistence, resolve exact-build/NAND recovery, protected host-key retention, log-partition cleanup, boot ordering and `sysmgr` ownership. A reviewed rootfs patch must be shown as a concrete diff with exact rollback before requesting permission to deploy it.
6. Treat service-control and firewall changes as separate approvals. Cover both IPv4 and IPv6; present listener/policy diffs before applying them. Do not expose the legacy daemon to the Internet.
7. Obtain explicit reboot authorization before any persistence test. Do not disable Telnet until key-only access survives approved reboot and service lifecycle tests and a viable independent recovery route exists.

The staged technical proposal is [SSH_PERSISTENCE.md](../../docs/SSH_PERSISTENCE.md); its recovery prerequisites are [RECOVERY.md](../../docs/RECOVERY.md). The actual findings and limitations are in [PHASE5_RESULTS.md](PHASE5_RESULTS.md).

There is no automatic authorization to proceed after this report. Phase 5 ends with investigation complete and implementation deliberately unstarted.
