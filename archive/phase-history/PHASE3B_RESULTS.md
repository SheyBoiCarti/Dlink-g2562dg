> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 3B — alternative access investigation

Date: 2026-10-19. Scope: safe local metadata tests, supported web inspection and exact-model public research only. Prior Phase 1–3 findings were read; the prompt's “Phase 13” was interpreted as Phases 1–3. Historical evidence preserved. No root or Linux shell established.

## New verified local observations

### Telnet: vendor management frontend, not a demonstrated Linux shell

TCP 23 was connected with a 2-second connection timeout and bounded 4–5-second receive windows. The client exchanged only Telnet option negotiation (declining optional terminal features); **no username, password, newline, help command or shell input was sent**. The meaningful printable banner was:

```text
welcome to D-Link ams_cli system
LOGIN#
```

The initial automated login detector looked for `login:`/`username:` and therefore missed `LOGIN#`; direct sanitized banner inspection resolves that limitation. The frontend identifies itself as D-Link ams_cli and presents a management login prompt. It is not an unsolicited root shell. Post-authentication command set, restrictions, Linux-shell availability and account mapping remain unknown; no credential guess or CLI bypass was attempted.

### FTP: metadata exposed, filesystem access requires authentication

One connection to TCP 21; no USER or PASS command sent. No anonymous login, data connection, file listing, download, upload, SITE command or working-directory change.

| Exchange | Observed reply |
|---|---|
| Greeting | 220; vsFTPd 3.0.2 |
| FEAT | 211; EPRT, EPSV, MDTM, PASV, REST STREAM, SIZE, TVFS, UTF8 |
| SYST | 530; authentication required |
| PWD | 530; authentication required |
| HELP | 530; reply refers to USER/PASS |
| QUIT | 221 |

FEAT did not advertise AUTH TLS. This is not proof that TLS is impossible; explicit TLS negotiation was not attempted. No reusable credentials were transmitted over FTP. TVFS is protocol capability, not proof of access to the router's root filesystem. vsFTPd's greeting/version does not establish its account database, chroot policy, storage root or exploitable state. No legitimate filesystem access has been demonstrated.

## Web investigation status

Prior authenticated findings remain directly applicable: password-management page exposes no SSH account mapping; Service Control lists enabled LAN service rules with global ACL unchecked; xDSL debug tool is disabled; no general shell console found; CWMP is deliberately hidden by a project menu override. Those controls were not changed and hidden-page authorization was not bypassed. See [web investigation](../../docs/WEB_INTERFACE.md) and [authenticated follow-up](../../findings/AUTHENTICATED_FOLLOWUP.md).

After the user requested reopening the secure dialog, fresh web authentication succeeded. The first helper stopped at the normal `/page/login/login_succ.html` JavaScript redirect; that was a helper limitation, not evidence of password rejection. Corrected normal redirect handling reached `/index.html` and the known protected menu pages. Password entry used the local Git for Windows dialog; no credential came from arguments, environment variables, project files or chat.

| Fresh authenticated page | Observed read-only structure |
|---|---|
| FTP Server | Enable control and USB partition selector; generated code references `InternetGatewayDevice.Services.ServiceFTP.Enable` and `.RootDIR`. No root directory value or account secret retained. |
| Storage Device Info | USB/partition inventory page and table functions exist. Device identifiers, storage labels and path values not retained; attached-storage availability not established from this inspection. |
| Account Passwords | Account selector and old/new/confirm password inputs; no SSH role or Linux-shell option established. Field values not read or submitted. |
| Ping | Host, repetitions, timeout, packet size, protocol and WAN-interface controls; standard `IPPingDiagnostics` fields. No general shell/command field observed. |
| Traceroute | Host, maximum hops, wait time and WAN-interface controls; standard `TraceRouteDiagnostics` fields. No general shell/command field observed. |
| xDSL Diagnostics | Debug-enable control; no toggle or submission. |

All inspected forms targeted the existing `/cgi-bin/setup.cgi` settings mechanism and were not submitted. Unlike the earlier menu-click limitation, ping/traceroute page sources were now successfully retrieved through their previously observed normal menu URLs. No diagnostic ran and no hidden page was accessed.

This was passive authenticated HTML/JavaScript inspection, not execution of the pages' initialization scripts. Raw checkbox defaults therefore were **not** treated as current enabled/disabled state. The live FTP listener remains the direct evidence of a running service. Storage-oriented UI controls support a legitimate USB-share use case, but do not prove FTP access to rootfs or the account needed for any namespace.

The normal logout endpoint was requested at the end. No new web credentials, hashes, cookies or session values were saved. The prior authenticated findings remain separately attributed. No further password dialog remains open.

## Exact-model research

The [firsthand DSL-G2562DG thread](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) was rechecked. Its original owner reports Linux 3.14.18, armv7l and OpenWrt Barrier Breaker / VSPM3XX release metadata after an unspecified shell-access method. A later comment claims UART root access but does not give a pinout, settings, board match or exact firmware. Another comment reports a boot loop after replacing a libc package. None supplies a safe reproducible method for this installed `ak_20221018` build. No loophole or package modification was attempted.

Exact-model searches for UART/pinout/serial voltage/115200 and GitHub did not establish electrical details. An ams_cli-titled GitHub issue in an unrelated Etcher project had no model text or shell proof; it was not used as a procedure. The OpenWrt forum could not be accessed through the research tool due to robots restrictions. Absence of findings is not proof no documentation exists.

The [vendor-authored model datasheet](https://manuals.plus/m/d745f4d824163fb2303674b703b3fd7c3b9c74e5c84b3ad583acf833a2d4958b.pdf) advertises serial/Telnet/SSH management and configuration upload/download. It establishes family capability, not a root account, public debug pinout or account mapping for this ISP firmware. [D-Link product page](https://www.d-link.co.za/product/dsl-g2562dg-tk/).

## Ranked methods and exact next step

See the current [ranked access assessment](../../findings/ACCESS_METHODS.md). **UART is the strongest published root-specific lead, with low confidence for this exact unit and insufficient electrical information to connect safely.** Existing SSH/Telnet management is the safest supported access route if D-Link/Telkom can establish the account/CLI policy; it is not evidence of root.

The exact next root-specific research step is to obtain the reporting owner's or vendor's board-revision-matched console evidence: pin-labeled photographs, measured logic voltage, baud/framing, boot log and whether access required authentication or bootloader changes. The relevant firsthand report is the UART comment in the linked thread. Do not substitute a related D-Link pinout or assume 3.3 V / 115200 baud. No message was sent to anybody and no hardware interaction performed.

For immediately useful low-risk technical progress, acquire the exact `TK_1.00TK_V1.2.12ak_20221018` firmware from D-Link/Telkom and record provenance/hash before separately scoped offline inspection of ams_cli/login/Dropbear startup policy. Older aj/al listings do not prove compatibility or explain this build. No firmware was downloaded, extracted, executed or flashed in Phase 3B.

No root path is verified. Phase 3B stops after the bounded permitted investigation; no authentication guessing, exploit, configuration change, shell escape, service enablement, firmware action, reboot or UART wiring.
