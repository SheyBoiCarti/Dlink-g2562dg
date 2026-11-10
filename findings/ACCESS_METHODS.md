> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Ranked access candidates

## Current Phase 3B ranking

This ranks evidential promise for eventual root, not confirmed access or permission to execute the next stage. No root path is verified.

| Rank / route | Evidence | Practical feasibility / required access | Risk / reversibility | Confidence and immediate next step |
|---|---|---|---|---|
| 1. UART console research | Exact-model owner claims UART root; vendor family serial CLI capability | Physical console later, but board match, pinout, voltage, baud and authentication unknown | Research low risk; incorrect future wiring can cause irreversible damage | Strongest root-specific report, low confidence for this unit. Obtain pin-labeled exact-board photos, measured voltage, settings and boot/login evidence from the report author/vendor before hardware work. |
| 2. Exact-firmware offline investigation | Live ams_cli frontend, Dropbear service, failed web-admin SSH attempt | Need legitimate exact ak_20221018 image and provenance; can inspect account/service policy offline in a later phase | No live-router changes; wrong-build conclusions remain a risk | Most useful low-risk technical next investigation if no supported account documentation. Obtain exact image; no extraction performed here. |
| 3. Supported SSH/Telnet management account | SSH offers publickey,password but attempt denied; Telnet banner ams_cli / LOGIN# | Service reachable; supported account and shell entitlement unknown | Read-only vendor inquiry low risk; Telnet/FTP reusable credentials would be plaintext | High service existence, unknown root availability. Seek firmware-specific account and documented CLI guidance, not alternate password guesses. |
| 4. Supported web diagnostics | xDSL debug disabled; normal account/service controls inspected; CWMP menu hidden | No general shell console observed; enabling debug exceeds read-only scope | Navigation reversible; toggles/bypasses prohibited | Low evidence of a root route. Inspect only normal supported read-only pages; no command injection or hidden-role override. |
| 5. FTP filesystem access | vsFTPd FEAT works; SYST/PWD/HELP require auth | USB-partition/root-directory controls observed in web UI; no authenticated FTP namespace or storage permissions established | Plaintext credential risk; no credentials or file transfers performed | No root evidence. Establish supported storage/account/transport policy first; a chroot or USB share is not rootfs. |

The strongest *root-specific* lead is UART; the safest *immediately useful technical research* is exact-build offline policy analysis after legitimate acquisition. Supported SSH account guidance remains a lower-risk route to ordinary management access, but its root entitlement is unknown. No email/forum message, hardware action, firmware download or extraction was performed.

See [Phase 3B results](../archive/phase-history/PHASE3B_RESULTS.md) and [alternative service details](../docs/ALTERNATIVE_ACCESS.md). The prior ranking below predates the denied SSH attempt and new Telnet/FTP observations.

## Historical Phase 2 ranking (preserved)

Ranking favors evidence and low-impact investigation, not likelihood of immediate root. No authenticated or root access confirmed.

| Rank / candidate | Evidence | Technical feasibility | Required access | Risk | Reversibility | Confidence |
|---|---|---|---|---|---|---|
| 1. Existing SSH service | Direct SSH 2.0 / Dropbear 2014.63 banner on 22; vendor family CLI advertised | Listener established; supported account, algorithms and shell type unknown | Trusted LAN plus documented account, later explicitly scoped session | Low for settings review; login may lock account or expose restricted CLI | Read-only review reversible; no setting changes needed | High listener; unknown authenticated shell/root |
| 2. Supported web administration | Direct HTTP login UI; vendor management docs | Service bindings inspected after sign-in; no SSH account mapping exposed | Interactive administrator web session | Low if read-only; accidental Apply or secret capture avoided | Reversible navigation | High authenticated inventory; unknown shell account mapping |
| 3. Existing Telnet service | Direct IAC negotiation on 23; vendor family CLI advertised | Service responds; supported account and CLI unknown | Trusted LAN plus documented account | Higher than SSH because credentials/data may travel in cleartext | Read-only inventory reversible; no login attempted | High Telnet negotiation; unknown authenticated shell/root |
| 4. Offline exact-firmware analysis | Vendor download link and older archive listings; exact ak file not established | Feasible only after legitimate exact-image acquisition and provenance verification | Correct binary and offline tools | Low to live router if strictly offline; wrong-image conclusions possible | Reversible offline analysis | Medium model-family availability; low exact-build availability |
| 5. UART investigation | Vendor serial CLI capability and one model-specific firsthand root claim | No verified pinout, voltage, board match or serial settings | Physical access, board identification and safe adapter | Medium/high hardware and recovery risk | Enclosure/solder damage may be irreversible | Low exact-device applicability |

FTP is an observed management/data service, not a shell-access candidate. Anonymous access, writing files and downloading router configuration were not tested. Exploits, firmware flashing and privilege escalation are outside scope and not ranked as Phase 2 options.

The safest realistic route is existing supported SSH management, using the completed [authenticated inventory](AUTHENTICATED_FOLLOWUP.md) and seeking vendor-supported SSH account documentation. UART is not currently justified as necessary. Linux userland access and root access are separate outcomes; an SSH banner establishes neither.
