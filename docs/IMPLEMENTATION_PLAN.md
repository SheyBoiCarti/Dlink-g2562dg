> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 2 implementation plan

Scope: the supplied phase2/prompt.txt is the specification. Preserve Phase 1. No exploitation, shell login, configuration changes, exports, or firmware downloads.

- [x] Read all eight Phase 1 documents (actual location: `phase 1/`).
- [x] Establish local connectivity and inspect unauthenticated login page.
- [x] Create fixed-target PowerShell and Bash/Python scripts with bounded TCP checks and safe HTTP summaries; test target rejection, syntax, and redaction.
- [x] Research exact-model CLI/UART and vendor recovery/firmware evidence.
- [x] Record actual network results and passive web findings, with authenticated inspection limited by secure interactive sign-in availability.
- [x] Rank access candidates and document Phase 3 readiness; verify all required artifacts.

Script design: hard-lock target to 10.0.0.2; sequential connections, 2-second connect/read limits, 200-ms spacing; only the eight requested TCP ports. Bash requires Python 3 standard library. HTTP inspection uses only root GETs, no credentials, proxies, redirects, or body output. Output header values are constrained; arbitrary banners and challenge values are withheld. Optional Nmap command is a connect scan without service probes or NSE scripts.

Verification: reject alternate targets before network activity; parse PowerShell and Bash; exercise HTTP response sanitization with a synthetic in-memory response containing cookies, tokens and redirect secrets; execute approved Windows checks once. WSL availability is reported separately from Git Bash verification.

Final verification: both offline tests pass; Bash syntax and PowerShell parser checks pass; all 11 requested artifacts exist and local Markdown links resolve. Windows TCP measurements and Git Bash/Python HTTP measurements are saved. Independent read-only review found no important issues; minor test portability and checklist issues addressed. Subsequent authorized web sign-in succeeded. Authenticated inventory and service-control observations are documented in findings/AUTHENTICATED_FOLLOWUP.md. SSH account mapping, Linux runtime, WAN exposure and CWMP state remain unknown. WSL execution remains unverified. Phase 2 ends here.

Follow-up completed: normal web authentication; model/build confirmation; service-control and account inventory; backup/update/logging/diagnostic inspection; static menu-rule inspection; report reconciliation and verification. No shell login, configuration change or hidden-page access.
