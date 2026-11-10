> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 6B results: interactive SSH and persistence investigation

Date: 2026-10-19. Device `10.0.0.2`, firmware `TK_1.00TK_V1.2.12ak_20221018`, Linux 3.14.18 ARMv7, Dropbear 2014.63, Unix `admin` UID 0.

**Interactive UID 0 SSH works. Autonomous persistence is not ready under the current constraints.** The authorized RAM-only test was fully removed. No permanent changes or reboot occurred.

## Verified PTY diagnosis and proof

Began with read-only diagnostics through the original root Telnet route after reviewing Phase 5/6A. Live PTY drivers and Telnet descriptors established original-root PTY support. Matched live library digests to local ELF copies for offline PTY-code inspection; no router executable or new tracing tool was installed. No speculative `/proc` mount or device-node repair was applied.

After the user explicitly approved the documented temporary scope, reused the Phase 6A public key, six RAM-chroot binds and existing host identity. Original Dropbear/Telnet remained untouched. The test listener was exactly IPv4 `10.0.0.2:2222`, key-only, forwarding disabled.

[Full execution evidence](../raw-evidence/PHASE6B_EXECUTION.json) shows that the old inherited-stdin test reproduced exit 255. Client diagnostics explicitly show PTY allocation **accepted**, followed by `read failed` and `send eof`. With only stdin changed to a maintained pipe, TERM still unset, the same daemon returned UID 0 with terminal stdin/stdout and exit 0. TERM=xterm also passed. A separate login shell accepted multiple commands, returned `uid=0(admin) gid=0(admin)`, confirmed terminal stdin, answered a second command and exited 0. Thus the reported PTY failure was client-side stdin handling in the automation, not an established kernel/Dropbear allocation defect. The exact Windows handle error below SSH's failed read was not traced.

No-PTY interactive fallback was unnecessary and not tested. Resize, signal forwarding, full-screen tools, long sessions, reboots and vendor service-restart behavior remain untested. The successful shell has the temporary chroot filesystem view, not a complete original-root layout; UID 0 remains a real router privilege, not sandbox containment.

## Persistence decision

`/data/ssh/authorized_keys` is a conservative **candidate** public-key storage location, subject to retention checks and approval. `/data` is writable flash-backed log storage, not an established autorun facility. UID 0 Dropbear still needs absent `/etc/dropbear/authorized_keys` on read-only rootfs. No supported custom `/data` startup consumer was found in the inspected init, cron, hotplug, USB or SSH-service paths. This bounded search does not prove none exists in all firmware functionality.

A tested RAM chroot solves key lookup for a manually launched process. It does not solve boot execution, single-listener/vendor lifecycle ownership or original host identity across reboot. sysmgr generates its host key under volatile `/var`; no persistent restore mechanism was established. No private host key was copied or overwritten. The original wildcard port 22 listeners and IPv6 INPUT ACCEPT remain; full management protection is not yet achieved.

[Persistence assessment and commands](../../docs/SSH_PERSISTENCE.md) supplies exact gated public-key staging, tested runtime references and a proposed both-family firewall chain. Those new storage/firewall variations have **not** been executed and are not a tested autonomous installer. A ready persistence implementation cannot honestly be supplied until the missing boot/identity/service mechanism is established or constraints are explicitly revised.

## Rollback and final state

The test cleanup terminated only temporary chroot processes, unmounted all six binds, removed the owned RAM tree and independently reconfirmed fresh Telnet UID 0. [Final checks](../raw-evidence/PHASE6B_FINAL_CHECKS.json) verify original service PIDs 3244/1037, unchanged public host fingerprint, root JFFS2 `ro`, no global `/etc/dropbear`, no temporary tree/mounts and no port 2222 listener. No original account, host key, SSH configuration, startup or firewall was modified, and no deliberate persistent-partition provisioning write was made. Ordinary vendor logging may still update logs. The private client key stayed local and out of reports; it is ACL-restricted but not passphrase-encrypted.

## Task and success-criterion reconciliation

| Requirement | Outcome |
|---|---|
| Read prior work; read-only PTY, device and shell diagnostics | Completed |
| Diagnose failure; demonstrate interactive UID 0 SSH | Completed with controlled client-stdin comparison |
| Verify mount/path behavior before recommending changes | Existing six-bind design verified at runtime; no extra mount needed |
| Public-key persistence storage | Candidate and exact staging commands documented; writes/retention test pending separate approval |
| Existing startup hooks and original host identity | Inspected; autonomous boot consumer and identity retention unresolved |
| Avoid extra permanent listeners | No new listener left running; final single-service ownership design unresolved |
| IPv4/IPv6 security | Both inspected; proposed rules documented, no enforcement changes applied |
| Rollback/recovery | Temporary rollback tested; candidate persistent inverses documented |
| Tested persistence ready for implementation | **Not met**: boot consumer, stable identity, policy/lifecycle and retention gates remain |

Evidence: [read-only batch](../raw-evidence/PHASE6B_READONLY.json), [follow-up](../raw-evidence/PHASE6B_FOLLOWUP.json), [boot checks](../raw-evidence/PHASE6B_BOOT.json), [matching binary notes](../raw-evidence/PHASE6B_BINARY_NOTES.json), [approved execution](../raw-evidence/PHASE6B_EXECUTION.json), [independent final checks](../raw-evidence/PHASE6B_FINAL_CHECKS.json). Reports: [PTY diagnostics](../../docs/SSH_PTY_DIAGNOSTICS.md), [persistence](../../docs/SSH_PERSISTENCE.md), [rollback](../../docs/SSH_ROLLBACK.md), [Phase 7 readiness](PHASE7_READINESS.md).

Stop after Phase 6B. Interactive proof is complete; full Phase 6B success is partial because persistence readiness is not established. No permanent changes or reboot are authorized by the temporary-test permission.
