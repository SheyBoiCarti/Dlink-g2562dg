# Installation and operation

This guide describes the device-specific controller. Read the [project overview](../README.md) and [security notes](../docs/SECURITY.md) before connecting. Internal Phase 6/8 names identify the preserved, tested scripts and ownership markers; they are not separate installation steps.

## Install locally

From this repository's `automation` folder, use Python 3.12 or later:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[test]'
.\.venv\Scripts\dlink-ssh.exe --help
```

Two runtime dependencies: Paramiko `>=4,<5` and keyring `>=25,<27`. The tested version range is pinned for compatibility with this legacy firmware. Only this device's transports enable the proven group14/SHA-1, ssh-rsa, AES128-CTR, HMAC-SHA1 combination. There is no global OpenSSH configuration change, password SSH fallback or agent-key search. Keep this compatibility environment isolated and review updates; this does not modernize Dropbear 2014.63.

Credentials explicitly use [keyring's Windows Credential Manager backend](https://github.com/jaraco/keyring/blob/main/keyring/backends/Windows.py). Plaintext/file backends are never selected. Offline tests do not read or write your real vault.

## Prepare a protected client key

Use a dedicated RSA key of at least 3072 bits, outside OneDrive. The application rejects unencrypted private keys. Create a dedicated protected key:

```powershell
New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\DLinkSSHRestore" | Out-Null
ssh-keygen -t rsa -b 3072 -a 100 -f "$env:LOCALAPPDATA\DLinkSSHRestore\id_rsa"
```

Enter a strong passphrase when prompted. Restrict private-key and application/config directory ACLs to your Windows account and SYSTEM; review inherited permissions before deployment. Do not put the private key, vault contents or configuration exports in this repository. Setup does not alter ACLs or generate keys automatically. Protect the application too: a process running as your Windows user can access that user's vault.

## Local interactive setup

```powershell
.\.venv\Scripts\dlink-ssh.exe setup
```

This command makes **no network connection**. Supply your PC's trusted Ethernet IPv4 address within `10.0.0.0/24`, the private/public key paths, an independently verified router public host fingerprint, the key passphrase, and the existing Telnet management password. The Telnet account is fixed to the verified `root`; SSH account is fixed to `admin`. Setup verifies the public/private key pair and encrypted private-key requirement before storing secrets.

The default non-secret configuration is `%LOCALAPPDATA%\DLinkSSHRestore\config.toml`. The vault namespace is `dlink-ssh-restore/<generated-owner-id>`, with entries `telnet-password` and `key-passphrase`. Never copy an installation/owner ID to another controller. Use one Windows PC/account/controller. The example TOML documents all configurable fields but is intentionally incomplete. A source address outside the trusted LAN, other device, username, unsafe owner ID, invalid fingerprint or unbounded timing value is rejected.

The owner ID is a resource identifier, not an authentication secret. Preserve it to retain cleanup ownership. A different owner or an old manual Phase 6 tree produces a conflict. Changing/recreating configuration does not authorize adoption of existing resources.

For a nondefault configuration, put the global option **before** the command:

```powershell
.\.venv\Scripts\dlink-ssh.exe --config 'C:\approved\config.toml' status
```

Setup refuses an existing configuration. For other settings, edit only the non-secret TOML deliberately. Vault secrets can be updated through Windows Credential Manager under the same owner namespace. Do not store passwords/passphrases in TOML, environment variables or command arguments.

## Trust and reboot behavior


Before sending Telnet credentials, the tool performs an SSH handshake against stock port 22 and compares the cryptographically presented public key with the configured fingerprint. It independently repeats that check immediately before Telnet authentication. Custom port 2222 is also pinned before public-key authentication. There is no automatic trust-on-first-use or known_hosts rewrite.

If identity changes, verify the new public key through your trusted recovery process first. For example, inspect only public output from `dropbearkey -y -f /var/dropbear/rsa_host_key` over the physically trusted recovery LAN and compute/compare its public fingerprint locally. A network scan alone is not independent verification. Telnet itself is unencrypted; it is not a cryptographic out-of-band channel. If you cannot establish trust, leave automation stopped.

After verification, this **local-only**, explicit command requires retyping the full fingerprint:

```powershell
.\.venv\Scripts\dlink-ssh.exe setup --update-trust
```

It preserves the owner ID, key paths and vault entries. It does not connect or restore SSH. Restart `watch`/the task explicitly afterward. Fully unattended restoration is possible only while the configured identity continues to match. The tool never writes/restores/generates a router host key to bypass this gate.

## Manual commands and effects

Only execute the following after approval for real-router RAM changes:

```powershell
.\.venv\Scripts\dlink-ssh.exe status
.\.venv\Scripts\dlink-ssh.exe restore
.\.venv\Scripts\dlink-ssh.exe rollback
```

`status` authenticates over Telnet to inspect ownership and network state. If owned resources are present, it also verifies actual SSH authentication, UID 0 and interactive PTY operation; inspection failure is not reported as ready. It does not provision or delete resources. `absent` is a successful inspection, not a successful restoration.

`restore` uses the following sequence:

1. Validate configuration and the protected RSA key pair locally. Bind all router connections to the configured trusted local IPv4 address. Reach stock SSH with a bounded TCP timeout; pin its key before Telnet secrets are sent.
2. Enter `LOGIN# -> PASS# -> AMS# -> sh`, suppress process-local shell history, confirm UID 0 and read the boot ID. No credential is extracted from firmware or hardcoded.
3. Refuse a foreign scratch tree, unknown port-2222 listener or orphan scratch mount. An already healthy owned setup is audited and SSH-verified without duplicate provisioning. If the owned listener disappeared, safely remove the owned remnants and rebuild.
4. Before writing, verify exact firmware/kernel, `/tmp` tmpfs, root JFFS2 ro, available RAM >=16 MiB, existing host key, absent global `/etc/dropbear`, original mount propagation, and the existing IPv4/IPv6 ingress policy. Missing/unsupported prerequisites fail closed. The kernel boot-ID interface is also required.
5. Atomically create only `/tmp/dlink-phase6a` with private permissions and an additional `.phase8-owner` marker. Stage the **unchanged** bundled Phase 6 rollback/setup scripts in bounded public Base64 chunks, verify their byte digests, and execute the original setup with exactly one validated RSA **public** key.
6. The original script creates the same account symlinks and six private binds and runs the exact original chroot/Dropbear command. No new daemon implementation or global `/etc` overlay is substituted.
7. Audit all six private mount targets, the IPv4-only listener, both-family policy, launcher PID/root/flags, original service listeners and root ro state. Authenticate to 2222 with the client key, require `id -u` = 0 and `id` containing `uid=0(admin)`, then request a PTY login shell and verify terminal stdin/stdout, UID 0 and a second command with stdin held open. Check boot and stock host identity again before reporting success.
8. On setup/audit/authentication failure, clean only owned resources while the same boot and trusted identity can still be established. A lost connection leaves cleanup pending and uses bounded reconnection; a subsequent trusted session can safely recover owned remnants. Unknown identity/ownership/unsafe unmount stops cleanup.

