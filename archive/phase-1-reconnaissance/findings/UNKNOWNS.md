# Unknowns and phase 2 data plan

## Missing facts
- Physical board/PCB revision and actual SoC marking
- Installed kernel/architecture, bootloader, RAM, flash and partition map
- Management services running on trusted LAN
- Whether CLI access exists or may be enabled through supported options
- Complete configuration backup/restore capability
- Exact `ak` firmware binary availability and signature structure
- UART header pinout, voltage, and recovery workflow
- Official OpenWrt support / GPL source release for exact build

## Proposed Phase 2 (not executed)
1. Save a local configuration backup through the official UI, if supported; keep it private as it may contain secrets.
2. Take redacted screenshots of Status, Management, Diagnostics and Remote Management pages.
3. From a PC on the owner's LAN only, check TCP 22, 23, 80 and 443 with `Test-NetConnection 10.0.0.2 -Port <PORT>` (one port at a time). Do not scan the public WAN.
4. Report only status, no raw configuration files with credentials.
5. Separately identify physical H/W revision from sticker with serial/MAC obscured.

Stop before sending state-changing requests, physical UART connections, reboots or flashing.
