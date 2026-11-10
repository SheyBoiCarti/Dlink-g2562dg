> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7 results: SSH persistence and boot investigation

2026-10-19; 10.0.0.2; `TK_1.00TK_V1.2.12ak_20221018`; Linux 3.14.18 ARMv7; admin UID 0.

**No supported autonomous data-backed boot hook was established. Firmware flashing is not proven necessary.** A minimal stock startup edit could plausibly avoid flashing but violates the unchanged-rootfs constraint and remains unvalidated. Externally reapplying the proven RAM arrangement is an operational fallback, not autonomous persistence. No permanent changes implemented.

## Review and evidence

“Phase 56B” was interpreted as Phases 5 through 6B; no literal Phase56B-named document appears in the project inventory. Reviewed Phase 5/6A/6B results, readiness, persistence/recovery, Dropbear report and Phase 6B evidence JSON. The Phase 6B interactive proof supersedes historical PTY failures.

Fresh [read-only batch](../raw-evidence/PHASE7_READONLY.json) records identity, complete non-secret boot scripts, bounded searches, mounts/filesystems, config/path inventory, named non-secret settings, service/listener state, filtered strings and final digests. [Follow-up](../raw-evidence/PHASE7_FOLLOWUP.json) records extroot caller/content checks, ScriptFiles searches, filtered init flow and public identity. Existing local console collector uses process-local history suppression; no startup helper was executed. Public-key fingerprint independently computed locally matches `[PUBLIC_KEY_FINGERPRINT_1]`. No credential/private-key output was collected.

Two grep records include an echoed shell fragment; only explicit path/line matches and complete script content support findings. Strings are references, not execution proof. Prior binary analysis is distinguished from fresh live inspection.

## Requirement reconciliation

| Question | Finding / limit |
|---|---|
| Boot process | Main configured kernel/BusyBox/inittab/rcS/vendor-script/tdsmgr/after-script/service chain traced. Bootloader bank selection, proprietary init internals and concurrent completion order remain partial; no complete runtime boot trace claimed |
| Supported data autorun | None found in inspected init/syscfg/cron/hotplug/USB/service paths; bounded negative result |
| Host keys | Volatile RAM path and sysmgr generation/launch established; no restore found; reboot regeneration remains inference |
| Stock service extension | Enable/Port verified; no custom argv/public-key/host-key retention setting established; hardcoded UID-0 key path absent on ro root; vendor killall risks replacements |
| Config/overlay/mounts | Separate data JFFS2 and RAM var confirmed; no active overlay; extroot files register callbacks without established active boot caller; configuration export is not arbitrary code execution |
| Reversible unchanged-root boot integration | Not established; RAM chroot cannot bootstrap itself |
| Alternatives/proposal | Ranked comparison and gated launcher design in SSH_PERSISTENCE.md; no implementation supplied |
| Recovery | Original Telnet reauthenticated; prior temporary rollback proven; persistent boot-failure recovery unresolved |

## Deliverables and stop state

Updated BOOT_PROCESS.md, SSH_PERSISTENCE.md, SSH_HOST_KEYS.md, RECOVERY.md and this report with evidence, ranking, risks, prerequisites and recovery. Local documentation/evidence writes are authorized deliverables, not router provisioning. No deliberate persistent router file, configuration, partition, firmware or bootloader modification, package installation or reboot occurred. Final path/mount/listener checks corroborate baseline; no byte-comparison of every router state is claimed.

Research stops after Phase 7 at the stated evidence boundary. Unresolved questions are explicitly open; neither a ready autonomous installer nor proof that firmware modification is necessary is claimed. Further exact-build proprietary analysis/vendor evidence or revised constraints is required. No Phase 8 work began.
