> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 4: UART access assessment and safe observation

Research date: 2026-10-19. Target firmware: `TK_1.00TK_V1.2.12ak_20221018`. This is a conditional bench procedure, not a tested wiring recipe. No enclosure was opened, cable connected, reset issued or firmware modified during this investigation. [Hardware evidence](UART_HARDWARE.md).

## Can stock UART provide a shell?

Possibly, but it is unverified on this build. In the [exact-model firsthand thread](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/), ZebraHole claims UART root access while SSH/Telnet failed. That comment supplies no pinout, electrical measurements, settings, firmware version, boot log or authentication sequence. It does not establish whether boot interruption or firmware changes were involved. The original poster separately reports Linux 3.14.18, an August 2021 kernel build and Barrier Breaker/VSPM3XX metadata. Do not merge those two owners' observations into one reproducible procedure. Relative comment dates are not reliable absolute timestamps; this phase does not independently validate the earlier June 2026 attribution.

UART can bypass the need for an SSH service only if the installed software already exposes a usable console. Electrical access does not bypass console authentication by itself.

## Bootloader and Linux findings

No exact-model/build boot transcript or reliably identified bootloader was located. U-Boot, CFE, boot delay, password, recovery method, flash layout, console device name and Linux getty policy are all unknown. SoC-family resemblance does not establish them.

