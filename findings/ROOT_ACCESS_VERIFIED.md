> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Root Linux access verified

Date: 2026-10-19. Target: owner's DSL-G2562DG at `10.0.0.2`, previously authenticated web firmware identity `TK_1.00TK_V1.2.12ak_20221018`.

**Root Linux access is now demonstrated.** A built-in account recovered from an official older firmware image authenticates to the running router's Telnet management console. Its `sh` command opens a Linux shell with effective UID 0. No password cracking, firmware flashing, configuration editing or bootloader interaction was required.

## Reproduced access sequence

1. Connect a Telnet client to `10.0.0.2`, TCP 23, from the owner's LAN.
2. At `LOGIN#`, use the firmware-derived built-in account `root`, with its recovered password. The password is omitted from project files; it was supplied directly to the owner in the final response. This is separate from the web `admin` account.
3. Successful authentication produces `AMS#`.
4. `help` lists `sh` with the description `entry linux shell.`
5. Enter `sh`; the prompt becomes `~ #`.
6. Run `id` and `uname -srm` to verify privileges and the operating system.

Actual read-only output:

```text
AMS# sh
~ # printf 'DLINK_LINUX_PROOF\n'; id; uname -srm
DLINK_LINUX_PROOF
uid=0(admin) gid=0(admin)
Linux 3.14.18 armv7l
~ # exit
AMS# exit
```

The CLI login name `root` and Linux account label `admin` differ. Numeric UID 0 is the decisive evidence of root privileges. Two separate successful logins were observed: first to inspect normal CLI help, then to enter the shell and collect proof. Both sessions were closed. The sanitized verification record is [LINUX_ACCESS_VERIFIED.json](../archive/raw-evidence/LINUX_ACCESS_VERIFIED.json).

Telnet carries credentials and shell traffic without encryption. Use this only on the trusted local connection; do not expose it to the Internet. SSH access was not established or changed. No additional router service was started, and no key or persistence mechanism was installed.

## How the account was found

The live official [D-Link product page](https://www.d-link.co.za/product/dsl-g2562dg-tk/) links the vendor's download service. Its [firmware directory](http://ftp.d-link.co.za/DSL/DSL-G2562DG%20(Telkom)/firmware/) exposes an `ak` build missing from the previously checked mirror listing:

```text
DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin
24,272,267 bytes
SHA-256: 2f7cf1c4992f6521265480dbb78d4989a80bf090ff636a3081ce6f1e275ebbd7
```

[Direct vendor image](http://ftp.d-link.co.za/DSL/DSL-G2562DG%20(Telkom)/firmware/DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin). Transport was HTTP, so vendor hosting and recorded hash establish the acquisition path and artifact identity, not a verified digital signature. The image predates the installed build and was used only offline.

Local firmware, provenance and extracted inode files are under:

```text
<WORKSPACE_OR_USER_HOME>\AppData\Local\DLinkResearch\firmware\
```

Ordinary Python parsing identified 17,405 JFFS2 nodes with valid header CRCs. Directory/inode/data CRC verification reported zero failures. Reconstructing uncompressed, zlib and RTIME nodes produced 3,627 non-directory inode artifacts without decompression/size errors; symlinks were retained as data rather than installed on Windows. `filesystem-manifest.json` maps original paths to inode artifacts. No extracted executable was run on the PC or uploaded to the router.

`/usr/sbin/ams_cli` contains a built-in account table. In this exact extracted binary, the `root` account string starts at file offset `0x18864`, its password slot starts at `0x18a64`, and its prompt slot starts at `0x18c64`. A separate `admin` table entry exists, explaining why equating web and CLI credentials was unjustified. Static strings were a lead; the successful live authentication and shell proof establish applicability to the owner's installed firmware.

The older image's `/etc/inittab` also contains:

```text
console::sysinit:-/etc/rc.d/rcS
ttyAMA0::respawn:-/bin/sh
```

This is new evidence for a stock serial-shell configuration in the **older image**, not proof of this unit's UART pinout, voltage or baud. UART is unnecessary for the demonstrated network access and was not physically investigated further.

## Other checks and corrected conclusions

- The known web credentials were tested against Telnet once and rejected with `The login info is not correct, please retry.` A preceding connection stopped at the password prompt without submitting a password.
- The same web credentials authenticated to FTP with status 230, but a directory listing was denied. FTP did not establish Linux filesystem or shell access.
- Deeper backup inspection found the `UserList.1` value is an alphabetic/underscore marker rather than an obvious hash or Base64 value. No usable Linux credential verifier was established from that export. The earlier report was accurate about the backup's limits, but it did not rule out firmware-derived credentials.
- REA's CLI doctor found no registered live REA server or native analysis engine. No client configuration was changed; the actual extraction and string/ELF inspection used ordinary Python tooling. These results are not represented as REA Evidence records.

The earlier Phase 1–4 documents remain historical. Their statements that no root route had been demonstrated have been superseded by the live proof here. The requested objective, obtaining verified root Linux access, is satisfied; no service changes, reboot, flash writes or further exploitation are necessary.
