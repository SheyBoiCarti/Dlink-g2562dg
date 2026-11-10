# Firmware evidence

## Installed version
`TK_1.00TK_V1.2.12ak_20221018` (device web interface). The terminal date segment plausibly denotes 2022-10-18 but is not independently verified as a build timestamp.

## Public archive entries

| Filename | Listed size | Evidence |
|---|---:|---|
| `DSL-G2562DG_TK_1.00TK_V1.2.12aj_20190312-telkom-Image.bin` | 23.03 Mb (archive notation) | [D-Link FTP index mirror](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/) |
| `DSL-G2562DG_TK_1.00TK_V1.2.12aj_20200605_telkom-Image .bin` | 23.03 Mb | [D-Link FTP index mirror](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/) |
| `DSL-G2562DG_TK_1.00TK_V1.2.12aj_20200806_telkom-Image-all.bin` | 23.10 Mb | [D-Link FTP index mirror](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/) |
| `DSL-G2562DG_TK_1.00TK_V1.2.12al_OpenMarket_20190724-Image-all.bin` | 23.10 Mb | [OpenMarket folder](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/Firmware%20for%20FTP) |

The mirror is an index, **not proof the files are currently downloadable or authentic**. No binaries were downloaded, hashed, extracted or compared. The exact installed `ak` image was not located in the checked listings. `Image` vs `Image-all` semantics are unknown. Compatibility and signing requirements are unknown.

## Kernel and build lineage (reported, not verified on target)
A DSL-G2562DG user reported `Linux 3.14.18 ... armv7l` and `/etc/openwrt_release` declaring `OpenWrt`, `barrier_breaker`, `VSPM3XX/generic`. This does **not** establish availability of official OpenWrt releases or compatible package feeds. [Source](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/).

## Next evidence
Obtain a safe offline copy of the *exact* installed firmware if possible; record origin/size/SHA-256 before opening it. Never cross-flash an older variant based solely on matching model number.
