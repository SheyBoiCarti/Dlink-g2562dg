> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# SSH PTY diagnostics: Phase 6B

Date: 2026-10-19. **Interactive UID 0 SSH verified after an approved RAM-only test; full cleanup verified.** No permanent changes or reboot occurred.

## Verified baseline

Read Phase 5 results/readiness, Linux environment, Dropbear, persistence and recovery reports, and Phase 6A results, controller and setup/rollback scripts. Phase 6A verified two non-PTY public-key command sessions as UID 0. Its separate `-tt` test authenticated, returned no output and exited 255 (remote status -1). Authentication success does not establish PTY allocation or shell startup.

[Live diagnostics](../archive/raw-evidence/PHASE6B_READONLY.json), [follow-up](../archive/raw-evidence/PHASE6B_FOLLOWUP.json) and [boot/device checks](../archive/raw-evidence/PHASE6B_BOOT.json) establish:

- `/dev/ptmx` is a character device, major/minor 5:2, mode 0660; `/dev/tty` is 5:0. `/dev/pts` is devpts, mounted `rw,mode=600`. `/dev/pts/ptmx` is absent. That absence is not itself a defect: this kernel uses the separately created `/dev/ptmx` node.
- `/proc/tty/drivers` lists UNIX PTY master/slave and legacy PTY drivers. Kernel PTY count was 1, limit 4096. `/proc/config.gz` is unavailable, so exact build-option values were not read.
- The active Telnet root shell's descriptors 0/1/2 resolve to `/dev/pts/0`. This proves PTY use works in the original root, not inside the Phase 6A chroot.
- `/bin/sh` links to BusyBox. Telnet shell flags include `i`. `/etc/profile`, `/etc/shells` and `/etc/securetty` are absent. `tty`, `stty`, `script`, Python and strace were not found in the inspected command paths; BusyBox has no tty/stty/script applets. `setsid` and `chroot` exist.
- The old temporary tree is gone. Its setup supplied a nonrecursive `/dev` bind plus a separate `/dev/pts` bind, both marked private at their new targets. It did **not** supply `/proc`. Bind creation succeeded in Phase 6A, but slave-node resolution during a live SSH PTY was not captured.

## Binary and source comparison

The actual Dropbear imports `openpty` and `ttyname`. Existing local copies of uClibc and libutil match live MD5 digests; their SHA-256 identities and symbols are recorded in [binary notes](../archive/raw-evidence/PHASE6B_BINARY_NOTES.json). Matching `ttyname_r` code scans device directories. Therefore adding `/proc` is not a justified fix merely because the chroot lacked it.

