> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 4: UART hardware evidence

Research date: 2026-10-19. Target: DSL-G2562DG, installed `TK_1.00TK_V1.2.12ak_20221018`. Public research only; no physical measurements or hardware access occurred. Read alongside [access procedure](UART_ACCESS.md) and [results](../archive/phase-history/PHASE4_RESULTS.md).

## Identity and evidence quality

| Item | Evidence | Conclusion for this unit |
|---|---|---|
| Model/build | Existing authenticated [Device Information findings](../findings/AUTHENTICATED_FOLLOWUP.md) | Exact model/build confirmed previously |
| UI hardware field | `G2562DG`, in the same findings | Model-like field; does not establish PCB revision |
| Product hardware revision | D-Link's [SAP10204 notice](https://supportannouncement.us.dlink.com/announcement/publication.aspx?name=SAP10204) explicitly lists DSL-G2562DG T1 | T1 exists; owner's label and PCB still need inspection |
| Exact PCB assembly / revision | No owner board photos or readable silkscreen available | Unknown; T1 product revision is not a PCB assembly number |
| SoC | [Hardware Upgrade discussion](https://www.hwupgrade.it/forum/archive/index.php/t-2653735.html), entry beginning “DSL-G2562DG T1 (Telkom Sud Africa)”, attributes VSPM340 | TriDuctor VSPM340 is the leading community attribution, not chip-marking verification; no independent vendor confirmation located |
| Architecture/platform | [Firsthand owner discussion](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) reports ARMv7 and VSPM3XX metadata | Supports a platform hypothesis, not a board match |
| RAM / flash | No exact-board evidence located | Unknown; do not import capacities from DVA-2800 or DSL-2888A |

The model-family [vendor-authored datasheet](https://manuals.plus/m/d745f4d824163fb2303674b703b3fd7c3b9c74e5c84b3ad583acf833a2d4958b.pdf) advertises serial management. It does not specify a debug connector or root policy. Its A1 filename also makes it unsuitable as a T1 wiring reference.

## Photographs and rejected matches

No trustworthy exact-model internal PCB photograph, annotated UART photograph, schematic or service-manual pinout was established in this search. Therefore there is no honest board-location diagram or numbered connection prescription to publish.

Useful available visual sources:

- [Vendor-authored datasheet photographs](https://manuals.plus/m/d745f4d824163fb2303674b703b3fd7c3b9c74e5c84b3ad583acf833a2d4958b.pdf): exterior product views only; no electrical reference.
- [DSL Telecom installation photographs](https://service.dsltelecom.co.za/portal/en/kb/articles/how-to-self-install-your-telkom-fibre-router): external ports only. These do not locate UART.

Search-result traps deliberately rejected:

- [FCC-hosted antenna specification, document 6352833](https://fcc.report/FCC-ID/2AR6UR3/6352833.pdf) contains DSL-G2562DG as a customer model in an antenna approval document. This is not an exact-model internal-photo exhibit or evidence of a UART pinout. Do not infer a matching router from the FCC URL.
- Image search returned an annotated **DIR-882** PCB and a **VMG3625-T50B** PCB. Neither is this model; their pad order is not transferable.
- Retail exterior photos and web-interface screenshots cannot establish chip identity, serial levels or PCB revision.

For future board documentation, photograph the underside model/H/W label with identifiers redacted, both PCB faces, full assembly/revision silkscreen, readable IC markings and close-ups of each candidate header. Use a fixed orientation (for example, Ethernet jacks at the top), a scale and numbered pads. Do not remove bonded heatsinks merely to obtain a chip name.

## UART location and possible assignments

**No verified header designator, test-point number, pad count, pitch or pin order is known.** In particular, there is no evidence that this board's UART is J1, JP1 or a four-pin row.

Engineering search hypotheses, not observations: inspect unpopulated small headers and test-pad groups for `UART`, `TX`, `RX`, `GND`, `CON` or debug labels. A three/four-pad group near the SoC or board edge is a candidate only. It could instead be JTAG, manufacturing test, power or another bus. Square pads indicate a numbering convention, not necessarily ground or VCC.

| Signal | Exact-board status | Evidence required before assigning it |
|---|---|---|
| GND | Unknown pad | Unpowered low-resistance continuity to independently established logic ground, corroborated at multiple points |
| Router TX | Unknown pad / voltage | Scope waveform referenced to verified ground; UART-like output decodes reproducibly |
| Router RX | Unknown pad / input tolerance | Board-matched documentation or circuit tracing to a positively identified UART input and its I/O domain; idle voltage alone is insufficient |
| VCC / rail | Unknown pad | Rail identification for documentation only; never connect to the adapter |
| Baud / framing / polarity | Unknown | Captured timing and consistent decoded frames; bootloader and Linux may differ |

No published measurements establish 3.3 V, 1.8 V or 5 V here. A DC reading cannot distinguish a supply from an idle TX or pulled-up RX. Do not apply a signal to discover RX.

## Measurement record to complete on the actual board

| Field | Current value |
|---|---|
| Label H/W revision / PCB assembly and revision | Not measured / photographed |
| Candidate connector and fixed photo orientation | Unidentified |
| Numbered GND pad and continuity references | Unmeasured |
| Each candidate's DC voltage | Unmeasured |
| TX low/high, overshoot, polarity and bit period | Unmeasured |
| Decoder settings, framing error count, capture file | Unavailable |
| RX circuit / voltage tolerance evidence | Unavailable |

The detailed equipment and electrical gates are in [UART_ACCESS.md](UART_ACCESS.md). This table must remain unfilled until evidence exists.
