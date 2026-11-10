# Historical experiment controllers

These files preserve how measurements and tests were conducted. They are intentionally stored as `.py.txt` / `.ps1.txt`: do not rename and run them as an installation method. Use the maintained [controller](../../automation/README.md) and [reproduction walkthrough](../../docs/REPRODUCING.md).

| File | Purpose and effects |
| --- | --- |
| `phase5_console.py.txt` | Original Telnet collector. It reads the management credential from a locally reconstructed firmware artifact, authenticates, and executes commands from a supplied JSON batch. Its name does not guarantee that arbitrary supplied commands are read-only. |
| `phase5_batch*.json` | Actual command batches used for the read-only investigation. Review each command before any reuse. Early blank/prompt-only observations are not proof of success. |
| `phase6a_execute.py.txt` | Original temporary SSH experiment: stages scripts/public key, creates RAM mounts/listener, tests, and attempts rollback. Requires the original local artifact layout and client trust/key files. |
| `phase6b_execute.py.txt` | Controlled PTY experiments on the same daemon/mount setup. Performs temporary router changes and cleanup; stdin handling is the experimental variable. |
| `phase6*_*.json`, `phase7_*.json` | Additional command batches for prerequisites, environment, host identity, and final recovery checks. |
| `phase9_manual_test.py.txt` | Restore/status/repeat/rollback experiment using the final package and installed local credential configuration. |
| `phase9_watch_test.py.txt` | Foreground monitor experiment and cleanup. Uses the final package and real installed credentials/configuration. |
| `phase9_setup.ps1.txt` | Local interactive setup/key-preparation wrapper from the original deployment. Contains historical paths and assumptions. |
| `phase9_local_diagnostic.ps1.txt` | Local setup diagnostic wrapper; inspect its output handling before adapting it. |
| `phase9_install_approved_task.ps1.txt` | Original task installation/start wrapper; changes Windows scheduled-task state if executed. |
| `phase9_show_telnet_password.py.txt` | Original Windows-only local dialog for an owner-requested credential display. Reads an already extracted artifact; contains no literal password. It does not extract firmware itself. |

## Missing prerequisites

Historical scripts expect `%LOCALAPPDATA%/DLinkResearch`, a `firmware/filesystem-manifest.json` mapping `/usr/sbin/ams_cli` to reconstructed bytes, specific client-key/known-hosts files, and sometimes an installed automation package. These local secret-bearing artifacts are not supplied. Placeholder paths and redacted identities require deliberate adaptation; archived controllers are not claimed to run unchanged.

Many original scripts have top-level actions. Importing or executing them may authenticate, change router RAM resources, launch a monitor, or change Windows scheduling without a separate confirmation prompt. Old approval strings in source are descriptions of the original authorized experiment, not an authorization mechanism. Keep these files as reference text and use the final package for operational work.

The command batches and resulting [findings](../../findings) let readers inspect the actual questions asked, what was measured, and where a test failed. The [PTY diagnosis](../../docs/SSH_PTY_DIAGNOSTICS.md) explains the decisive controlled comparison.