A host-local exclusive lock prevents concurrent commands on this PC. Atomic remote mkdir protects against a different controller claiming the same absent path. Copying the same owner configuration to multiple PCs is unsupported and must not be used as distributed coordination.

JSON events contain only application error codes and non-secret results. Raw Telnet/SSH output, shell commands, passwords, private keys and underlying exception text are suppressed. Exit codes: 0 = command succeeded (inspect the state), 1 = network/trust/auth/policy/recovery failure, 2 = local configuration/file failure, 130 = interrupted. Foreground output can be retained in a protected local log if desired; the scheduled task does not configure a transcript or persistent log file. Task Scheduler records task exit status, while `status` provides a fresh detailed check.

## RAM writes and rollback contract

| Router-side action | Effect | Exact inverse / refusal behavior |
|---|---|---|
| Telnet login and history suppression | Management session, process-local environment; vendor may log normally | Exit shell/CLI or close transport; no vendor logs deleted |
| Scratch mkdir, `.phase8-owner`, original marker, two script uploads | Only the fixed tmpfs tree | Canonical rollback removes that tree after marker/process/mount guards |
| Original setup's key file/account symlinks | Public key and original passwd/group view inside the RAM chroot | Removed only after all owned binds are unmounted |
| Original six binds | `/bin`, `/lib`, `/usr`, `/dev`, `/var`, `/dev/pts` beneath the scratch root; new targets private | Original rollback unmounts dev/pts, var, dev, usr, lib, bin with `-n`; no force/lazy unmount |
| Additional Dropbear | Foreground stock executable in chroot, IPv4 10.0.0.2:2222, key-only, forwarding disabled, RAM PID/log | TERM only processes whose `/proc/PID/root` is exactly the fixed chroot; never killall or stock port-22 replacement |
| Verification sessions | Short-lived SSH command and PTY sessions | Close channels and transport |

