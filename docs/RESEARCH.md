# Verified research summary

These observations come from an owner-authorized investigation of one DSL-G2562DG on 2026-10-19. They distinguish reproduced behavior from portability assumptions.

| Property | Observed result |
| --- | --- |
| Firmware | `TK_1.00TK_V1.2.12ak_20221018` |
| Linux | 3.14.18, ARMv7 (`armv7l`) |
| Root identity | `uid=0(admin) gid=0(admin)` |
| Userland | BusyBox 1.19.4; stock Dropbear 2014.63 |
| Usable RAM | 105312 kB; no swap |
| Root filesystem | JFFS2 mounted read-only, 40 MiB |
| `/tmp` | RAM-backed tmpfs; lost at reboot |
| `/var` | Symlink to `/tmp/var`; volatile |
| `/data` | Writable 2 MiB JFFS2 vendor log partition; not used by this tool |
| OpenWrt metadata | `barrier_breaker`, `VSPM3XX/generic`; does not establish upstream OpenWrt support |

## Access sequence

On the trusted LAN, Telnet authentication with the existing management account `root` reaches `AMS#`. The CLI command `sh` enters Linux. `id` establishes effective UID 0 even though the Unix account label is `admin`. The management password is intentionally excluded. The web account and management account must not be assumed equivalent.

The original research identified the account in an older vendor firmware image and then verified it on the device. This export contains neither that password nor extracted firmware bytes. The recovered extraction code and verification instructions are now included; raw private observations remain outside the public copy.

## SSH implementation

Public-key authentication for UID 0 expects `/etc/dropbear/authorized_keys`, while the original root filesystem is read-only. The controller creates a scoped RAM tree, uses six private bind mounts to expose the required stock filesystem paths, and launches the existing Dropbear in that filesystem view. It verifies root identity and an interactive PTY over key-authenticated SSH before reporting success.

The original scripts and their duplicate packaged assets are preserved byte-for-byte. Internal phase names are retained because they are part of the established path/ownership contract. Tests verify that packaged and reference scripts match.

## Persistence and unresolved limits

The service itself is temporary. A signed-in Windows controller can reconstruct it after loss or reboot, subject to strict host-key verification. This is external restoration, not a persistent router startup modification. Host-key rotation was observed after a router restart. End-to-end WAN isolation, alternate firmware/hardware, UART pinout, voltage, and upstream firmware support are not established by this project.

## How the investigation worked

### 1. Finding a management account

Initial service discovery found SSH, Telnet, FTP, and the web interface, but open ports did not establish Linux access. Web credentials were not assumed valid for other services. SSH transport negotiation succeeded with scoped legacy algorithm exceptions, while the attempted web-account password login failed. Telnet exposed a vendor management CLI.

The account-discovery lead came from an older vendor-hosted image:

