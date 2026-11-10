# Troubleshooting reproduction

| Symptom | Meaning and next check |
| --- | --- |
| Web login works, Telnet login fails | Distinct authentication domains. Confirm that you have the authorized management credential; this repository does not supply it. |
| Prompt is `AMS#` | You are in the management CLI. Enter `sh`, then verify `id -u` equals `0`. |
| `root` fails as an SSH username | The verified Unix UID 0 account is `admin`; `root` is the management CLI account name. |
| Modern SSH rejects algorithms | This legacy firmware needs per-invocation exceptions. Use the walkthrough; do not weaken your global SSH configuration. |
| `host_identity_changed_explicit_trust_required` | Stop and independently verify the current public host key. After verification use local `setup --update-trust`; do not bypass checking. |
| `offline_or_trusted_lan_unavailable` | Check Ethernet, stock SSH reachability, and the configured PC source IPv4 address. This is not an authentication result. |
| `telnet_credentials_rejected` | The existing management credential was rejected. Do not substitute repeated web-account guesses. |
| `conflict_unowned_resources` | Scratch paths, mounts, or a listener do not match this controller's ownership. Inspect through original recovery access; do not delete or adopt them blindly. |
| `another_instance_running` | Stop the foreground/scheduled monitor before running manual commands. Another process may own the local lock port. |
| `unsupported_firewall_*` | The policy parser cannot prove the required restriction. Inspect exact rules; do not disable the checker or assume the router is protected. |
| SSH authenticates but immediately exits with no output | Check client stdin lifetime. Use a real terminal or keep subprocess stdin open. Authentication and PTY acceptance do not prove a usable shell. |
| `status` succeeds with state `absent` | Inspection worked; a custom service was not found. Use a reviewed `restore` to provision it. |
| Scheduler is installed but SSH is absent | A signed-in user's token/vault is required; inspect task state and sanitized error codes. Check trust changes and source network. Task registration alone is not proof. |
| Router reboot removes SSH on 2222 | Expected for RAM-backed resources. Restoration requires the Windows controller and accepted verified host identity. |
| `failed_cleanup_unconfirmed_*` | Cleanup could not be confirmed. Retain original recovery access and inspect ownership/mount state before further changes. |

Do not paste raw management transcripts, configuration exports, credentials, or private keys into public issues. Provide the device/firmware identity, the command name, sanitized application code, and whether an original recovery session still works.
