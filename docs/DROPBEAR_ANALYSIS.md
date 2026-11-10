> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 5: live Dropbear and root authentication

## Phase 6B interactive update

The same RAM chroot now passed interactive UID 0 SSH. The controlled test reproduced the old failure with inherited client stdin, despite an accepted PTY request; maintaining an open stdin pipe fixed it even with TERM unset. No additional mount or server fix was needed. All temporary changes were rolled back. See [diagnostics and evidence](SSH_PTY_DIAGNOSTICS.md). Autonomous persistence and host identity across reboot remain unverified.

## Phase 6A verified runtime update

After explicit approval, a RAM-backed chroot supplied `/etc/dropbear/authorized_keys` to a separate IPv4-only, key-only Dropbear on `10.0.0.2:2222`. Two independent non-PTY SSH connections using RSA-3072 returned `uid=0(admin) gid=0(admin)`; client diagnostics explicitly confirmed public-key authentication. This verifies the vendor UID 0 key lookup and RSA/SHA-1 compatibility at runtime. A PTY check authenticated but returned no output and failed validation; its cause remains unresolved.

All temporary processes, mounts and files were removed. Original port 22 Dropbear, Telnet and host identity remain unchanged; a fresh Telnet login returned UID 0. The private client key remains off-router with user/SYSTEM ACLs, but **has no passphrase**. See [Phase 6A results and evidence](../archive/phase-history/PHASE6A_RESULTS.md). The remaining sections describe the historical Phase 5 baseline unless explicitly updated.

Date: 2026-10-19. This report combines live read-only inspection, a no-credential SSH negotiation, and offline disassembly of a copy of the **running** Dropbear executable. No login secret, password hash, private key or authorized-key contents are included. No authentication file or service setting was changed.

## Running service

| Item | Verified result |
|---|---|
| Version / executable | Dropbear 2014.63, `/usr/sbin/dropbear`, 154236 bytes |
| Current process | Root-owned daemon, parent PID 1; observed argv: `dropbear -r /var/dropbear/rsa_host_key -p 22` |
| Configuration owner | Vendor `sysmgr`, using `InternetGatewayDevice.Services.ServiceSSH.Enable` and `.Port`; current values 1 and 22 |
| Socket binding | `0.0.0.0:22` and `:::22`, not an explicit LAN binding |
| Advertised authentication | `publickey,password`, reconfirmed without sending a credential/key |
| Active flags | No `-s`, `-g`, `-w`, `-j`, `-k` or address-specific `-p` in observed argv |
| Host identity | RSA public fingerprint matches the previously saved host key; no trust-store change made |

The binary's own help confirms `-s` disables password authentication, `-g` disables passwords for UID 0, `-w` rejects UID 0 logins, `-j`/`-k` disable forwarding, `-p [address:]port` selects a listening address, and `-P` selects a PID file. These options were inspected in Phase 5; Phase 6A applied `-s`, `-j`, `-k`, address-specific `-p` and `-P` only to the temporary additional daemon. For root public-key access, do not use `-w`.

## Why Telnet root access did not translate to SSH

There are separate identity domains:

1. `ams_cli` accepts its built-in management account; `sh` inherits UID 0.
2. Unix `/etc/passwd` has two records, exactly one with UID 0: **`admin`**, GID 0, home `/`, shell `/bin/sh`. No Unix `root` record was found. `/etc/shadow` has a `root` placeholder, which does not create a passwd account.
3. Dropbear resolves names with `getpwnam`. For `admin`, vendor code replaces the password loaded from the account database with an embedded credential. Its password-authentication handler compares supplied plaintext length and bytes against this in-memory value; it does not perform the usual crypt-based verification on this path.

Consequently, neither the CLI login name nor a web password should be assumed valid for SSH. Changing `/etc/shadow` would not address this vendor override. No such change or new password attempt was made. The public-key account to target is **`admin@10.0.0.2`**, which already maps to UID 0.

These are findings from live account classifications and the actual daemon executable, not a conclusion based only on a version banner. The older official `ak_20210420` image's Dropbear is byte-identical to the running daemon, although other copied executables differ.

## Public-key authentication: exact vendor path

The executable includes a public-key verification path that bypasses its password comparison when a valid key signature is accepted. For **any UID 0 account**, including `admin`, it checks:

```text
/etc/dropbear
/etc/dropbear/authorized_keys
```