Rollback verifies the staged script against the unchanged local canonical asset, then invokes it with a short command. If that file is missing or incomplete, it uploads a fresh, uniquely named canonical repair copy in bounded chunks, verifies it, then invokes that short path. It never overwrites or executes an unverified partial copy. The Phase 9 live test found that a long inline Base64 rollback command times out on this Telnet input path; every fully framed command is now capped at 1000 bytes including CRLF. Owner, same-boot, original marker, process-root and mount guards remain enforced. MD5 is used only to compare transferred public asset bytes against the package, not as host authentication; SSH identity uses SHA-256. Preserve the tree and inspect from original-root Telnet if cleanup refuses. A damaged/missing ownership marker requires manual review; the tool will not guess ownership.

Stopping `watch`, killing Python or uninstalling the task does not implicitly remove a healthy listener. Stop the monitor first, then invoke approved `rollback`. If an interrupted process leaves RAM resources, a later trusted restore/rollback can reconcile them. Do not reboot as an automatic cleanup action. Never delete through live binds, use killall, disable Telnet or alter stock service settings.

## Exposure validation and security limits

The expected custom socket must be **exactly one** `10.0.0.2:2222` TCP listener, with no wildcard, other address or IPv6 port-2222 listener. `iptables -S` is conservatively evaluated for NEW TCP/2222 on every named nontrusted ingress and an abstract future interface. Only `lo` and exactly `br0` are trusted; wildcard bridge names are not equivalent. Supported predicates are ingress interface, TCP/UDP protocol, destination port/range, packet type and connection state, with ordinary chain jumps/RETURN and DROP/REJECT. Declared empty chains return normally. Structurally proven drop/return-only chains can be omitted conservatively: removing their drops enlarges the accepted-packet set, so they cannot make a denial proof falsely succeed. Chains containing ACCEPT, state-changing targets, goto or cycles are never ignored by this shortcut. Multicast/broadcast-only rules do not match the modeled unicast TCP connection. ACCEPT paths on other ingress, unsupported syntax/targets/matches, missing policies and cycles cause refusal. No firewall rule is installed. The IPv6 INPUT policy is collected, and the absence of any IPv6 custom socket is required; IPv6 ACCEPT alone is not called a secure router-wide policy.

This conservative checker refuses rules containing predicates it does not model. That is a deployment blocker to investigate under separate approval, not permission to ignore the check. The tool does not prove end-to-end WAN isolation, guest-LAN isolation or future firewall/bridge changes. It assumes br0 is the physically trusted LAN and the PC's configured source address belongs to that LAN; source binding and a pinned SSH service cannot authenticate the separate Telnet transport. Use only a trusted, preferably direct wired LAN. Do not forward 22, 23 or 2222 to WAN. Stock SSH/Telnet exposure is preserved rather than altered or globally certified. No active WAN probing occurs.

