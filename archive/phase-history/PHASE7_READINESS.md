> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7 readiness after Phase 6B

**Not ready for autonomous persistent deployment, reboot validation or Telnet removal.** Interactive UID 0 SSH is now proven using the stock Dropbear with RAM-only key lookup. All test changes have been removed; original service configuration remains.

## Established

- `admin` maps to UID 0 and RSA public-key authentication works.
- Both PTY command execution and a multi-command login shell work when client stdin stays open. No router-side PTY fix was required.
- Existing host identity can be reused read-only in the current boot.
- Six-bind chroot setup and exact scoped rollback worked; fresh original Telnet UID 0 survived.
- `/data` is writable JFFS2 log storage. New public-key storage is technically plausible, but no key was written there.
- IPv4 and IPv6 policy were independently inspected. No new IPv6 SSH listener was created during testing.

## Pending gates

1. Establish a real boot consumer for a `/data` launcher without stock-rootfs/firmware changes, or explicitly revise those constraints. Current inspected paths do not supply one. Do not substitute a fictitious rc.local/UCI recipe.
2. Establish `/data/ssh` ownership, retention, available-space/log cleanup and factory-reset semantics; separately approve exact public-key staging and rollback.
3. Resolve original host identity across reboot without unauthorized host-key changes. Volatile key storage and vendor generation remain unresolved.
4. Establish one service owner/listener on port 22 and test vendor lifecycle handling. Do not leave permanent parallel daemons or race sysmgr's `killall dropbear`.
5. Review/apply/test SSH ingress restrictions in both families under separate approval. Current wildcard listeners and IPv6 ACCEPT are not a demonstrated LAN-only configuration.
6. Passphrase-protect the existing client private key locally before ongoing use; preserve private material outside reports and router.
7. Preserve configuration/boot baselines and resolve recovery limitations. Obtain explicit persistent-write, mount/service/firewall and reboot approval for the exact subsequent scope. Temporary-test permission does not authorize those actions.
8. Only after independent approved reboot and service-lifecycle verification, evaluate retiring Telnet with its own recovery/rollback plan. No such change now.

The next decision is the boot/identity integration approach, not a reboot or execution of a guessed persistence installer. [Results](PHASE6B_RESULTS.md), [persistence constraints and candidate commands](../../docs/SSH_PERSISTENCE.md), [rollback](../../docs/SSH_ROLLBACK.md) and [recovery limitations](../../docs/RECOVERY.md) provide the evidence and review boundaries. Phase 7 has not started.