- Product page used during acquisition: [DSL-G2562DG Telkom](https://www.d-link.co.za/product/dsl-g2562dg-tk/).
- Historical [vendor image URL](http://ftp.d-link.co.za/DSL/DSL-G2562DG%20(Telkom)/firmware/DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin).
- Filename: `DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin`.
- Size: 24,272,267 bytes.
- SHA-256: `2f7cf1c4992f6521265480dbb78d4989a80bf090ff636a3081ce6f1e275ebbd7`.

These are recorded acquisition details, not a fresh check that the download remains available. The download used HTTP; the recorded digest identifies the analyzed artifact but does not establish a vendor signature. The older image was analyzed offline and never flashed to the router.

A custom Python parser reconstructed JFFS2 directory and inode data, supporting uncompressed, zlib, and RTIME data. The private report recorded 17,405 header-CRC-valid nodes and 3,627 reconstructed non-directory inode artifacts, with no recorded directory/inode/data CRC or decompression/size failures. Extracted symlinks were retained as data instead of installed on Windows; no extracted executable was run.

The reconstructed `/usr/sbin/ams_cli` contained a built-in account table. In this exact artifact, the `root` account name starts at file offset `0x18864`, its password slot at `0x18a64`, and its prompt slot at `0x18c64`. These are artifact-specific investigation leads, not universal firmware offsets. Credential values are intentionally excluded from this repository. Live Telnet authentication and `sh -> id` established that the lead applied to the installed newer firmware; the static strings alone would not establish that.

**Extraction now reproduced:** the original inline parser was recovered from the investigation's local chat history. The [packaged offline extractor](../research/firmware/README.md) verifies the exact older image's size and digest before reconstructing it into a new private directory outside the repository. A fresh run reproduced all 17,405 node records and all 3,627 original artifacts byte-for-byte. Firmware bytes and literal credentials remain excluded. This validates extraction, not a fresh credential login on another device; the runtime controller still assumes an existing authorized management credential.

### 2. Explaining why stock SSH rejected the expected account

The vendor management CLI and Unix account database use different names. The management login is `root`, but the observed UID 0 Unix account is `admin`, home `/`, shell `/bin/sh`. Dropbear resolves Unix usernames; it does not authenticate against the CLI account table. Live account inspection and offline analysis of the running Dropbear also identified a vendor password override. Editing shadow files or trying the web password would not address that behavior.

The useful alternative was public-key authentication. Static analysis identified `/etc/dropbear/authorized_keys` as this build's UID 0 lookup path. Nonzero-UID accounts use a home-relative path. Merely placing a key in `/root/.ssh`, `/var/dropbear`, or `/data` would not satisfy the verified root-key lookup. Successful live RSA public-key authentication later confirmed the finding.

### 3. Working around the read-only filesystem

The mounted root filesystem made the required `/etc/dropbear` path unavailable for normal writes. Instead of remounting flash or replacing the global `/etc` view, a second Dropbear process was given its own root-directory view under `/tmp/dlink-phase6a/root`.

| Path in temporary root | Source or purpose |
| --- | --- |
| `/bin`, `/lib`, `/usr` | Bind existing programs and libraries |
| `/dev`, `/dev/pts` | Bind device nodes and PTY slave filesystem separately |
| `/var` | Bind existing RAM runtime files, including the host key |
| `/etc/passwd`, `/etc/group` | Symlinks to existing `/var/passwd` and `/var/group` |
| `/etc/dropbear/authorized_keys` | One dedicated client public key, mode 0600 |
| `/run`, `/tmp` | Private directories inside the RAM tree |

All six new bind targets are marked private. No additional `/proc` bind or generated account/shadow database was needed. Private client key bytes never go to the router. The exact launch command in the preserved script is:

```sh
chroot /tmp/dlink-phase6a/root /usr/sbin/dropbear \
  -F -E -r /var/dropbear/rsa_host_key \
  -p 10.0.0.2:2222 -s -j -k -P /run/dropbear.pid
```

`-F` keeps the daemon in the foreground, `-E` logs to stderr, `-r` selects the existing host key, `-p` selects the IPv4 address/port, `-s` disables password authentication, `-j` and `-k` disable local and remote forwarding, and `-P` chooses the PID file. The setup script redirects output into its owned RAM tree. This is the core mechanism, not a complete standalone setup command: directory creation, account/key setup, mount checks, ownership, and rollback must precede or surround it. Use the controller for the reproducible managed sequence.

### 4. Separating authentication from a usable terminal

Initial non-PTY sessions authenticated successfully and returned UID 0, while an automated interactive test exited without output. Controlled tests kept the same daemon and mounts and changed only client input handling. The failing session's PTY request had already been accepted; keeping the subprocess stdin pipe open made the terminal work. A second command also succeeded. No server-side PTY modification, device-node creation, or additional mount was necessary.

### 5. Turning the experiment into a controller

The final controller added pinned host identity, protected local credentials, ownership markers, transfer-byte verification, bounded Telnet command lengths, a single-instance lock, conservative listener/firewall checks, independent root/PTY verification, and scoped rollback. A live trial exposed two compatibility problems: real stock firewall syntax and overlong inline rollback input. The implemented controller handles its supported rule grammar and stages verified rollback scripts in bounded chunks instead of sending a long inline rollback command.

The validation sequence was restore, independent key/UID/PTY proof, status, repeated restore, rollback, and original-service verification. It was repeated after an owner-performed router restart and explicit acceptance of an independently verified changed host key. A foreground monitor and then an approved scheduled monitor were also tested. These observations support the device-specific result; they do not establish compatibility with other firmware or uninterrupted sessions during vendor service changes.

## Read the implementation

- [Router transport and provisioning](../automation/src/dlink_ssh_restore/router.py): Telnet framing, prerequisites, script staging, and remote ownership.
- [SSH checks](../automation/src/dlink_ssh_restore/ssh.py): scoped algorithms, pinned identity, client-key validation, root and PTY proof.
- [Policy validation](../automation/src/dlink_ssh_restore/security.py): listener, mount, and supported firewall analysis.
- [Restore orchestration](../automation/src/dlink_ssh_restore/restore.py): recovery and repeated restoration behavior.
- [Reference setup](../scripts/phase6a_setup.sh) and [reference rollback](../scripts/phase6a_rollback.sh): exact router-side mechanism.
- [Tests](../automation/tests): offline cases and explicitly opted-in live integration.
