> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 2 actual results

Investigated 2026-10-19. **Existing SSH is the most promising route: TCP 22 responds with SSH 2.0 and Dropbear 2014.63.** No SSH/Telnet login, shell, root access, exploitation, configuration change or hardware access attempted.

| TCP port | State | Service / evidence |
|---|---|---|
| 21 | Open | FTP 220 greeting; vsFTPd 3.0.2 self-identification |
| 22 | Open | SSH identification; Dropbear 2014.63 |
| 23 | Open | Telnet IAC negotiation received |
| 53 | Open | TCP connection only; DNS not identified or queried |
| 80 | Open | HTTP 302 to login; D-Link login page inspected |
| 443 | Open | TCP works; default TLS handshake fails |
| 8080 | Timeout | 2-second connect timeout; service unknown |
| 8443 | Timeout | 2-second connect timeout; service unknown |

These are measurements from the owner's Ethernet LAN host, not WAN tests. Timeouts are not proof of closed ports. Authentication and allowed accounts were not tested for FTP/SSH/Telnet. See [network details and raw sanitized evidence](../../docs/NETWORK_RECON.md).

## Linux environment

No kernel, CPU architecture, BusyBox version, filesystem layout or OpenWrt release identifier confirmed on the exact device. Live Dropbear/vsFTPd banners strengthen the embedded Unix-style environment hypothesis but do not prove ARMv7, Linux 3.14.18, VSPM340 or OpenWrt. Those remain attributed public reports. The installed firmware string was subsequently confirmed on the authenticated Device Information page. [Evidence matrix](../../docs/LINUX_ENVIRONMENT.md).

## Web interface

Observed D-Link Gateway login at `/page/login/login.html`, jQuery 1.10.2, custom JavaScript and SHA-256 transformation before login POST to `/`. Web server identity and authenticated session mechanism remain unknown. Authenticated follow-up succeeded through the normal login form. Service Control lists SSH/Telnet LAN accept rules, with global ACL Enable unchecked; WAN restrictions remain unverified. Project menu JavaScript hides CWMP. Backup, restore, firmware update, password and logging controls were inspected without submission. No shell account mapping established. See [authenticated findings](../../findings/AUTHENTICATED_FOLLOWUP.md). Credentials and session values were not placed in tool output or generated artifacts. [Inventory and limitations](../../docs/WEB_INTERFACE.md).

## Access and next step

Rank: existing SSH, supported web administration, existing Telnet, offline exact-image analysis, UART. Each method's evidence, feasibility, access requirements, risks, reversibility and confidence is in [ACCESS_METHODS](../../findings/ACCESS_METHODS.md). No root route confirmed. UART is a fallback community lead with no verified pinout or build match, not a demonstrated requirement.

**Recommend Phase 3 focus on supported SSH account/CLI configuration, starting with read-only authenticated web inspection.** Do not begin firmware extraction or UART wiring merely because earlier reports mention root. Exact-image acquisition and recovery research become alternatives if supported management cannot answer the questions. [Readiness, security concerns and recovery gaps](PHASE3_READINESS.md).

## Deliverables and verification

All three requested scripts and eight requested reports created, alongside README, implementation plan, offline safety tests and sanitized evidence. PowerShell script executed on the router; Bash syntax checked; HTTP script executed under Git Bash/Python. Alternate-target rejection and HTTP secret-redaction tests passed. Nmap absent; no installation attempted. WSL launcher did not provide an Ubuntu runtime; WSL execution is unverified, with exact owner commands in README.

The safely available Phase 2 work and subsequent authorized authenticated web inventory are delivered, with runtime/hardware and SSH account unknowns explicitly recorded. No fabricated results fill these gaps. Stop here; no Phase 3 activity performed.
