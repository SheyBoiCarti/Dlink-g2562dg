> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 9 final deployment outcome

**Live implementation validation and approved scheduled deployment succeeded.** The current-user Limited/Interactive task is enabled and Running, and independent verification of its listener passed key authentication, UID 0, interactive PTY, logical ingress and six-bind mount checks. The owner-approved task and RAM listener are left active. Original SSH/Telnet and read-only rootfs remain intact.

Manual restore/status/repeated restore/rollback passed before and after an owner-performed router restart. The restart changed the host identity: verification stopped first, trusted physical Ethernet was explicitly confirmed, public console/SSH fingerprints matched, then the owner explicitly accepted the new Windows trust pin. This demonstrates functional restoration after reboot with an explicit trust gate; fully unattended restoration across rotating host keys is not claimed.

Scheduled task registration/start was separately approved. Windows denied the non-elevated attempt; an owner-approved UAC installer registered the reviewed same-user Limited task. Duplicate-start refusal and a single unchanged monitor lock owner corroborate single-instance behavior. Task Running was independently checked against actual SSH proof rather than treated as restoration success on its own. No startup/logon/network trigger was force-fired via reboot/sign-out/network disruption.

The regression suite passed 70 tests on Python 3.12 and 3.14; one generic opt-in live case remained skipped because approved equivalent controllers supplied explicit live evidence. Firewall grammar, bounded rollback staging and Windows event-trigger CIM metadata bugs were fixed with regressions. Unchanged Phase 6A/6B assets are retained in the rebuilt verified wheel. The earlier timeout/recovery evidence and chronological notes below are preserved; this final outcome supersedes historical pending states.

Remaining security limits: stock Telnet is plaintext and its end-to-end Internet isolation remains unverified; only logical custom-listener ingress/socket policy was verified. The owner explicitly requested the existing Telnet credential in chat; no such value was copied into project reports or application logs. A signed-in Windows user is required; future changed SSH identity needs explicit verification/acceptance. No agent-initiated reboot, firmware/startup/bootloader modification, deliberate router flash write, firewall change or Telnet disablement occurred.

[Current status](../../findings/DEPLOYMENT_STATUS.md) · [Live results](../../findings/LIVE_TEST_RESULTS.md) · [Scheduled task evidence](../raw-evidence/PHASE9_TASK_DEPLOYMENT.json) · [Independent scheduled SSH proof](../raw-evidence/PHASE9_SCHEDULED_RESTORE.json).

Stop after Phase 9. No Phase 10 work began.

## Chronological implementation and checkpoint record

# Phase 9 results

**Manual live root SSH restoration and scoped rollback passed. Scheduled deployment remains gated; reboot behavior and end-to-end WAN isolation are not verified.**

The existing Phase 8 application was deployed for an owner-approved temporary RAM integration. Real key authentication returned UID 0; the PTY login shell and second command passed. Status and duplicate restore were correct. The full sequence passed after fixing two compatibility defects discovered by real testing: stock firewall grammar and overlong Telnet rollback input. Original Phase 6A/6B shell assets were reused unchanged; no redesign or firmware modification occurred.

Initial rollback timed out and was not reported as successful. Original-root recovery remained available, the staged verified original rollback removed all temporary resources, and the corrected full trial then passed. Evidence and per-test boundaries are in [LIVE_TEST_RESULTS](../../findings/LIVE_TEST_RESULTS.md) and [deployment guide](../../docs/AUTOMATION_DEPLOYMENT.md).

Local setup completed interactively with Windows Credential Manager and an encrypted RSA-3072 key outside OneDrive. Only current user and SYSTEM can access the private-key file. No secrets are included in these reports. Host identity remains pinned and unchanged. No automatic trust acceptance is implemented.

The foreground monitor passed two verified cycles (restored then already_ready), was stopped, and all owned router resources were rolled back. The regression suite passes 70 tests; one generic live-router test remains intentionally gated because the equivalent approved round trip was executed with its own evidence controller. The corrected scheduler installer passes an actual Windows -WhatIf definition check without registration. Scheduled installation/enabling is separately approval-gated and has not been performed. Offline recovery tests cover unreachable router, credentials, mismatch, duplicate execution, partial/interrupted setup and missing owned listener; disruptive variants were not induced on the router.

Security boundary: the custom listener passes logical IPv4 ingress and no-custom-IPv6-socket checks, but stock wildcard Telnet/SSH with IPv6 INPUT ACCEPT prevent a blanket claim of secure management exposure. No external WAN vantage or approved reboot test exists. Windows user sign-in is required. Automatic restoration across host-key rotation stops for explicit trust verification.

Phase 9 continues only through its authorized test/deployment checkpoints. No Phase 10 work, reboot, flash write, firmware/startup change or Telnet disablement is authorized.

Application runtime log/evidence review found no stored credential values or private-key blocks. Separately, the owner explicitly requested that the existing Telnet credential be shown in chat; that disclosure is outside application logs and was not copied into project reports. Two offline tests initially encountered the live monitor lock while run concurrently; rerunning after the monitor stopped passed. No lock bypass or behavior change was made.

Final verification: 70 tests passed on Python 3.12 and 3.14, one generic opt-in live test skipped; lint/format and rebuilt-wheel byte comparisons passed. The scheduler event-trigger CIM metadata defect was also fixed and exercised through a registration-forbidden WhatIf regression. Final authenticated status is absent, and DLinkSSHRestore task does not exist. Scheduled deployment remains awaiting separate owner approval.

## Post-restart public identity verification

After explicit confirmation of the trusted physical Ethernet connection, read-only Telnet authentication returned UID 0. Public-only output from the runtime host key independently produced `[PUBLIC_KEY_FINGERPRINT_2]`, matching the SSH handshake. Uptime was about 138 seconds; root JFFS2 remained ro and the scratch deployment was absent. The local trust pin has not yet been changed; explicit acceptance of the new verified fingerprint is pending. This demonstrates the operational blocker to fully unattended post-reboot restoration under the required strict trust policy: a changed host identity requires owner verification/acceptance. No stable host key was written to flash or restored by the tool. [Evidence](../raw-evidence/PHASE9_POST_RESTART_KEY_VERIFICATION.json).
