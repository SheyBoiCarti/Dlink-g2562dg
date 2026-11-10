# Historical Research Archive

This directory stores the preserved chronological records, discovery phases, and raw evidence from the original device investigation.

For current architecture, guides, and reproducible usage instructions, refer to [`docs/`](../docs/) and the root [`README.md`](../README.md).

---

## Structure

- [`phase-history/`](phase-history/): Chronological markdown reports documenting each stage of discovery:
  - `PHASE2_RESULTS.md`: Initial port scanning and network reconnaissance.
  - `PHASE3_RESULTS.md`: Stock SSH banner probes and legacy cipher evaluation.
  - `PHASE3B_RESULTS.md`: Telnet and FTP protocol evaluation.
  - `PHASE4_RESULTS.md`: UART hardware safety and pinout research.
  - `PHASE5_RESULTS.md`: Read-only Linux rootfs and Dropbear binary analysis.
  - `PHASE6A_RESULTS.md`: Dropbear RAM chroot deployment prototype.
  - `PHASE6B_RESULTS.md`: PTY allocation diagnostics and client terminal isolation.
  - `PHASE7_RESULTS.md`: Storage persistence analysis (JFFS2/tmpfs).
  - `PHASE8_RESULTS.md`: Windows automation controller design and safeguards.
  - `PHASE9_RESULTS.md`: Live automated restore, rollback, and reboot recovery testing.
- [`phase-1-reconnaissance/`](phase-1-reconnaissance/): Phase 1 preliminary public source survey and hypothesis formation before active device testing.
- [`raw-evidence/`](raw-evidence/): Sanitized JSON command logs, execution transcripts, and preflight test records referenced throughout the phase reports.
