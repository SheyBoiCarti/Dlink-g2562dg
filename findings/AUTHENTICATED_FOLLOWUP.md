> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Authenticated read-only follow-up

Date: 2026-10-19. User explicitly requested continuation with the existing administrator account. Web login succeeded through the router's normal login form. Credentials were read in memory from the already supplied local prompt, without copying them into tool arguments, generated source, output, or artifacts. A temporary local-only browser document read that file; its network requests were blocked and it was closed before login. The file was not uploaded to the router. No backup/configuration export was performed.

## Direct findings

| Area | Observation |
|---|---|
| Identity | Authenticated Device Information confirms DSL-G2562DG, hardware field G2562DG, firmware `TK_1.00TK_V1.2.12ak_20221018`. Device identifiers were not retained here. |
| Service Control | `/page/management/mngt_srvctl.shtml` lists HTTP, TELNET, SSH, FTP, TFTP, ICMP, SAMBA and SNMP rows: LAN, IPv4, Any, Enable, ACCEPT. These rows do not prove every listed service runs. |
| Global ACL | `ACL Enable` unchecked. This prevents interpreting LAN rules as proof that WAN access is blocked. No WAN test performed. |
| Service ports | Page-generated JavaScript identifies SSH 22, Telnet 23, FTP 21 and TFTP 69. TFTP was not probed. Existing SSH/Telnet listener findings therefore agree with the installed UI's port configuration. |
| Account management | Password page offers one selectable web account, old/new/confirm password fields, Apply/refresh controls. No SSH-specific account, role or shell mapping exposed. No password fields inspected for values; no submission. |
| Backup | Settings > Backup describes saving router configuration to a PC. Backup button not clicked. |
| Configuration restore | Settings > Update offers a settings-file upload. No file selected or submitted. |
| Firmware update | Page instructs obtaining software from ISP and warns update takes about two minutes and reboots the router. No upload attempted. This is ordinary update functionality, not verified recovery. |
| xDSL diagnostics | Debug-tools enable checkbox unchecked; unchanged. No commands or diagnostics run. |
| Logging | Enable Log checked; Enable Log Server unchecked. Displayed Logs view contains no retained log entries or kernel/BusyBox/OpenWrt identifiers. No clear/download/upload/refresh operation invoked. |
| Ping / traceroute | Menu entries exist. Selecting them did not replace the content frame in this browser session; no diagnostic executed. No speculative endpoint request used to work around this. |
| Session | No browser cookies observed after successful login. Authentication clearly persists across normal page navigation, but its server-side association/token mechanism is not established. No session values inspected or manipulated. |

## Menu visibility and exposed request paths

Authenticated `/menu.shtml` loads `/js/menu.js` and `/js/project_menu.js`. The menu code skips entries when `userlevel > pagelevel`. Observed numeric levels: hidden 0, administrator 1, user 2; the current menu reports level 1. Default menu data marks CWMP as administrator level, but project customization sets `PAGE_LEVEL_mngt_cwmp = PAGE_LEVEL_HIDDEN`. The menu source references `page/management/mngt_cwmp.shtml`, yet the resulting navigation omits it.

This establishes an intentional client-side visibility rule, **not** an authorization flaw or proof that the page is accessible. The hidden page was not requested and visibility was not overridden. TR-069 enablement, ACS configuration, provisioning activity and privileges remain unknown.

Normal page forms reference POST `/cgi-bin/setup.cgi` (settings changes) and POST `/cgi-bin/main.cgi` (configuration/software uploads). These are observed frontend targets, not a verified public API. They were not invoked. Only the normal login form was submitted. No raw request payloads, cookies, hashes, HAR files or configuration dumps were saved.

## Access conclusion

The existing SSH listener remains the strongest candidate. No service enablement change is needed to establish reachability. The supported web UI does not establish which SSH accounts are accepted or whether they receive a restricted CLI, ordinary Linux shell or root. Successful web authentication must not be treated as successful SSH authentication.

The default web credential was accepted, strengthening the previously reported security concern. Its value is deliberately omitted. No password, ACL, service, provisioning or logging setting changed. No FTP/SSH/Telnet login or shell command attempted.

Next evidence should be vendor/ISP confirmation of the exact build's supported SSH account and command interface. Any later shell-login investigation must retain a separate scope from root access, escalation, firmware changes and UART. No evidence currently justifies UART as necessary.

The normal Logout control was used after inspection; the login form reappeared. The inspection session was not left signed in.
