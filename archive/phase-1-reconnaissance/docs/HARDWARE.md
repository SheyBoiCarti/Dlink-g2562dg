# Hardware evidence

| Item | Finding | Status | Source |
|---|---|---|---|
| Product | D-Link DSL-G2562DG/TK, AC1200 dual-band ADSL2+/VDSL2 with VoIP | Vendor confirmed (product family) | [D-Link](https://www.d-link.co.za/product/dsl-g2562dg-tk/) |
| SoC | TriDuctor VSPM340 on DSL-G2562DG T1 | Community identification, not verified on owner's board | [Hardware forum](https://www.hwupgrade.it/forum/archive/index.php/t-2653735.html) |
| CPU ISA | `armv7l` | Another owner's shell output; firmware/board match unknown | [Reddit](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) |
| Kernel | `3.14.18` | Another owner's runtime observation; not owner's firmware | [Reddit](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) |
| RAM, flash capacities | Unknown | No reliable exact-board evidence collected | — |
| Wi-Fi chipset | Unknown | Do not transfer specifications from related D-Link models | — |
| Bootloader | Unknown | Need UART/firmware evidence | — |
| PCB revision | Unknown | Router UI field only says `G2562DG` | User device data |
| UART | User report of root shell via UART (June 2026 comment) | Unverified electrically and for owner's unit | [Reddit](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/) |

**Important**: A VSPM340 in another product does not establish this device's RAM, flash, radio, pinout, or bootloader. Do not attach a UART adapter without identifying 3.3V/1.8V logic, pinout and ground. Never connect adapter VCC blindly.