Vendor `sysmgr` may terminate all Dropbear processes during service changes. The monitor can reconstruct its owned listener afterward, but cannot promise uninterrupted sessions. Existing PTY resize, full-screen applications and lengthy root sessions are outside the automated proof. UID 0 in the chroot is real router privilege; the chroot is a filesystem view, not security containment.

## Monitor and Task Scheduler

After separate authorization, run the monitor manually first:

```powershell
.\.venv\Scripts\dlink-ssh.exe watch
```

It audits/restores every 120 seconds by default, with up to five transient attempts and exponential waits of 15, 30, 60, 120 seconds (maximum backoff 300). Offline periods can continue across monitor cycles without rapid polling. Startup handshake failures, disconnects and pending connection-loss cleanup are retryable. Identity mismatch, incorrect credentials, unsafe policy/ownership and unresolved cleanup errors stop the monitor. The next network event may trigger the task again, but cannot bypass those gates.

Review the scheduler files before registering anything:

```powershell
.\windows\install-task.ps1 -Python (Resolve-Path .\.venv\Scripts\python.exe) -WhatIf
# Only after explicit owner approval:
.\windows\install-task.ps1 -Python (Resolve-Path .\.venv\Scripts\python.exe)
```

The task uses the **same interactive Windows user**, limited privileges, and that user's vault. Triggers: PC startup, user logon and NetworkProfile event 10000 (network connected). Multiple instances are ignored. The monitor handles later router reboots/reconnections without a reboot trigger on the router. The install script registers but does not immediately start the task; Windows may require elevation to register the startup/event triggers. Do not run the task as SYSTEM or store your Windows account password in Task Scheduler.

Because the user's interactive token/vault is required, **restoration before the user signs in is not supported**. The startup trigger can only run when that token is available; logon/network triggers provide the normal start. A signed-out PC cannot provide unattended restoration with this design. Locked sessions normally retain the token; locked-session behavior has not been independently established by this export. Task history or manual foreground `watch` helps diagnose failures; no secret-bearing transcript is configured.

```powershell
# Review first; removal also requires approval:
.\windows\uninstall-task.ps1 -WhatIf
.\windows\uninstall-task.ps1
```

Removal checks the exact task description, stops and unregisters only this task, and leaves router state/vault/config/key files intact. It does not perform router rollback. If `watch` holds the local lock, stop that monitor/task before manual restore/status/rollback. If port 39482 on Windows loopback is occupied by something else, the lock fails safely.

## Offline and authorized live tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

All normal tests are offline. Network state/transport failures are mocked; an in-process SSH integration test uses a local simulated encrypted server, not the router. Tests cover offline/rejected credentials, host mismatch, reboot/disconnect, duplicate execution, insufficient RAM, partial cleanup, non-root/key-auth failures, actual UID/PTY proof, scoped rollback, fragmented Telnet framing and IPv4/IPv6 checks. The real-router test is skipped unless explicitly enabled.

Only after explicit authorization for its RAM writes and cleanup, with completed setup and an absent scratch deployment:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_router_integration.py --live-router --router-config "$env:LOCALAPPDATA\DLinkSSHRestore\config.toml" -v
```

The live test restores, verifies a second idempotent run and rolls back in `finally`. It refuses a pre-existing deployment and never reboots. Reboot and scheduler behavior must be validated separately for each installation; host-key rotation stops restoration for explicit verification.

Troubleshooting: `host_identity_changed_explicit_trust_required` needs independent verification; `telnet_credentials_rejected` needs the existing management credential; `conflict_unowned_resources` needs manual ownership review; `unsupported_firewall_*` needs a reviewed exact-rule analysis; `boot_id_unavailable`/firmware/RAM failure needs read-only prerequisite inspection; `failed_cleanup_unconfirmed_*` needs original-root recovery inspection before any further write. A generic remote-command failure deliberately excludes raw output; review the fixed command and use an approved read-only recovery session rather than enabling secret-bearing debug logs.
