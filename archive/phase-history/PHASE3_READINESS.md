> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 3 readiness and separate security recommendations

Recommended scope: **existing SSH/Telnet configuration and web administration**, with SSH first. Stop at the Phase 2 boundary now. Future shell authentication, command execution or hardware work needs a separately scoped Phase 3; none is performed here.

## Available evidence

LAN SSH/Dropbear, FTP/vsFTPd, Telnet negotiation and HTTP login directly observed. TCP 53/443 open, TLS handshake fails normally, 8080/8443 time out. Scripts, redacted measurement outputs, and bounded public research are available. All eight Phase 1 documents were reviewed.

## Unknowns that constrain further work

- Authenticated web inventory completed to the safely available extent; see [follow-up](../../findings/AUTHENTICATED_FOLLOWUP.md). Backup/restore/update controls exist, global ACL is unchecked, and CWMP is hidden by the project menu. SSH account mapping, WAN exposure and active provisioning remain unknown.
- No supported SSH account/CLI documentation established for exact `ak` build. No shell, root or Linux runtime confirmation.
- Exact installed firmware image, trustworthy hashes/signatures, flash layout and recovery mechanism not established. Older `aj`/`al` variants are not substitutes.
- UART board revision, pinout, voltage, settings and recovery remain unknown.
- WSL Ubuntu unavailable in this execution environment; Bash syntax/HTTP checks used Git Bash and Python instead. Windows LAN measurements are valid independently of WSL.

## Recovery evidence

[D-Link's product page](https://www.d-link.co.za/product/dsl-g2562dg-tk/) links firmware and datasheet downloads. Its download host could not be retrieved through the research tool; this does not prove the host is down for the owner. [Archive index](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/) lists Telkom `aj` images dated 2019/2020; an [OpenMarket subdirectory](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/Firmware%20for%20FTP) lists an `al` 2019 image. Index listings establish historical names, not present download success, authenticity or compatibility. No binary was downloaded. No verified bootloader/TFTP/recovery-button sequence located. Factory reset is not firmware recovery and was not attempted.

The vendor-authored datasheet advertises configuration upload/download; authenticated UI confirms backup and restore controls exist. Export and restore reliability remain untested. Configuration export remains prohibited without execution-time approval. If later approved, keep backups private outside version control and validate a supported restoration method before relying on them.

## Security concerns and safe recommendations (not applied)

1. The supplied administrator password matches a publicly documented factory default ([model login guidance](https://service.dsltelecom.co.za/portal/en/kb/articles/how-to-login-to-your-d-link-dsl-g2562dg-router)). The authorized follow-up web login succeeded, confirming that the supplied default credential is currently accepted. After this investigation, use the supported password UI to set a unique password, with ISP credential/recovery readiness first. No password value retained in generated Phase 2 files; the user-supplied prompt was preserved without copying it into the deliverables.
2. HTTP is plaintext; client-side SHA-256 does not make transport confidential. Use a trusted wired LAN for administration and investigate vendor-supported HTTPS compatibility without weakening system-wide TLS settings.
3. SSH, Telnet and FTP respond on this LAN. Restrict unnecessary services through documented controls in a later authorized change; no WAN exposure can be inferred from LAN listening ports. Telnet/FTP commonly lack transport confidentiality.
4. Dropbear/vsFTPd versions self-identify as old releases. Assess vendor support separately; banner age alone proves no particular vulnerability. Do not install arbitrary replacement packages or cross-flash firmware.
5. Check remote administration and CWMP settings read-only. TR-069 capability is documented for the family, but active provisioning is unknown. Coordinate with Telkom before later changes that might disrupt provisioning or service.

No security recommendation was automatically applied. No reboot, password change, provisioning disablement, service toggle, backup export or firmware update occurred.
