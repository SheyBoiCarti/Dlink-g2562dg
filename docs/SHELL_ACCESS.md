> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Existing shell service assessment

**Strongest result: SSH is already listening on TCP 22 and identifies as Dropbear 2014.63.** Telnet negotiation is also reachable on TCP 23. Neither was authenticated. No successful login, Linux console, command execution or root privilege established.

| Question | Finding |
|---|---|
| SSH reachable / identifies itself? | Yes, from this Ethernet LAN host; SSH 2.0 identification and Dropbear version observed. |
| SSH enabled by default? | Unknown. Current availability is not factory-default evidence. |
| SSH supported enablement? | Model datasheet advertises SSH CLI; installed Service Control confirms port 22 and an enabled LAN ACCEPT row, with global ACL unchecked. No enablement change needed. |
| Telnet responds? | Yes, Telnet IAC negotiation received; no negotiation replies or login attempts sent. |
| Telnet restricted to LAN? | LAN reachability confirmed; exclusivity and WAN ACLs unknown. No WAN probing. |
| Telnet supported enablement? | Installed Service Control confirms Telnet port 23 and an enabled LAN ACCEPT row; account policy unknown. |
| Web console / diagnostics? | Authenticated maintenance pages inspected; xDSL debug tool disabled. No general system console found in inspected navigation. |
| UART required? | No evidence it is required. Working SSH listener makes software management investigation the first choice. |

The vendor-authored [DSL-G2562DG A1 datasheet](https://downloads.d-link.co.za/DSL/DSL-G2562DG%20(Telkom)/datasheet/DSL-G2562DG_A1_Datasheet(HQ)-v2.pdf), available through the vendor product page and a [PDF mirror](https://manuals.plus/m/d745f4d824163fb2303674b703b3fd7c3b9c74e5c84b3ad583acf833a2d4958b.pdf), advertises command-line management over serial, Telnet and SSH, TR-069, and PSI configuration upload/download. The document's A1 naming and generic product specifications do not verify T1 hardware or feature enablement in this ISP build. This is vendor-authored capability evidence, not proof of Linux shell entitlement or a root account.

Recommended Phase 3 focus: establish the installed firmware's supported SSH account and CLI behavior through read-only web settings and vendor/ISP documentation. A restricted vendor CLI may be the intended outcome of SSH authentication. Do not assume web credentials work for SSH, that root is enabled, or that old firmware reports imply an exploit is necessary. No password lists, anonymous FTP login, root guesses, legacy cipher changes or additional service probes performed.

Access rankings, risks and reversibility are in [ACCESS_METHODS](../findings/ACCESS_METHODS.md). UART remains a fallback research lead, not the recommended first action.
