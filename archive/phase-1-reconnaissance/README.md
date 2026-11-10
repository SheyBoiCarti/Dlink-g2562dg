# D-Link DSL-G2562DG — Phase 1 research

Research date: 2026-10-19. Scope: passive public-source research; **no router access, firmware downloads, binary analysis, or changes performed**.

Target as reported by device UI: DSL-G2562DG; hardware version field `G2562DG` (not a confirmed PCB revision); installed software `TK_1.00TK_V1.2.12ak_20221018`; management address `10.0.0.2`. Credentials are intentionally not stored here.

## Key result
A public account describes DSL-G2562DG shell access and reports Linux 3.14.18 on ARMv7, with an `OpenWrt`-labeled `VSPM3XX/generic` release file. A subsequent comment claims UART root access. **Neither account verifies the user's exact 2022 firmware build.** See docs/EXISTING_RESEARCH.md and raw-evidence/HYPOTHESES.md.

## Files
- `docs/HARDWARE.md`: hardware evidence and uncertainties
- `docs/FIRMWARE.md`: listed stock firmware variants and unresolved acquisition
- `docs/EXISTING_RESEARCH.md`: community discoveries and caveats
- `docs/SOURCES.md`: source links
- `raw-evidence/CONFIRMED.md`: direct evidence and bounded claims
- `raw-evidence/HYPOTHESES.md`: possible technical paths, unverified
- `raw-evidence/UNKNOWNS.md`: evidence needed for phase 2

No root access method has been tested or confirmed for the installed build. No download compatibility is implied.
