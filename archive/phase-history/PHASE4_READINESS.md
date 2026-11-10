> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 4 readiness

## Latest recommendation after Phase 3B

Phase 3B verified Telnet's D-Link ams_cli / LOGIN# frontend and unauthenticated FTP metadata only. No root shell, supported network root account or filesystem access established. Read [Phase 3B results](PHASE3B_RESULTS.md) before the older recommendations below.

The most promising root-specific lead is the exact-model UART-root report. Immediate safe next step: obtain board-revision-matched pinout/voltage/serial/boot-authentication evidence from the report author or vendor before proposing hardware access. For technical progress without touching the device, seek an authentic exact ak_20221018 image for a separately scoped offline service/account-policy investigation. No message was sent and no download/extraction started. Request supported SSH/ams_cli account guidance rather than guessing credentials. Plaintext Telnet/FTP authentication remains unattempted.

Stop after Phase 3B. This is a recommendation, not a started firmware/hardware phase.

## Preserved earlier readiness assessment

## Current next objective after authentication failure

Phase 3 now has a bounded observed outcome: TOFU explicitly approved for the exact RSA fingerprint; strict saved-key verification succeeded; a single password-method attempt ended Permission denied. Server methods are publickey,password. No shell/root identity or Linux runtime is known.

Do not retry credentials, switch usernames or transmit reusable passwords over Telnet. Seek D-Link/Telkom documentation for the supported SSH account and management CLI on this exact build. The [Telkom support index](https://online.telkom.wds.co/device/D-Link_DSL-G2562DG/Telkom_Mobile/en) exposes web/setup guides, but the checked searches did not establish SSH account mapping. The previously inspected vendor-authored datasheet advertises SSH capability, not exact-build account policy.

If supported-account documentation cannot resolve this, offline analysis is a sensible separately scoped Phase 4 objective: acquire an authentic exact `ak_20221018` image, record provenance and hashes, and inspect account/service startup policy without running firmware or modifying the router. An older aj/al image may mislead. Exact-image acquisition, extraction and analysis have not begun. No privilege escalation, persistence, firmware upload, reboot or hardware work authorized or performed.

The only local persistent change was the user-approved public host-key entry. No router configuration or storage change was made. Diagnostic script remains prepared only.

## Historical pre-approval readiness snapshot (preserved)

**Not ready for escalation, firmware work, hardware access or persistence implementation.** The next objective is to resolve the current Phase 3 host-identity blocker and finish the single authorized SSH login, rather than assume shell/root access.

1. Independently verify the observed RSA host fingerprint from a previously trusted connection record or router-side information. Do not treat a fresh keyscan on the same LAN as verification.
2. With trusted identity established, use only the two demonstrated per-connection compatibility options and the known account; enter the password through a non-echoing interactive prompt. Limit to one credential attempt and stop on rejection.
3. If authentication succeeds, establish CLI versus POSIX shell before issuing Linux syntax. For a shell, run individual approved read-only identity/OS/mount commands with sensitive output filtered. Use numeric UID to decide root, never account naming.
4. If authentication fails, document the exact non-sensitive reason and seek vendor/ISP-supported account/CLI documentation. No account guesses, Telnet passwords or bypasses. Telnet authentication remains separately gated by plaintext-risk authorization.

The diagnostic script is ready for review, not authorization to upload it or implement persistence. No existing Linux ABI, filesystem, startup or reboot-persistence evidence supports choosing custom ARM binaries, modifying Dropbear, package installation or root-login changes.

The cryptographic mismatch is known and locally worked around. The unknown key remains unaccepted. An SSH/SHA-256 fingerprint is public identity metadata, not a private key. Passwords and private material should never be sent in chat or committed. Existing project credentials in the original user prompt were not reused in Phase 3; no new credentials collected.

Phase 3 remains resumable when independent fingerprint verification is available. Stop now; no Phase 4 action performed.
