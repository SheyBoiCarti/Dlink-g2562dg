# Reproducing the result

This guide separates obtaining a Linux shell from restoring SSH. The controller handles only the second part. Read [how the investigation worked](RESEARCH.md) for the discovery evidence and the [offline extraction guide](../research/firmware/README.md) for the recovered, digest-verified firmware workflow. Extracted bytes and credentials must stay private; extraction alone does not verify access to another router.

## 1. Check the device and prepare the PC

Confirm DSL-G2562DG and firmware `TK_1.00TK_V1.2.12ak_20221018` in the router's web Device Information page. Other versions are unverified. Use Windows 11, Python 3.12+, Git Bash in its default installation directory, and a physically trusted Ethernet connection. PowerShell 7 is needed for the scheduler-definition test. Keep an existing management/recovery session available during the first restore.

This code deliberately requires router address `10.0.0.2`, trusted subnet `10.0.0.0/24`, and router bridge `br0`. These values are validated in code and scripts; editing only the example TOML does not port it to a different network. Your PC needs its own address in that subnet; do not assign it the router's address.

From PowerShell:

```powershell
Test-NetConnection 10.0.0.2 -Port 23
Test-NetConnection 10.0.0.2 -Port 22
```

`TcpTestSucceeded: True` confirms reachability only. It does not prove authentication, identity, or Linux access. If either prerequisite service is unavailable, investigate the router's supported management settings before proceeding.

## 2. Establish the original Linux shell

Use a Telnet client on the trusted LAN to connect to `10.0.0.2:23`. Supply your authorized management credential interactively, never as a command-line password. The verified account name is `root`; this is separate from the web account. The password is not supplied by this repository. If you do not have it, stop here and read the credential-discovery limitations in [the research notes](RESEARCH.md#1-finding-a-management-account).

Expected sequence, with credentials omitted:

```text
LOGIN# [management username]
PASS# [management password, entered interactively]
AMS# sh
~ # id
uid=0(admin) gid=0(admin)
~ # uname -srm
Linux 3.14.18 armv7l
```

`AMS#` alone is the management CLI, not the Linux shell. `sh` changes to the shell; numeric UID 0 is the root proof. A rejected web password does not disprove management access. Do not repeatedly guess credentials.

Inspect a few prerequisites in that original shell:

```sh
id -u
readlink /var
awk '$2=="/" || $2=="/tmp" {print $2, $3, $4}' /proc/mounts
ip -o -4 addr show br0
```

Expect `0`, `/tmp/var`, read-only JFFS2 at `/`, tmpfs at `/tmp`, and `10.0.0.2/24` on `br0`. These are read-only checks. The controller performs additional checks before provisioning. An unexpected result is a compatibility issue to investigate, not a reason to bypass its checks.

## 3. Verify the router's public SSH identity

In the original root shell:

```sh
dropbearkey -y -f /var/dropbear/rsa_host_key
```

The `-y` operation prints public information. Do not `cat`, export, or upload the private host-key file. Copy only the single public line beginning `ssh-rsa ` to a temporary local `.pub` file outside the repository. On Windows, compute its fingerprint:

```powershell
ssh-keygen -lf "$env:LOCALAPPDATA\DLinkSSHRestore\router_host.pub" -E sha256
```

Create that local directory before saving the public file. Record the `SHA256:...` fingerprint from your own router. Compare it with the public identity presented by stock SSH on port 22 before accepting trust. A host-key network scan alone is not independent verification. The console check relies on your physically trusted connection because Telnet itself is plaintext. Never use a fingerprint copied from this project or another owner's device.

The application checks its pinned fingerprint before sending Telnet credentials and also checks the custom SSH service's identity. After a reboot, repeat independent verification if the identity changes; do not simply accept the newly offered key.

## 4. Install and configure the controller

From the repository root:

```powershell
cd automation
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[test]'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\dlink-ssh.exe --help
```

The normal tests are offline. A skipped real-router test is expected. See [installation and operation](../automation/README.md#prepare-a-protected-client-key) to create an encrypted RSA-3072 client key outside this repository, restrict its Windows permissions, and run:

```powershell
.\.venv\Scripts\dlink-ssh.exe setup
```

Supply the PC's trusted Ethernet address, client key paths, independently verified router host fingerprint, existing management password, and key passphrase. Setup is local: it does not connect to or change the router. It stores the two secrets in Windows Credential Manager; the example TOML is documentation, not a ready-to-use installed configuration.

## 5. Run a temporary restore and verify it

Read the [RAM writes and rollback contract](../automation/README.md#ram-writes-and-rollback-contract) first. The following `restore` intentionally creates temporary files, bind mounts, and an additional root SSH daemon on the router:

```powershell
.\.venv\Scripts\dlink-ssh.exe restore
.\.venv\Scripts\dlink-ssh.exe status
```

Successful restoration means more than an open port: the tool checks ownership, boot identity, mounts, listener address, supported ingress policy, key authentication, UID 0, and an interactive PTY with a second command. Read the JSON event/results, not just the process exit code. A successful `status` reporting `absent` means inspection succeeded but the service is absent. A second `restore` should audit the existing healthy deployment rather than create a duplicate.

This is not a Telnet-to-SSH credential conversion. Telnet uses management username `root`; the new SSH service uses Unix username `admin` and your dedicated client key. `admin` maps to UID 0 on this firmware.

### Open an interactive terminal

Use an actual terminal with stdin attached. Obtain the public host-key line as described above, and create a dedicated local known-hosts file containing `[10.0.0.2]:2222 ` followed by that `ssh-rsa ...` line. Verify the key's SHA-256 fingerprint before saving it. Set `$clientKey` and `$knownHosts` to your actual local file paths, then use a compatible OpenSSH client:

```powershell
$env:TERM = 'xterm'
ssh -F none -tt -p 2222 -i $clientKey `
  -o "UserKnownHostsFile=$knownHosts" `
  -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes `
  -o IdentityAgent=none -o PreferredAuthentications=publickey `
  -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no `
  -o KexAlgorithms=+diffie-hellman-group14-sha1 `
  -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa `
  admin@10.0.0.2
```

These legacy algorithm exceptions apply only to this invocation. Enter the client key's passphrase when prompted. Do not disable host-key checking. In the shell, run `id`, `test -t 0 && echo PTY_STDIN`, and another simple command before exiting. Never pipe an empty stream to this session or use `ssh -n`: premature stdin closure caused an apparent PTY failure during the original investigation.

## 6. Prove cleanup before scheduling

With no monitor running, review and invoke:

```powershell
.\.venv\Scripts\dlink-ssh.exe rollback
.\.venv\Scripts\dlink-ssh.exe status
```

Expect the custom setup to be absent. Independently check that original Telnet still reaches `sh` with UID 0. Rollback should remove only owned processes, mounts, and the temporary tree; it must not alter the stock services. If it refuses cleanup, preserve the resources and use [recovery guidance](SECURITY.md#recovery).

Only after this round trip works, follow the [monitor and scheduler instructions](../automation/README.md#monitor-and-task-scheduler). Run foreground `watch` first; scheduler installation is optional. Stop the monitor before manual CLI operations. Stopping or uninstalling the task alone does not roll back router resources.

## 7. Reboot behavior

A deliberate router restart is a separate, disruptive test; none is required to follow the temporary round trip above. If you choose to validate reboot restoration on your own device, expect the RAM listener to disappear. The controller can restore it only with a running signed-in Windows controller and valid trust. The original investigation observed a changed host key after restart, independently verified it, explicitly updated the local trust pin, and then restored SSH. Fully unattended restoration across host-key rotation is not implemented.
