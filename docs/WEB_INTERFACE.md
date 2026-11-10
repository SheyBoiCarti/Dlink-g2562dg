> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Web interface investigation

## Phase 3B follow-up

Earlier authenticated observations below remain the evidence for account permissions, diagnostics and hidden-menu rules. Fresh Phase 3B browser state showed the login form. A secure local web-password dialog was offered for read-only FTP/storage/diagnostic inspection; its final outcome is recorded in [PHASE3B_RESULTS](../archive/phase-history/PHASE3B_RESULTS.md). No saved password, stale session value or speculative privileged API was used. The hidden CWMP page was not opened or unhidden; its existence is not a root-access method.

### Completed fresh Phase 3B inspection

Secure local password entry and normal login redirect handling reached the authenticated UI. FTP Server exposes a USB-partition selector and `ServiceFTP.RootDIR` setting name; no path value, credential or account data retained. Storage Device Info exposes USB inventory. The password page provides password-change controls without an established SSH/shell role mapping. Ping/traceroute page sources now load normally via their already observed menu URLs, resolving the earlier menu-navigation limitation; controls reference standard IPPingDiagnostics/TraceRouteDiagnostics parameters, not a general shell console. No forms were submitted, diagnostics run, debug toggles changed or hidden pages opened. Normal logout endpoint requested at completion.

These fresh sources were inspected without running initialization JavaScript, so raw checkbox defaults are not evidence of current service state. See [full fresh observations](../archive/phase-history/PHASE3B_RESULTS.md).

## Preserved authenticated UI findings

Authenticated read-only follow-up succeeded on 2026-10-19 after the user explicitly requested continuation. The sign-in blocker is resolved. See [authenticated findings](../findings/AUTHENTICATED_FOLLOWUP.md) for detailed evidence.

Frontend: HTML and custom JavaScript with jQuery 1.10.2. HTTP redirects to `/page/login/login.html`; the normal login handler hashes the password with SHA-256 and submits POST `/`. Successful authentication loads `/index.html`, `/menu.shtml` and `/page/status/status_info.shtml`. No credentials, hashes or session values were printed or saved. No other form was submitted. Client hashing does not encrypt HTTP transport. No browser cookies observed after login; session association and expiration remain unknown.

| Area | Actual observation |
|---|---|
| Device information | Model, hardware field and exact firmware confirmed; no displayed kernel/ISA identified. |
| Advanced menus | WAN/LAN/wireless, NAT, security, routing, QoS and tunnels present; no edits. |
| Account management | Password-change UI with one selectable web account; no SSH account mapping. |
| Service Control | SSH/Telnet LAN IPv4 ACCEPT rows enabled; global ACL Enable unchecked. WAN restrictions unknown. |
| Firmware update | ISP image upload control; page warns of update-triggered reboot. No upload. |
| Backup / restore | Configuration backup and settings-file restore controls present. No export or upload. |
| Diagnostics | xDSL debug checkbox unchecked; ping/traceroute menu selection did not replace the content frame. No tests executed. |
| Logs | Logging enabled, remote log server disabled. Displayed view yielded no kernel/BusyBox/OpenWrt metadata. No downloads or clearing. |
| TR-069 | CWMP entry in source deliberately hidden by project menu customization. Hidden page not opened; provisioning state unknown. |
| Console | No general system console found in inspected normal navigation. |

Menu code skips entries when `userlevel > pagelevel`. Current level is administrator (1); project customization sets CWMP to hidden (0). No visibility override or direct request to that hidden page occurred. A referenced endpoint does not establish backend authorization or active provisioning.

Normal forms reference POST `/cgi-bin/setup.cgi` for settings and POST `/cgi-bin/main.cgi` for uploads. Neither was invoked. These are frontend request targets, not verified public APIs. Web server identity remains unknown. No Save, Apply, reboot, reset, restore, export, upload, service toggle or password change occurred. Raw requests, HAR files and configuration/session dumps were not retained.