It opens `/etc/dropbear/authorized_keys` for the key scan. Nonzero-UID accounts use `$HOME/.ssh/authorized_keys`. Therefore `/.ssh/authorized_keys`, `/root/.ssh/authorized_keys` and `/var/dropbear/authorized_keys` are not the correct UID 0 locations for this build.

The permission-check code accepts owner UID 0 or the authenticated UID and rejects group/other write bits. Proposed conservative permissions are UID/GID 0, directory 0700 and file 0600. Parent directory ownership should also remain trusted. Current `/etc/dropbear` is absent, and `/etc` belongs to a read-only root filesystem. Simply copying a public key into `/data` or `/var` will not make this daemon use it.

RSA and DSA algorithm strings are present; RSA-SHA2, Ed25519 and ECDSA strings are absent. A dedicated **RSA 3072-bit** client key is the conservative candidate; its acceptance was verified in Phase 6A command sessions. Keep its private key passphrase-protected on the client. Do not generate or upload a private client key to the router. DSA is not recommended.

The permission and signature code is confirmed statically. End-to-end public-key authentication was subsequently verified under the approved RAM-only Phase 6A test; no key was installed for the original daemon. Options such as `no-port-forwarding`, `no-agent-forwarding`, `no-X11-forwarding` and `no-pty` have compiled strings; do not assume newer options such as `restrict` or `from=` are implemented. Use verified listener/firewall restrictions rather than an unverified authorized-key option.

## Host keys and boot behavior

`/var -> /tmp/var`, so `/var/dropbear/rsa_host_key` is in RAM. Its inspected mode is 0600, owner UID 0. Only public-key information was derived using `dropbearkey -y`; the private bytes were never returned or backed up in Phase 5.

The derived public fingerprint is:

```text
[PUBLIC_KEY_FINGERPRINT_1]
```

It matches the saved SSH identity. This is corroboration through the root console, whose Telnet transport itself is unencrypted; it is not a claim of a cryptographically independent hardware channel.

The live `sysmgr` initializer contains calls to create `/var/dropbear` and run `dropbearkey -t rsa -f /var/dropbear/rsa_host_key` before launch. Its update/stop paths use `killall dropbear`. No persistent host-key restore was established. The RAM path and initializer imply regeneration risk on reboot, but no reboot test was permitted. A stable host key must be explicitly addressed before declaring persistent trusted SSH.

## Client crypto compatibility

The no-credential probe negotiated DH group14/SHA-1, RSA/SHA-1 host signatures, AES128-CTR and HMAC-SHA1. Scoped `KexAlgorithms=+diffie-hellman-group14-sha1` and `HostKeyAlgorithms=+ssh-rsa` remain necessary with the installed modern OpenSSH client. An RSA user-key test will likely also need scoped `PubkeyAcceptedAlgorithms=+ssh-rsa`, because host-key and user-authentication signatures are separate. All three scoped overrides were exercised successfully with the Phase 6A RSA user key.

[OpenSSH's legacy guidance](https://www.openssh.org/legacy.html) supports per-host algorithm exceptions and distinguishes host authentication from user-key authentication. The [upstream 2014.63 public-key source](https://raw.githubusercontent.com/mkj/dropbear/DROPBEAR_2014.63/svr-authpubkey.c) describes home-based key lookup and permission checks, but **this vendor binary's UID 0 path differs**. Current Dropbear/OpenWrt instructions must not substitute for live behavior.

Key-only access improves credential handling but does not modernize this old SSH implementation. Do not describe it as suitable for Internet exposure. See [persistence proposal](SSH_PERSISTENCE.md) and [recovery](RECOVERY.md).

## Auditable binary evidence

[PHASE5_BINARY_ANALYSIS.json](../archive/raw-evidence/PHASE5_BINARY_ANALYSIS.json) records integrity digests and code addresses without credential literals:

- `0x10514–0x10648`: account resolution and admin override.
- `0x196a4–0x197b0`, helper `0x11488–0x114b8`: direct password length/byte comparison.
- `0x198f0–0x19920`, `0x199ac–0x199f0`: UID 0 authorized-key selection.
- `0x197c8–0x19844`: key-file permission checks.
- Live `sysmgr`, `0x13574–0x136a4`: vendor SSH lifecycle handling.

These were inspected using ordinary Python ELF parsing and Capstone already available on the PC. REA was not registered in the session; no configuration repair, engine installation, package installation or router binary execution was performed for this analysis.
