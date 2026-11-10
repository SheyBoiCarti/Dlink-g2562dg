# Hypotheses needing device confirmation

- The user's firmware `ak` may share the ARMv7/VSPM3XX OpenWrt-derived build observed by a different owner. **Unverified**. [Report](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/)
- A local UART console may offer interactive access and perhaps root on the user's revision. **Unverified**. [Report](https://www.reddit.com/r/openwrt/comments/1fnicwy/openwrt_on_dlink_dslg2562dg/)
- The `OpenMarket` image may remove ISP defaults, but it could be older, incompatible or differently packaged. **Unverified; do not flash**. [Index](https://www.mmnt.net/db/0/0/ftp.d-link.co.za/DSL/DSL-G2562DG%20%28Telkom%29/firmware/Firmware%20for%20FTP)
- SSH or Telnet may be included but disabled; no evidence for the installed firmware yet.
- Root filesystem and overlay may be limited, immutable, or writable depending on variant and partitioning; must be measured rather than assumed.
