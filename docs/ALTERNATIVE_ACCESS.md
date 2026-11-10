> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Alternative service evidence — Phase 3B

## Telnet

Verified banner: `welcome to D-Link ams_cli system`; prompt: `LOGIN#`. Only protocol negotiation sent, no application input or credentials. The visible management login is confirmed; whether an authorized account gets a restricted CLI or a Linux shell is **unverified**. The banner is not proof of root or a Linux OS version. Do not send a reusable password on Telnet without separately reviewing and authorizing plaintext-credential risk. No attempt to use help/login strings as guessed usernames.

## FTP

Verified vsFTPd 3.0.2 greeting and FEAT response. SYST/PWD/HELP return 530 before authentication. No filesystem root, readable files, account policy, anonymous access, chroot, write permissions or OS identity established. No FTP password or username sent. FTP is not a shell protocol; USB sharing or TVFS support cannot establish rootfs access. FEAT omits AUTH TLS; explicit secure negotiation remains untested.

Safe future authenticated assessment would need an authorized account, a suitable confidential transport or explicitly reviewed plaintext risk, and documented storage permissions. Only then could a read-only listing establish the presented namespace; even a listing named `/` could be a chroot, not Linux root. Do not use FTP to read credential databases or private keys, or to write configuration/startup files. No such access occurred.

## Web

The model-specific [Storage Setup Guide](https://manuals.plus/m/fa07c8bc70bb32605b10256f0c3e57d7f7d426a91e0b82d34c0f2e93d6086561.pdf) describes Samba sharing of attached storage, not the router root filesystem or an FTP root-access procedure. Its setup instructions would enable services; none were followed or recommended as a shell method. No SMB feature or service was enabled on the PC or router.

Normal management pages and shipped menu scripts were already inspected during Phase 2 follow-up. Supported xDSL debugging exists but is disabled; enabling it would be a configuration change. CWMP's client menu is hidden by a deliberate project override; that is not a shell interface or authorization to bypass backend permissions. Account/password UI does not expose a service-account mapping. No supported system console found in inspected navigation.

Fresh Phase 3B web authentication succeeded after secure local entry. FTP Server exposes a USB-partition selector and ServiceFTP.RootDIR setting; no actual storage root, credentials or permissions were retrieved. Ping/traceroute sources expose standard diagnostic parameters, not a general shell console. No settings submitted or diagnostic run; normal logout requested. Full outcome is tracked in [PHASE3B_RESULTS](../archive/phase-history/PHASE3B_RESULTS.md). Do not confuse prior authenticated evidence with a new session or claim that no UI feature can exist merely because it was not observed.

## Reproducibility and scope

Target hard-coded in performed probes: 10.0.0.2, TCP 23 and 21 only. Telnet: 2-second connect, bounded 4–5-second receive, at most 8 KiB, reply only IAC negotiation. FTP: 2-second socket timeout, commands FEAT/SYST/PWD/HELP/QUIT only, bounded replies. No data-channel connection, broader scan or user-authentication exchange. Meaningful sanitized replies are retained in [results](../archive/phase-history/PHASE3B_RESULTS.md) and [evidence journal](../findings/VERIFIED_COMMAND_OUTPUT.md). LAN access was available, so these are actual observations rather than suggested commands.
