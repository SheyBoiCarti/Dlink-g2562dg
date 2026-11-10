> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# UART research

## Later offline firmware evidence and network access

An official older `ak_20210420` image contains `ttyAMA0::respawn:-/bin/sh` in `/etc/inittab`. This is image-specific serial-shell evidence, not electrical verification or a claim about the installed build's UART settings. The same investigation obtained root through Telnet and the CLI's `sh` command, so physical UART access is unnecessary for that result. See [verified access report](../findings/ROOT_ACCESS_VERIFIED.md).

## Phase 4 update

See [hardware evidence](UART_HARDWARE.md), [safe access assessment](UART_ACCESS.md) and [Phase 4 results](../archive/phase-history/PHASE4_RESULTS.md). Fresh public research confirms a vendor-listed T1 revision but leaves the owner's PCB, pinout, electrical levels and serial settings unknown. Initial physical observation must be receive-only after measurement. No hardware action occurred. Earlier phase boundaries below are historical.

## Phase 3B update

The exact-model firsthand discussion was rechecked. Its UART root claim still provides no verified header pinout, measured logic voltage, baud rate, framing, bootloader identity or exact installed-build/board mapping. Exact-model searches for pinout/voltage/115200/GitHub did not establish these details. Neither 3.3 V nor 115200 is confirmed; they must not be presented as this router's settings. No board photograph was established as a validated electrical reference. Hardware fields in the web UI are not a PCB revision.

UART is now the strongest reported root-specific alternative after the bounded SSH attempt was denied and live Telnet identified an ams_cli login. It is a research lead, not a ready-to-wire procedure or proof UART is necessary. The exact next prerequisite is board-matched evidence from the reporting owner or vendor: pin-labeled photos, logic voltage measurement, serial settings, boot log and account/authentication behavior. No outreach was sent, enclosure opened, voltage measured, cable connected or bootloader accessed. See [ranked assessment](../findings/ACCESS_METHODS.md).

A future physical investigation requires separately authorized enclosure access, exact board identification, ground/logic-level verification, an appropriate adapter and recovery planning. Do not use RS-232 voltage levels or blindly connect adapter VCC. Power/reset, soldering and wiring are outside this phase. A console could be a restricted CLI or require credentials; root is not guaranteed.

## Preserved earlier UART research

The [firsthand DSL-G2562DG discussion](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) includes a follow-up claiming root access over UART while SSH/Telnet did not work for that owner's unit. The visible page labels it roughly four months before this investigation; Phase 1 dates it June 2026. Exact board revision, installed build, login behavior and method are not documented in the inspected account. That report differs from this unit, which responds to SSH and Telnet.

The vendor-authored model-family datasheet advertises a serial management CLI; see [SHELL_ACCESS](SHELL_ACCESS.md). Advertising serial management does not prove an accessible debug header, root prompt or bootloader console.

| Needed evidence | Research result |
|---|---|
| Exact-board internal photographs | No trustworthy pin-labeled photograph established in checked sources |
| Header location / pinout | Unknown; no transferable pinout from related models |
| Logic voltage | Unknown; do not assume 3.3 V or 1.8 V |
| Baud / framing / flow control | Unknown; no validated serial settings |
| Bootloader identity | Unknown |
| Boot interruption / recovery protocol | No exact-build recovery mechanism established |
| Console account / root policy | Single community claim only; not reproduced |
| Required access | Physical access and enclosure/PCB identification, outside Phase 2 |

Public searches covered exact model plus UART, pinout, serial, board and recovery terms; no reproducible, firmware-matched UART procedure was established. Missing evidence is not proof one does not exist. The hardware forum used in Phase 1 contains both Broadcom and TriDuctor attributions in its broader discussion; its T1 entry specifically says VSPM340. The owner's UI hardware identifier does not establish T1 PCB revision. [Forum](https://www.hwupgrade.it/forum/archive/index.php/t-2653735.html).

Future hardware research would need verified board photos, ground, voltage, TX/RX identification, suitable logic-level adapter, isolation from adapter VCC, and a recovery plan before any connection. Incorrect voltage or pin assignment can damage the router or host; opening may affect warranty. Reading a console is less reversible than network inspection if enclosure or soldering is required. These are prerequisites, not wiring instructions. No enclosure opening, electrical measurement, wiring, soldering, bootloader interaction or power cycling occurred.
