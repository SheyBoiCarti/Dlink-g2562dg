> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 9 live tests

| Test | Actual result |
|---|---|
| TCP reachability | Original SSH 22 and Telnet 23 reachable from 10.0.0.10; custom 2222 initially absent |
| Host trust | Stock RSA identity matched the prior trusted SHA-256 fingerprint; no trust bypass/update |
| Local credentials and key | Interactive setup completed; Windows vault presence and protected RSA-3072 public/private match verified without logging values |
| Original recovery | Authenticated Telnet shell UID 0, retained recovery session and fresh post-cleanup login verified |
| Read-only prerequisites | Exact firmware/kernel, boot-ID availability, RAM, tmpfs and read-only rootfs passed |
| Initial live restore | Public-key UID 0 and two-command PTY proof passed |
| Initial rollback | Inline command timed out; failed attempt preserved as PHASE9_MANUAL_ATTEMPT1.json |
| Recovery cleanup | Hash-verified staged original Phase 6 rollback removed listener/tree/six binds; no original service disruption |
| Repeated full manual test after fix | Restore=restored, status=ready, repeated restore=already_ready, rollback=removed, final status=absent |
| Original service preservation | Original PIDs 3244/1037 and host identity unchanged; same boot; fresh Telnet UID 0 passed |
| Single-instance check | A concurrent CLI command while watch held the lock returned another_instance_running |
| Foreground monitor | Passed two cycles, single-instance exclusion and final cleanup; task installed separately afterward |
| Router/Windows restart | Owner restarted router; post-restart trust verification, acceptance and complete manual round trip passed. No agent-initiated reboot or Windows restart |
| Disruptive recovery cases | Offline mocks only; no deliberate crash, wrong router-password attempt or forced router failure |

Evidence: [preflight](../archive/raw-evidence/PHASE9_PREFLIGHT.json), [authenticated preflight](../archive/raw-evidence/PHASE9_AUTHENTICATED_PREFLIGHT.json), [manual test](../archive/raw-evidence/PHASE9_MANUAL_EXECUTION.json), [first attempt](../archive/raw-evidence/PHASE9_MANUAL_ATTEMPT1.json), [recovery](../archive/raw-evidence/PHASE9_RECOVERY_EXECUTION.json), [input-length probes](../archive/raw-evidence/PHASE9_TELNET_LINE_LIMIT.json), [single-instance](../archive/raw-evidence/PHASE9_SINGLE_INSTANCE.json). Firewall policy evidence is retained in the restricted local deployment directory rather than copied wholesale into project reports.

No firmware, startup script, bootloader, flash partition, firewall rule, original SSH configuration or Telnet setting was deliberately modified. Ordinary management logging may occur. This does not claim a byte-comparison of every persistent router file.

Post-restart follow-up: the owner reported restarting the router. An unauthenticated SSH handshake observed a new public host fingerprint; 22/23 remain reachable and 2222 is absent. Stored-identity comparison failed as intended. No credentials or provisioning commands were sent. The new public key's provenance is not yet independently verified; no silent trust update was performed.

## Post-restart public identity verification

After explicit confirmation of the trusted physical Ethernet connection, read-only Telnet authentication returned UID 0. Public-only output from the runtime host key independently produced `[PUBLIC_KEY_FINGERPRINT_2]`, matching the SSH handshake. Uptime was about 138 seconds; root JFFS2 remained ro and the scratch deployment was absent. The local trust pin has not yet been changed; explicit acceptance of the new verified fingerprint is pending. This demonstrates the operational blocker to fully unattended post-reboot restoration under the required strict trust policy: a changed host identity requires owner verification/acceptance. No stable host key was written to flash or restored by the tool. [Evidence](../archive/raw-evidence/PHASE9_POST_RESTART_KEY_VERIFICATION.json).

## Final approved scheduled deployment

The owner explicitly approved registration/enabling/start. Direct non-elevated registration was denied without creating the task; the owner-approved UAC installer registered it under the same user with Limited/Interactive principal and started it. The task is Running and enabled, with Boot/Logon/NetworkProfile triggers and IgnoreNew. Direct router verification found an owned six-bind deployment, expected IPv4-only listener, trusted identity, successful key authentication, UID 0 and interactive PTY. Original SSH/Telnet PIDs 2680/996 and root ro were preserved. A duplicate start returned a refusal while the same single monitor lock owner remained; that result is not labeled completed-run success. The task and RAM listener are intentionally left active. [Task evidence](../archive/raw-evidence/PHASE9_TASK_DEPLOYMENT.json); [SSH proof](../archive/raw-evidence/PHASE9_SCHEDULED_RESTORE.json).