Upstream [Dropbear 2014.63 sshpty.c](https://raw.githubusercontent.com/mkj/dropbear/DROPBEAR_2014.63/sshpty.c) and [session handling](https://raw.githubusercontent.com/mkj/dropbear/DROPBEAR_2014.63/svr-chansession.c) separate allocation, controlling-terminal setup, login bookkeeping and shell execution. These are comparison references; vendor runtime behavior takes precedence.

## Hypotheses and next discriminating test

| Hypothesis | Evidence / required discriminator |
|---|---|
| Kernel lacks PTYs | Contradicted by live Telnet `/dev/pts/0` and PTY driver inventory |
| Incorrect or incomplete chroot device view | Plausible; capture PTY-request reply and inspect slave paths while test is active |
| Client terminal/stdin handling closes the session | Plausible; old controller captured output but did not manage a persistent interactive stdin stream; compare explicit stdin pipe and TERM |
| Failure after allocation, during controlling tty or shell start | Plausible; require full client debug output and test-daemon log to locate boundary |
| Missing `/proc` or login files | Unproven; do not add mounts or synthesize files without evidence |

## Approved temporary test scope (executed and removed)

Reuse the unchanged operational commands in [Phase 6A setup](../scripts/phase6a_setup.sh) and [rollback](../scripts/phase6a_rollback.sh). Create only the owned `/tmp/dlink-phase6a` tree, public key and six reviewed bind mounts. Start the existing binary with:

```sh
chroot /tmp/dlink-phase6a/root /usr/sbin/dropbear \
  -F -E -r /var/dropbear/rsa_host_key \
  -p 10.0.0.2:2222 -s -j -k -P /run/dropbear.pid
```

Keep original-root Telnet open. Verify the existing pinned host identity and unused 2222 before launch. Do not restart or reconfigure port 22. Retain full sanitized client diagnostics and the temporary daemon log, rather than the Phase 6A filtered subset.

Use the Phase 6A dedicated client key and known-hosts file with strict host checking, publickey-only, agent/password fallbacks disabled, and the same per-invocation legacy exceptions. Test these separately with `TERM=xterm` in the client process:

1. `ssh -T ... admin@10.0.0.2 "unset HISTFILE; id; uname -srm"` as a control.
2. `ssh -vvv -tt ... admin@10.0.0.2 "unset HISTFILE; id; test -t 0 && echo PTY_STDIN; test -t 1 && echo PTY_STDOUT"`, holding a client stdin pipe open until the remote command exits.
3. `ssh -vvv -tt ... admin@10.0.0.2` with a maintained stdin pipe: send `unset HISTFILE; HISTSIZE=0`, then `id; test -t 0 && echo INTERACTIVE_PTY`, a second command and finally `exit`. Require both responses and UID 0, not just a prompt.
4. If PTY fails, optionally test `ssh -T ... admin@10.0.0.2 /bin/sh -i` with a maintained command stream. This may provide command dialogue but is not a terminal, has no verified job control and cannot satisfy PTY success.

No additional `/proc` bind, devpts remount, device-node creation, tracing binary upload or shell configuration changes are included. After success or failure, immediately run the existing rollback and verify original services, mount state and fresh Telnet UID 0. Further changes require a separately reviewed scope. See [rollback](SSH_ROLLBACK.md).

## Controlled test results: client stdin caused the failure

[Full execution evidence](../archive/raw-evidence/PHASE6B_EXECUTION.json) records these tests against the **same running daemon and same six mounts**:

| Test | Result |
|---|---|
| Non-PTY control, maintained stdin | UID 0, exit 0 |
| PTY with inherited stdin, TERM unset | Exit 255, no output; PTY request **accepted**, then client `read failed` / `send eof` |
| PTY with maintained stdin pipe, TERM unset | UID 0, stdin/stdout both terminals, exit 0 |
| Same maintained stdin, TERM=xterm | UID 0, stdin/stdout both terminals, exit 0 |
| Login shell, maintained stdin, TERM=xterm | UID 0, terminal confirmed, second command answered, normal exit 0 |

Changing only inherited stdin to an open pipe changed failure to success even with TERM unset. This isolates the observed failure to client stdin lifetime/read handling in the automated Git/OpenSSH test. It was **not a PTY allocation failure**: the server accepted allocation in the failing case too. The exact lower-level cause of the inherited Windows handle's failed read was not instrumented, but no router-side fix is needed for the demonstrated interactive path.

The actual login-shell output included:

```text
~ # id
uid=0(admin) gid=0(admin)
INTERACTIVE_PTY
SECOND_COMMAND_OK
```

Use an actual interactive terminal or keep the subprocess stdin pipe open until the shell exits. The successful automated test sent multiple newline-terminated commands through `Popen(stdin=PIPE)`, flushed them and kept the pipe open while waiting; stdout/stderr were drained concurrently. Avoid `ssh -n`, null stdin or closing stdin immediately after starting a PTY session. TERM=xterm is a sensible explicit setting but was not required to fix this failure. Full-screen applications, resize, signal forwarding and prolonged sessions were not tested.

No `/proc` bind, devpts remount, device creation or profile changes were needed. The non-PTY fallback was unnecessary and was not tested. Original host identity, services and fresh Telnet UID 0 were reconfirmed after rollback in [independent final checks](../archive/raw-evidence/PHASE6B_FINAL_CHECKS.json). A working test does not leave an SSH listener active: port 2222 is now absent.

## Exact interactive client command for an approved active test

Run from an actual PowerShell terminal after separately approved reactivation; it will currently fail because cleanup removed port 2222. Keep the terminal input attached. Never pipe an empty input stream or use `-n`.

```powershell
$keyDir = Join-Path $env:LOCALAPPDATA 'DLinkResearch/ssh/phase6a-20261019-202134'
$env:TERM = 'xterm'
& 'C:/Program Files/Git/usr/bin/ssh.exe' -F none -tt -p 2222 `
  -i (Join-Path $keyDir 'id_rsa_dlink_phase6a') `
  -o "UserKnownHostsFile=$keyDir/known_hosts_phase6a" `
  -o GlobalKnownHostsFile=none -o StrictHostKeyChecking=yes `
  -o UpdateHostKeys=no -o IdentitiesOnly=yes -o IdentityAgent=none `
  -o PreferredAuthentications=publickey -o PasswordAuthentication=no `
  -o KbdInteractiveAuthentication=no -o BatchMode=yes `
  -o KexAlgorithms=+diffie-hellman-group14-sha1 `
  -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa `
  admin@10.0.0.2
```

The equivalent managed-stdin invocation was tested, including strict host checking and these scoped crypto exceptions. The above human-terminal invocation itself was not separately exercised. At the shell, first run `unset HISTFILE; HISTSIZE=0`, then `id`, `test -t 0`, a second command and `exit`. No original service/key configuration is changed by this client command.