General Linux behavior: serial kernel output and an interactive login are separate facilities; seeing kernel logs does not prove a shell exists. The [kernel serial-console documentation](https://kernel.org/doc/html/next/admin-guide/serial-console.html) describes console selection and a separately started getty. Use it to interpret captured output, not to alter this router's configuration.

During a future receive-only capture, retain the bootloader banner/version if printed, natural autoboot countdown, kernel command line, serial-driver registration, init messages and final prompt. Record only what appears; do not send keys at a countdown. Keep raw logs private because boot output can contain identifiers or secrets, and redact before sharing.

| Passive observation | Meaning / next boundary |
|---|---|
| Bootloader output then normal boot | Serial TX works at those settings; let boot continue |
| Kernel logs but no prompt | Console output exists; no evidence of interactive access |
| `login:` | Authentication required; do not guess accounts/passwords |
| `LOGIN#` / ams_cli | Likely management frontend; not proof of POSIX shell |
| `#` or `$` prompt | Suggestive only; prompt characters do not establish shell or UID |
| Silence / gibberish | Could be wrong pad, levels, polarity, framing, baud or a disabled console; do not transmit to test |

Only after electrical RX verification and a separately deliberate interactive step, with Linux fully booted and an actual shell identified, would read-only `id` / `id -u` establish identity; UID 0 establishes root. Those commands were not run. Do not use shell escapes, change boot arguments, short pads, invoke recovery, edit init/login configuration or write flash. Even ordinary console authentication may create device logs; receive-only capture provides the strictest non-interference.

## Required equipment and adapter selection

- Magnifier, camera, nonconductive enclosure tools, stable board support and insulated fine probes or secured pogo fixtures. Avoid loose clips that can bridge pads.
- A high-impedance DMM for continuity with power removed and initial DC measurements; an oscilloscope with a suitable high-impedance probe for actual signal swing/timing. A DMM average is not a logic-level verification.
- A documented logic analyzer with input thresholds and absolute limits suitable for the **measured** waveform, if offline serial decoding is needed. For example, Saleae distinguishes [input thresholds from protection limits](https://www.saleae.com/support/specifications-hardware/electrical-characteristics/supported-voltages); its original Logic/Logic 4 cannot reliably decode 1.8 V logic. Confirm the exact instrument, not merely its brand.
- A genuine, documented USB-to-**logic-level UART** interface whose RX thresholds/absolute ratings match measured router TX. Never use a PC RS-232 port or USB-to-RS-232 cable on unverified logic pads. A module's power-output jumper does not prove its I/O voltage changes.
- ESD mat and wrist strap with the manufacturer's current-limiting ground lead, short insulated leads, and a logging terminal with flow control disabled. Consider suitable isolation if the grounding arrangement requires it; check isolation bandwidth and UART level compatibility.

Conditional adapter examples, not permission to connect:

| Established signal domain | Manufacturer-documented example |
|---|---|
| 1.8 V logic, compatible input specs confirmed | [FTDI TTL-232RG-VREG1V8-WE](https://ftdichip.com/products/ttl-232rg-vreg1v8-we/) |
| 3.3 V logic, compatible input specs confirmed | [FTDI TTL-232RG-VREG3V3-WE](https://ftdichip.com/products/ttl-232rg-vreg3v3-we/) |
| Other or uncertain levels | Defer purchase/connection; choose a documented compatible interface after measurement |

The [FTDI cable datasheet](https://ftdichip.com/Support/Documents/DataSheets/Cables/DS_TTL-232RG_CABLES.pdf) distinguishes 1.8 V and 3.3 V variants. Both provide power wires that must remain individually insulated and disconnected. Verify exact part number, wire functions and electrical limits against its datasheet; do not use wire colour from memory. A TX measurement establishes an output domain, not by itself the tolerance of an unidentified router RX input.

## Electrical and ESD precautions

Work only on the router's low-voltage board; never open the mains adapter. Disconnect DC power, DSL/telephone, FXS phones, Ethernet/WAN and USB accessories before opening or continuity testing. External telephone circuits and FXS ringing can present hazardous voltages. Leave them disconnected for bench observation. Allow stored charge to decay and verify absence of voltage before resistance tests.

Use ESD protection on a suitable bench, handle board edges, remove jewellery, avoid carpet and support the PCB clear of metal. Do not solder or reposition probes while powered. If a stable solderless contact is impossible, stop; soldering adds thermal/shorting risk and is not necessary for this research deliverable. Opening may damage clips or affect warranty.

USB interfaces and ordinary scope grounds can tie the board to PC/earth ground. Verify the grounding arrangement and potential difference before attaching grounds; never defeat protective earth or clip an earth-referenced scope ground onto an unknown pad. [Saleae's safety guidance](https://www.saleae.com/support/specifications-hardware/product-comparison-and-selection/safety-and-warranty) explains shared PC ground and ground-current risks. A battery laptop alone does not prove isolation. Stop on unexplained ground potentials, heating, resets, excessive loading or unstable contacts.

## Exact next steps: measurement first, receive only

These are future operator steps; no physical execution is claimed here.

1. Record underside H/W version, PCB assembly/revision and oriented photos as specified in [hardware evidence](UART_HARDWARE.md). Redact SSIDs, keys, MACs and serial numbers. Inspect candidate pad groups without assigning a pinout from another router.
2. With all power/cables removed and charge checked, establish logic ground from circuit evidence (for example a positively identified regulator ground and corroborating ground plane). Do not assume connector shields or DC-jack polarity equal logic ground. Check candidate GND continuity to multiple established references.
3. Arrange safe grounding, support and secure probes while unpowered. Use only the router's original known-good supply for a deliberate bench power-up after these checks. Never power it from UART. Measure candidate DC levels, then scope low/high swing, overshoot, idle polarity and data timing. Observe only; do not short pins or inject signals. If opening/power interruption is unsuitable for the current service, stop before this step.
4. Identify candidate TX by reproducible asynchronous serial output. Measure bit timing over multiple frames; estimate baud as `1 / bit_period`. Illustrations only: 8.68 microseconds corresponds to about 115200 baud, 17.36 to 57600, 26.04 to 38400, 104.17 to 9600. **None is verified for this router.** Try framing/polarity hypotheses on a saved capture rather than repeated boots. 8N1 is a decoding candidate, not a confirmed setting. [Serial framing reference](https://www.saleae.com/support/protocol-analyzers/learn-digital-protocols/learn-asynchronous-serial).
5. Select an adapter only after RX compatibility with measured TX is documented. Validate the adapter detached from the router; verify unused wires are insulated and no pull-up or protection path will back-power the target. Configure measured baud/framing, no hardware/software flow control, no macros, automatic newlines or BREAK on open. Physically leave adapter TX, VCC, RTS, DTR and every other wire disconnected. This physical separation prevents terminal input reaching the router.
6. With router power off, attach verified GND to adapter GND and verified router TX to adapter RX; no other connection. Ensure no pad bridging and account for the adapter's unpowered/powered input behavior. Power the adapter and then the router only in the sequence its documentation permits without back-powering. If uncertain, stop and resolve that electrical question.
7. Capture one ordinary uninterrupted boot if a planned service interruption is acceptable, then observe steady state. Do not press Enter, Space, Ctrl-C, BREAK or any other key, and do not touch Reset/WPS. Record framing changes between boot stages. Avoid automatic reboot loops or repeated power cycling.
8. Save the private capture and measurement table, then disconnect with power removed. Review what the installed console actually exposes. **Leave router RX unidentified/unconnected unless independent input-domain and pin evidence is obtained.** A later TX connection requires both that evidence and an explicit decision to move beyond passive observation; this Phase 4 stops at research.

Conditional connection topology, **not a board pinout**:

```text
Router verified logic GND -------- adapter GND
Router verified TX -------------- adapter RX  (compatible measured levels)
Router RX                         UNCONNECTED
All power rails / VCC             UNCONNECTED
Adapter TX / RTS / DTR / others   UNCONNECTED, insulated
Router power                      original supply only
```

Receive-only access cannot itself execute shell commands. An existing stock serial shell could permit later interaction without flashing, but this remains a hypothesis until a board-matched boot capture and login behavior establish it.
