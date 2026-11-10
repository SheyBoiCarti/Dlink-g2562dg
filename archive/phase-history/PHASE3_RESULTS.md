> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 3 results

## Current outcome: authentication denied after approved TOFU

The user explicitly approved TOFU for the exact observed RSA fingerprint. OpenSSH recorded that public key locally, and the next connection passed `StrictHostKeyChecking=yes`. This is user-approved first-use trust, not independent verification.

The single configured password-method authentication attempt used a secure local Git askpass dialog and ended with:

```text
admin@10.0.0.2: Permission denied (publickey,password).
```

No retry, alternate username, user-key attempt, Telnet authentication or authenticated router command followed. Dialog contents and cancellation status were deliberately not logged; the SSH result does not prove which secret was entered, that the account exists, or why the request was denied.

| Required result | Current verified status |
|---|---|
| Host-key trust | Explicitly approved TOFU; exact RSA key saved locally and matched under strict checking |
| SSH authentication | Single password-method attempt ended Permission denied |
| Server authentication methods | publickey,password |
| Requested account | admin |
| Authenticated username / effective UID | None established / unknown |
| Shell / restricted CLI | No authenticated session; unknown |
| Kernel / architecture / SoC | Unknown on exact device |
| Root filesystem / root access | Unknown / not confirmed |
| Persistence | Unknown; no changes or reboot |

The host-trust blocker is resolved by approval; account/authentication acceptance is now the blocker. Phase 3 ends with documented authentication failure (Outcome D). All runtime diagnostics remained conditional and were not run. The prepared script remains unchanged, unuploaded and unexecuted on the router.

Vendor/ISP search found no supported SSH account mapping for this exact firmware. The inspected web password page also did not establish one. Recommended Phase 4: request supported account/CLI documentation from D-Link/Telkom; if unavailable, plan strictly offline analysis of a provenance-checked exact firmware image. No extraction or other Phase 4 work performed.

## Historical first-run results (preserved)

2026-10-19. **SSH is reachable and legacy compatibility is resolved, but authentication is blocked by host-key verification. No password was sent and no shell or root access obtained.**

| Required result | Actual status |
|---|---|
| SSH login | Not attempted with credentials: strict host-key verification stopped it |
| Requested account | admin; acceptance untested |
| Authenticated username | Unknown |
| Effective UID | Unknown |
| Shell / restricted CLI | Unknown |
| Kernel / CPU architecture / SoC | Unknown on exact device |
| Root filesystem | Unknown |
| Root access | Not confirmed |
| Persistence / automatic startup | Unknown; no changes or reboot |

Two credential-free connections were made: default algorithms fail with no matching KEX; one retry adds `diffie-hellman-group14-sha1` and `ssh-rsa` per connection. That retry negotiates AES128-CTR / HMAC-SHA1 and receives the RSA fingerprint, then stops because it is not trusted locally. No system-wide settings or host trust records changed. [Exact command evidence](../../findings/VERIFIED_COMMAND_OUTPUT.md).

The observed public fingerprint is `[PUBLIC_KEY_FINGERPRINT_1]`. It is not independently verified. The user was asked for an independent comparison using a previously trusted client or router-side source. No verification was available during this run. Repeating network observations cannot supply that independent trust.

This is **not authentication rejection** and does not prove an invalid password, nonexistent account, disabled password auth, restricted CLI or unsupported SSH transport. Server user-authentication methods were not reached. No Telnet password transmitted and no fallback credential attempts.

The existing web inventory already found no supported SSH account mapping in the inspected account page; Service Control lists port 22 and LAN accept rules with global ACL unchecked. Hidden CWMP was not opened. Those historical findings are preserved. No new web sign-in was needed for the transport blocker.

All requested documents and [shell_diagnostics.sh](../../scripts/shell_diagnostics.sh) are prepared. Script requires full review and `--reviewed`, uses no credentials or authentication, writes no router files and filters identifiers, mount secrets and process arguments. It was **not uploaded or run on the router**. Offline tests verify the review gate and mount-secret filtering; Bash syntax checked. Existing Phase 2 tests remain passing.

**Remaining blocker:** independently establish the host key before the initial bounded interactive credential attempt. The authenticated objectives remain incomplete; the documented Phase 3 investigation ends at this trust boundary. [Authentication details](../../docs/SSH_AUTHENTICATION.md), [root assessment](../../docs/ROOT_ACCESS_ASSESSMENT.md), [Phase 4 readiness](PHASE4_READINESS.md).
