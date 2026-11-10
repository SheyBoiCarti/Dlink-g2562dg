> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Current Phase 9 deployment

The owner-approved DLinkSSHRestore task is enabled and Running with a Limited/Interactive current-user principal. Independent scheduled-service verification passed for key authentication, UID 0, PTY, mounts and expected IPv4-only listener. Non-elevated registration was denied; the approved UAC helper registered the same reviewed task and requested start. A duplicate start was refused while the existing unique monitor remained running. No Windows reboot/logoff test was performed. The detailed checkpoint history below is historical; [DEPLOYMENT_STATUS](../findings/DEPLOYMENT_STATUS.md) is authoritative for current state.

The owner restarted the router and the host identity changed. Read-only trusted-Ethernet public-key verification and explicit acceptance preceded the local trust-pin update and successful post-restart RAM test. Future host-key rotation still requires this gate. The task/listener are intentionally running now; no firmware/startup/flash/firewall change was made.

## Stop, inspect, or roll back the active deployment

```powershell
Stop-ScheduledTask -TaskName DLinkSSHRestore
.\automation\.venv312\Scripts\dlink-ssh.exe status
.\automation\.venv312\Scripts\dlink-ssh.exe rollback
```

Stopping the monitor alone does not remove router RAM state. To resume, start the existing task explicitly after resolving any trust/configuration issue. Removing the task uses the reviewed uninstall script and may require the same Windows elevation as registration. Do not disable Telnet recovery.

# Phase 9 automation deployment

## Verified environment and local setup

Windows Ethernet uses 10.0.0.10/24 with an on-link route to 10.0.0.0/24. Python 3.12.14 environment is automation/.venv312; Paramiko 4.0.0 and keyring 25.7.0 satisfy dependencies. Configuration is `%LOCALAPPDATA%/DLinkSSHRestore/config.toml`; protected RSA-3072 key material remains there outside OneDrive. The public key matches its encrypted private key. Windows Credential Manager contains the required entries; no values are included in project reports. Private-key access is limited to the current user and SYSTEM after DACL-only adjustment using icacls. PowerShell Set-Acl requested an unavailable security privilege, and a launched Windows PowerShell 5.1 window could not auto-load its security module; interactive setup completed in PowerShell 7 after read-only permission verification.

Stock port 22 presents the historically pinned SHA-256 host identity. Telnet reaches LOGIN#, authenticates through the configured vault and enters UID 0 shell. The boot-ID interface is available, root JFFS2 is ro, /tmp is tmpfs and roughly 39.7 MiB RAM was available at preflight. No initial scratch deployment or port 2222 listener existed. No firmware/startup/bootloader/flash changes or reboot were performed.

## Approved temporary scope and live outcome

The owner explicitly approved RAM setup, UID/PTY/status/idempotence checks, a brief foreground monitor and scoped cleanup. This does not authorize scheduled tasks or reboot tests. The unchanged Phase 6A/6B assets implement the same six private binds and key-only IPv4 listener at 10.0.0.2:2222. A retained original-root Telnet session provided recovery throughout the manual trial.

The initial restore/status/repeated restore passed, but inline rollback timed out. Read-only input-length probes reproduced the issue; the short verified staged Phase 6 rollback recovered every temporary resource. A bounded staging/invocation fix was regression-tested and the complete manual sequence repeated successfully. Original Dropbear/Telnet PIDs 3244/1037, host identity and boot ID were preserved; a fresh original Telnet UID 0 login succeeded afterward. See [execution evidence](../archive/raw-evidence/PHASE9_MANUAL_EXECUTION.json).

## Fixes made without redesign

- The stock firewall's multicast accept, empty chains, drop-only anti-attack chain and UDP-only DHCP relay initially exceeded the checker grammar. Explicit packet-type/UDP handling and conservative structural drop-only-chain treatment resolve this without altering firewall rules or ignoring possible ACCEPT paths.
- Long inline rollback exceeded this live Telnet input path's usable length. All framed commands now have a 1000-byte ceiling. Normal rollback verifies and invokes the staged canonical script; interrupted uploads can be repaired using short bounded chunks to a fresh internal filename before verified invocation.
- Original shell assets, chroot layout, account mapping, service argv and recovery guards are unchanged. Reboot, disconnect, incorrect/unavailable credentials, mismatch and destructive failure cases remain mock-based rather than deliberately disrupting the router.

## Commands after authorization

Use the configured environment from the project root:

```powershell
.\automation\.venv312\Scripts\dlink-ssh.exe status
.\automation\.venv312\Scripts\dlink-ssh.exe restore
.\automation\.venv312\Scripts\dlink-ssh.exe rollback
```

The restore command verifies SSH key authentication, numeric UID 0, id account output, PTY terminal stdin/stdout and a second shell command before success. Stop a running watch process/task first: the single-instance lock rejects concurrent commands. Stop the monitor before explicit rollback; stopping it alone leaves its healthy RAM listener running.

The Windows installer also required a small CIM fix: client-only event triggers must be constructed from Get-CimClass metadata to preserve the MSFT_TaskTrigger base type. An actual read-only -WhatIf test now builds the complete task definition; registration is forbidden by the offline regression wrapper.

## Windows deployment checkpoint

The foreground watch trial passed restoration and a later idempotent audit, then cleaned up; scheduled-task installation/enabling requires explicit owner approval after successful manual integration. The existing installer registers startup, current-user logon and network-connect triggers with limited privileges, interactive token, network availability and IgnoreNew multiple-instance policy. It does not save a Windows account password. Signed-out/pre-logon restoration is unsupported. Defaults remain five transient attempts, 15-second exponential base and 120-second cycle; a foreground test can use 60 seconds without changing production defaults.

Do not register a task until [DEPLOYMENT_STATUS](../findings/DEPLOYMENT_STATUS.md) records approval. Review command:

```powershell
.\automation\windows\install-task.ps1 -Python (Resolve-Path .\automation\.venv312\Scripts\python.exe) -WhatIf
```

A task removal stops/unregisters only the matching named task and does not roll back router state or erase vault/key/configuration files. Do not substitute SYSTEM or silently elevate. Any actual registration, enablement or start must be covered by explicit approval.

## Security and recovery limits

The custom listener must be exactly one IPv4 10.0.0.2:2222 socket; custom IPv6/wildcard sockets are rejected. Live IPv4 rule analysis denies modeled NEW TCP/2222 on nontrusted ingress, assuming br0 is the trusted LAN. Original IPv6 INPUT is ACCEPT and original Telnet/SSH sockets are wildcard; no external WAN-vantage test was performed. Physical bridge topology, guest isolation, ISP routing and Internet reachability are not globally certified. This is not a claim that stock Telnet is Internet-safe. No firewall changes or active WAN probes were made.

A changed host identity stops automation and requires independent verification plus explicit local trust update. Reboot restoration has not been tested because reboot authorization was not given. Keep Telnet recovery. Refused ownership/mount/identity guards require investigation, never force/lazy unmount, killall, broad deletion, reset or flash writes.
