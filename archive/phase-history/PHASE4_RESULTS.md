> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 4 results: DSL-G2562DG UART investigation

Date: 2026-10-19. Firmware: `TK_1.00TK_V1.2.12ak_20221018`.

**UART is a plausible stock-shell route, but there is no verified ready-to-wire pinout or proof of a shell on this firmware.** The useful next action is board identification and passive electrical characterization, not connecting a presumed 3.3 V / 115200 adapter.

## Existing evidence read

The prompt's “Phase 13B” was interpreted as the existing Phases 1 through 3B: there is no file literally named Phase 13B. Read Phase 1 hardware, sources, confirmed findings and existing research; Phase 2/3 results; [Phase 3B results](PHASE3B_RESULTS.md); [Phase 4 readiness](PHASE4_READINESS.md); previous [UART research](../../docs/UART_RESEARCH.md); and authenticated identity findings. Historical results remain preserved. SSH authentication was denied, Telnet exposed ams_cli/LOGIN#, FTP metadata responded, and no root shell was established.

## Research outcomes

| Requested investigation | Result |
|---|---|
| PCB revision / SoC / photos | D-Link independently documents the T1 product revision; exact owner PCB remains unknown. VSPM340 is the leading community attribution. No trustworthy exact-board teardown photo established. See [hardware evidence and photo links](../../docs/UART_HARDWARE.md). |
| UART headers / test points | No validated designator, pad order or numbered pinout found. Candidate-search guidance is explicitly hypothetical. |
| Voltage / GND / TX / RX / baud | All remain physically unverified. No credible measurement found that permits assuming 3.3 V or 115200. |
| Bootloader / Linux console | Exact bootloader, console device, settings and authentication policy unknown. No matching boot transcript found. |
| Root reports | A firsthand [exact-model comment](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) claims UART root, but lacks reproduction details or firmware/board mapping. |
| Adapter / safe procedure | Conditional FTDI 1.8 V or 3.3 V examples, instrumentation requirements, ESD precautions and receive-only procedure documented in [UART_ACCESS.md](../../docs/UART_ACCESS.md). Selection waits for measurement. |
| Shell without firmware changes | Technically possible if the installed console already offers one; not demonstrated here. The report does not prove unmodified-firmware access. |

New stronger revision evidence: [D-Link SAP10204](https://supportannouncement.us.dlink.com/announcement/publication.aspx?name=SAP10204) lists DSL-G2562DG T1. This does not equate the owner's `G2562DG` UI field to T1 or identify PCB silkscreen.

## Research coverage and limitations

Actual web searches covered exact model plus UART, pinout, PCB, board, teardown, internal, serial, 115200, J1 and U-Boot; VSPM340 plus UART/bootloader; and an image search for the exact model plus PCB/teardown/UART. The exact-model Reddit thread and Hardware Upgrade archive were opened and searched. Vendor revision notices, the vendor-authored family datasheet, an FCC antenna document, manufacturer adapter specifications, Linux console documentation and instrument safety/threshold documentation were checked.

No exact-board annotated photo or reproducible electrical procedure emerged. Image results contained different router models, which were excluded. The FCC model-string hit is an antenna document, not a teardown. Some direct D-Link/FTDI page opens returned tool errors; indexed manufacturer extracts supplied the limited adapter claims and the prior family datasheet was separately available. Public-search coverage is not exhaustive, and failed/absent results do not prove no documentation exists. No matching firmware was acquired or analyzed, and no source claims were upgraded into local measurements.

## Most likely connection and exact handoff

Engineering inference: an internal logic-level UART debug connection is the most plausible interpretation of the published report. Its physical location and voltage are unknown. The initial topology, **only after measurement**, is two wires: verified board GND to adapter GND, verified board TX to voltage-compatible adapter RX. Keep VCC, adapter TX and all flow-control outputs physically disconnected.

Required equipment: magnification/camera, ESD bench protection, DMM, suitable scope/probe, secure insulated contacts, optional documented logic analyzer, and a USB-UART adapter selected for the measured I/O domain. A generic “3.3/5 V” module is not a justified purchase specification. Risks include ESD, adjacent-pad shorts, back-powering, wrong signal levels, ground currents, telephone/FXS voltages, enclosure damage and service interruption. Receive-only wiring reduces input-related risk but does not eliminate electrical risk.

Next physical steps are: photograph label and both PCB faces; establish unpowered ground; measure voltage and TX timing without injecting signals; choose compatible equipment; capture one uninterrupted normal boot receive-only. Full gates and stop conditions are in [the numbered procedure](../../docs/UART_ACCESS.md#exact-next-steps-measurement-first-receive-only). Lack of matching hardware evidence is the current blocker to a specific pin-number recommendation.

An alternative evidence request, if the owner later chooses to contact the reporter/vendor, should ask for PCB assembly/revision, oriented numbered photos, measured TX levels and RX tolerance, serial settings, full redacted normal boot log, exact firmware and whether root required authentication, boot interruption or any persistent change. No outreach was sent.

## Completion and boundaries

- Completed: review of prior evidence and fresh public hardware/UART research.
- Completed: source-linked hardware assessment with verified facts separated from hypotheses and unknowns.
- Completed: equipment selection criteria, passive procedure, ESD/electrical precautions and console interpretation.
- Completed: requested three documents and project navigation updates, checked for local-link integrity and unsafe assumed settings.

This completes the Phase 4 research deliverables, not electrical verification or shell acquisition. No router network connection, authentication attempt, enclosure opening, measurement, UART transmission, reset, bootloader interruption, firmware download/extraction, flash write or configuration change occurred in Phase 4. No Phase 5 work started. Stop here.
