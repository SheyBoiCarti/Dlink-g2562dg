> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 5 results: Linux environment and persistent SSH investigation

Date: 2026-10-19. Exact live software field reconfirmed: `TK_1.00TK_V1.2.12ak_20221018`. The previous [root access report](../../findings/ROOT_ACCESS_VERIFIED.md), account/SSH findings, environment/filesystem assessments and backup report were read before live investigation.

**Outcome:** the running Dropbear supports public-key authentication for the existing UID 0 Unix account `admin`, but uses `/etc/dropbear/authorized_keys`. That path is currently absent on read-only rootfs. A safe autonomous persistence mechanism without stock-rootfs changes has not been established. No SSH changes were implemented.

## Actual task outcomes

| Task | Verified finding / practical consequence |
|---|---|
| Linux environment | Linux 3.14.18 ARMv7; BusyBox 1.19.4; BusyBox init; OEM Barrier Breaker/VSPM3XX metadata. Root JFFS2 is read-only; `/var` is RAM; `/data` is a 2 MiB writable log partition |
| Dropbear | Running 2014.63 daemon uses `-r /var/dropbear/rsa_host_key -p 22`; `sysmgr` controls it through ServiceSSH Enable/Port. No standard Dropbear init/UCI config present |
| Account mismatch | CLI built-in identity differs from Unix passwd. Unix `admin` is UID/GID 0 with home `/`; Unix `root` is absent. Dropbear overrides `admin`'s in-memory password and directly compares it, independent of the web password |
| Public keys | Live ELF code confirms UID 0 lookup at `/etc/dropbear/authorized_keys`, ownership/write-bit checks and a signature-verification path. RSA is the compatible candidate. No client key installed or authentication success claimed |
| Persistence | `/var` loses runtime state; persistent `/data` is log storage, and no supported custom startup hook was found. Existing vendor boot script is a candidate only if changes to read-only stock rootfs are separately approved and recovery gates resolved |
| Network security | SSH listens on all IPv4/IPv6 addresses. IPv4 INPUT DROP with LAN accept; IPv6 INPUT ACCEPT. Current IPv6 addresses are loopback/link-local only; future exposure is not ruled out |
| Backups / recovery | Existing config-export integrity verified; three exact boot files copied to restricted local storage. Full exact-build/NAND/bootloader recovery and host-key backup remain unverified |

## Concrete next design

Use `admin@10.0.0.2`, a dedicated RSA public key, vendor-required key path, trusted file permissions and a stable host identity. First obtain approval for a precisely reversible temporary test arrangement and a separate LAN-bound key-only listener. No passwd/shadow edit is needed to map the account to root.

For persistent deployment, resolve `/etc/dropbear` creation, `/data` retention, a reviewed boot integration point and `sysmgr` service-update races. A possible small rootfs link/boot-script change does not replace the firmware image, but it **does change stock filesystem contents** and is not authorized now. [The staged plan](../../docs/SSH_PERSISTENCE.md) identifies each approval and validation gate. [Phase 6 readiness](PHASE6_READINESS.md) does not clear unattended persistence or Telnet removal.

## Evidence and validation

Sanitized live observations are retained in:

- [Batch 1](../raw-evidence/PHASE5_OBSERVATIONS_1.json): identity, BusyBox, release fields, partitions/capacity, account classifications, daemon help, processes and init.
- [Batch 2](../raw-evidence/PHASE5_OBSERVATIONS_2.json): mount summary and actual daemon argv. This collection stopped on a local console-encoding error; only saved records are evidence.
- [Batch 3](../raw-evidence/PHASE5_OBSERVATIONS_3.json): persistent directory/capacity, boot references, runtime key metadata, socket bindings and interfaces.
- [Batch 4](../raw-evidence/PHASE5_OBSERVATIONS_4.json): key fingerprint, tool/init inventory, volatile symlinks and initial IPv4 firewall observations.
- [Batch 5](../raw-evidence/PHASE5_OBSERVATIONS_5.json): JFFS2 source mapping, NAND geometry, account count and IPv4/IPv6 policy. The first SSH config values were concatenated and were resolved by a labeled follow-up.
- [Batch 6](../raw-evidence/PHASE5_OBSERVATIONS_6.json): firewall remainder, IPv6 scopes, MTD capability flags, labeled ServiceSSH settings, command line and final root/mount baseline.
- [Batch 7](../raw-evidence/PHASE5_OBSERVATIONS_7.json): log mount command, empty shutdown script, key metadata and unchanged final listeners/mount modes.
- [Batch 8](../raw-evidence/PHASE5_OBSERVATIONS_8.json): live vendor boot-hook reference, log destinations, exact firmware/hardware fields and file modes.
- [SSH probe](../raw-evidence/PHASE5_SSH_PROBE.json): strict known-host match and advertised methods; no password, agent credential or public key was offered, so its expected rejection is not another password failure.
- [Binary analysis](../raw-evidence/PHASE5_BINARY_ANALYSIS.json): exact running executable identities and instruction ranges supporting vendor authentication and lifecycle conclusions. No credential constants are retained in this report.

Early prompt-only/empty observations were not upgraded into facts; later targeted commands resolved the relevant mount/path/account questions. A marker-parser issue was corrected locally, and affected observations were repeated. Public fingerprint extraction from the running host key matched the previously trusted SHA-256 fingerprint; private key bytes were not emitted or saved. Local boot-file backups and configuration-export integrity were checked independently.

Offline analysis used existing Python ELF/Capstone tooling. Live Dropbear was byte-identical to the previously acquired official older image; `sysmgr`, `srvcmgr` and `ams_cli` were not, so current live evidence took precedence. No extracted router executable was run on the PC. Upstream documentation is supporting context; the vendor's key-file and password behavior were derived from its actual binary.

## Completion and scope reconciliation

- Completed: prior-evidence review and live read-only Linux/storage/init inspection.
- Completed: current Dropbear/account/key-path/startup analysis and no-credential SSH negotiation.
- Completed: IPv4/IPv6 policy inspection, backup validation, recovery-risk assessment and gated persistence plan.
- Completed: all six requested reports, evidence references and project navigation updates.

Unperformed implementation tests are explicitly future gates, not unfinished Phase 5 actions: no authorized-key install, key login, daemon launch/restart, remount, firewall edit, passwd/shadow edit, host-key change, boot-hook edit, raw partition write, package operation, reboot or Telnet-disable operation occurred. Telnet sessions were closed after inspection; the collector made no deliberate persistent router writes. Process-local history suppression and ordinary automatic device logging are distinct from changing router configuration.

**Stop after Phase 5.** No Phase 6 implementation began. Successful persistent key-only SSH is not claimed.
