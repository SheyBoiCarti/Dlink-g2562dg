> Historical overview. The [reading guide](READING_GUIDE.md) explains which results supersede earlier findings. Paths and public device identities are sanitized.

# DSL-G2562DG Phase 2

Current investigation: [Phase 5 results](../archive/phase-history/PHASE5_RESULTS.md) — live read-only Linux/Dropbear investigation completed. Public-key code uses `/etc/dropbear/authorized_keys` for UID 0 `admin`; that directory is absent on read-only rootfs. See [Dropbear analysis](../docs/DROPBEAR_ANALYSIS.md), [gated persistence plan](../docs/SSH_PERSISTENCE.md), [recovery](../docs/RECOVERY.md) and [Phase 6 readiness](../archive/phase-history/PHASE6_READINESS.md). No SSH, firewall, startup or flash changes were implemented, and Telnet remains enabled.

Latest outcome: **[Root Linux access verified](../findings/ROOT_ACCESS_VERIFIED.md)**. A firmware-derived built-in Telnet account reaches `AMS#`; `sh` opens Linux with `uid=0(admin)`. Actual kernel/architecture: `Linux 3.14.18 armv7l`. No firmware flashing or configuration change was required. Sessions were closed after read-only verification. Earlier phase findings below are historical.

Phase 4: [UART results](../archive/phase-history/PHASE4_RESULTS.md), [hardware evidence](../docs/UART_HARDWARE.md) and [safe access assessment](../docs/UART_ACCESS.md). Public research found no verified board pinout, voltage or baud rate. UART root remained a report, not a reproduced result. No hardware was connected; Phase 4 stopped at research.

Previous: [Phase 3B alternative-access results](../archive/phase-history/PHASE3B_RESULTS.md). Telnet identifies D-Link ams_cli at LOGIN#; FTP metadata works but filesystem commands require authentication. No root path verified. See the prior [ranking](../findings/ACCESS_METHODS.md).

## Phase 3 update

[Phase 3 results](../archive/phase-history/PHASE3_RESULTS.md): SSH transport requires two observed legacy algorithm options. The continuation established user-approved TOFU for the exact RSA key, then a single secure-dialog password-method attempt ended Permission denied. No shell opened. See [authentication details](../docs/SSH_AUTHENTICATION.md) for the approved first-use fingerprint, recorded trust decision and authentication outcome. The fingerprint was not independently verified; accepting it required explicit user approval.

The prepared [shell diagnostics](../scripts/shell_diagnostics.sh) are for an already authenticated POSIX shell only. Review all commands before use; the script requires `--reviewed`. It never authenticates or writes router files and was not uploaded or executed on the router. A restricted CLI must be investigated through its own documented commands instead. Phase 2 evidence below is historical and preserved.

Read [results](../archive/phase-history/PHASE2_RESULTS.md) first. Investigated 2026-10-19; target is strictly `10.0.0.2`. No shell login, exploitation, configuration changes, backup exports, firmware downloads, reboot, or hardware interaction performed.

From `<WORKSPACE_OR_USER_HOME>`, run Windows discovery:

```powershell
powershell -NoProfile -File .\dlink-g2562dg\scripts\check_ports.ps1
```

In an existing WSL Ubuntu terminal (Python 3 required):

```bash
cd /path/to/private-workspace
bash dlink-g2562dg/scripts/check_ports.sh
bash dlink-g2562dg/scripts/inspect_http.sh
```

Scripts accept either no argument or exactly `10.0.0.2`. They do not authenticate, accept credentials, follow HTTP redirects, use proxies, or send shell commands. TCP probes are sequential with 2-second connection/read timeouts and 200-ms spacing. Only FTP/SSH/Telnet greetings are read; other TCP services receive no application data. HTTP inspection makes four root GET requests with 3-second socket timeouts and normal certificate verification. Banner contents and non-allowlisted headers are withheld. An open port never proves authenticated Linux access. Scripts exit successfully when measurements finish even when individual services are unavailable; read each row's state/error. Invalid target exits nonzero.

HTTP output gives only constrained metadata. Redirect destinations, cookie values, authentication realm/token values, and response bodies are never printed. Full HTTP headers and raw packet captures are intentionally absent because they may contain secrets. `server_header_present=false` means no observable server identity, not no server.

Nmap was absent; nothing installed. If already available, this optional command checks only the eight TCP ports without version probes, OS detection, scripts, or authentication:

```text
nmap -n -Pn -sT -p 21,22,23,53,80,443,8080,8443 --max-retries 0 --scan-delay 250ms --max-parallelism 1 --host-timeout 30s 10.0.0.2
```

Nmap service names without `-sV` are port labels, not protocol evidence. Do not add scripts or expand the target/port set. TCP 53 does not test UDP DNS.

Verification (requires Python 3 plus Git Bash on Windows, or Bash on Linux):

```powershell
python -m unittest discover -s dlink-g2562dg/tests -v
```

The Bash scripts were syntax checked using Git Bash. The HTTP script was executed there using Python 3; **WSL Ubuntu execution was unavailable**: the installed WSL launcher returned installation/usage text rather than a distribution. No WSL installation or repair was attempted. Windows TCP results are actual LAN observations.
