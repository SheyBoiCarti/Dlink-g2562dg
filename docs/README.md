# Documentation Directory

Comprehensive technical guides, architectural explanations, and operational manuals for D-Link DSL-G2562DG root access and SSH automation.

---

## Getting Started & Operations

| Guide | Description |
|---|---|
| [`REPRODUCING.md`](REPRODUCING.md) | Step-by-step reproduction walkthrough for unlocking root and starting SSH. |
| [`../automation/README.md`](../automation/README.md) | Installation, CLI configuration, and Windows Task Scheduler deployment. |
| [`SECURITY.md`](SECURITY.md) | Trust boundary definitions, host key pinning, and safe operational guidelines. |
| [`RECOVERY.md`](RECOVERY.md) | Clean rollback, unmounting temporary chroot trees, and recovery troubleshooting. |
| [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) | Resolving common transport, authentication, or host verification issues. |

---

## Technical Deep-Dives

| Document | Topic |
|---|---|
| [`RESEARCH.md`](RESEARCH.md) | Full architectural explanation of the RAM chroot and Dropbear restoration trick. |
| [`DROPBEAR_ANALYSIS.md`](DROPBEAR_ANALYSIS.md) | Firmware Dropbear binary inspection, hardcoded paths, and key constraints. |
| [`LINUX_ENVIRONMENT.md`](LINUX_ENVIRONMENT.md) | Device OS details (Linux 3.14.18 ARMv7, BusyBox 1.19.4, `/tmp` tmpfs). |
| [`FILESYSTEM.md`](FILESYSTEM.md) | Read-only JFFS2 rootfs layout and mount propagation properties. |
| [`SSH_SERVICE.md`](SSH_SERVICE.md) | Dual Dropbear listener model (stock port 22 vs custom RAM port 2222). |
| [`SSH_HOST_KEYS.md`](SSH_HOST_KEYS.md) | Cryptographic host key behavior, reboot regeneration, and trust pinning. |
| [`BOOT_PROCESS.md`](BOOT_PROCESS.md) | Device startup flow and persistence assessment. |
| [`SSH_PTY_DIAGNOSTICS.md`](SSH_PTY_DIAGNOSTICS.md) | Pseudo-terminal allocation diagnostics and stdin/stdout handling. |
| [`UART_ACCESS.md`](UART_ACCESS.md) | Hardware serial console safety considerations and pinout assessment. |

---

## Historical Research & Claims

- [`READING_GUIDE.md`](READING_GUIDE.md): Chronology and guide for auditing historical evidence.
- [`README_CLAIMS.md`](README_CLAIMS.md): Claim-to-evidence matrix mapping every assertion to test results.
- [`PUBLICATION.md`](PUBLICATION.md): Notes on data sanitization, exclusions, and redaction.
- [`../research/firmware/README.md`](../research/firmware/README.md): Recovered offline extractor and exact-image reproduction.
- [`../archive/`](../archive/): Historical investigation phase logs and raw evidence files.
