> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Deployment status — Phase 9

**Deployed and running after explicit owner approval.**

- Windows task: `DLinkSSHRestore`, enabled and Running, same Windows user, Interactive token, Limited privileges.
- Triggers: Windows startup, user logon and network-connected event; network availability required, IgnoreNew multiple-instance policy. No Windows restart/sign-out was performed to exercise those triggers individually.
- Current temporary listener: `10.0.0.2:2222`, key-only stock Dropbear in the verified RAM chroot. Independent SSH authentication, UID 0 and interactive PTY proof passed while the task was running.
- Logical IPv4 ingress, absence of custom IPv6/wildcard sockets and six private mounts: verified. End-to-end WAN/stock Telnet isolation remains unverified.
- Original port-22 SSH PID 2680 and Telnet PID 996 remain intact after the owner's restart. Root JFFS2 remains read-only.
- Manual restoration/status/idempotence/rollback passed before and after the owner-reported restart. The foreground monitor passed two cycles and cleanup; scheduled restoration was then separately installed, started and verified.
- One monitor lock owner was observed. A duplicate task start was refused without creating another instance; the refusal result is recorded separately from live service verification.
- Regression suite: 70 passed on Python 3.12 and 3.14, one generic opt-in live test skipped; equivalent approved live tests were executed with recorded controllers. Lint/format and rebuilt wheel checks passed before scheduled deployment.

## Host identity is an explicit operational gate

The owner restarted the router. Its host fingerprint changed from the prior pin to `[PUBLIC_KEY_FINGERPRINT_2]`. Credentials were withheld until the owner confirmed trusted physical Ethernet and approved read-only Telnet verification. The console's public host key matched the SSH handshake; the owner then explicitly approved updating only the Windows trust pin. Post-restart root SSH restoration and rollback passed.

A future host-key change will stop automation again for independent verification and explicit acceptance. This is not fully unattended restoration across key rotation. No router host key was persisted/restored by this tool.

## Current state and recovery

The task and verified RAM listener are intentionally left running under the installation/start approval. To inspect through the CLI or roll back, stop the monitor task first; its local lock otherwise refuses concurrent commands. Stopping the task alone leaves the RAM listener intact. Use approved scoped rollback afterward, then uninstall the task only if desired. Keep original Telnet recovery. No agent-initiated reboot, flash write, firmware/startup edit, firewall change or Telnet disablement occurred.

Evidence: [scheduled task](../archive/raw-evidence/PHASE9_TASK_DEPLOYMENT.json), [independent scheduled SSH proof](../archive/raw-evidence/PHASE9_SCHEDULED_RESTORE.json), [post-restart manual test](../archive/raw-evidence/PHASE9_MANUAL_POST_RESTART.json), [trust verification](../archive/raw-evidence/PHASE9_POST_RESTART_KEY_VERIFICATION.json), [explicit trust update](../archive/raw-evidence/PHASE9_POST_RESTART_TRUST_UPDATE.json).
