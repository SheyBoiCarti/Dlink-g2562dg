> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7: SSH host keys

Evidence: [Phase 7 live observations](../archive/raw-evidence/PHASE7_READONLY.json), [public identity follow-up](../archive/raw-evidence/PHASE7_FOLLOWUP.json), [Phase 5 binary lifecycle analysis](../archive/raw-evidence/PHASE5_BINARY_ANALYSIS.json).

## Verified

Stock Dropbear reads `/var/dropbear/rsa_host_key` through its explicit `-r` option. `/var` resolves to `/tmp/var` on tmpfs. File metadata remains UID 0, mode 0600, 805 bytes. Phase 5 sysmgr analysis at `0x13574–0x136a4` identifies directory creation, `dropbearkey -t rsa -f /var/dropbear/rsa_host_key`, launch controlled by ServiceSSH Enable/Port, and process-wide stop/update commands. Phase 7 live strings reconfirm the generation/launch paths; strings alone do not establish conditionals.

Only `dropbearkey -y` public output was obtained; no generation option was executed. Locally computed public fingerprint: `[PUBLIC_KEY_FINGERPRINT_1]`, matching the prior trusted identity. No private key was emitted, copied, changed or backed up.

## Not established

No persistent key restore source or configurable host-key path was found in the inspected startup/service paths. The RAM location and generation code create a regeneration risk, but regeneration on every reboot is an inference, not a reboot observation. Exact generation guards, factory-reset behavior and all possible proprietary restore paths are unresolved. A key surviving service restarts within this boot would not prove reboot retention.

## Proposed identity handling, not executed

Before persistent deployment, separately approve a protected backup of the existing server identity and an exact restore design. A candidate `/data/ssh/rsa_host_key` must be root-owned mode 0600 under a private directory, outside log cleanup, and treated as a secret. Confirm `/data` retention and its mount before use. Restore/copy into RAM before the sole intended daemon starts, or give an approved custom service the persistent path directly. Neither behavior is configured today. Prevent sysmgr regeneration or replacement races through reviewed service ownership; do not overwrite a live key to force a match.

For the first approved reboot, compare the server public fingerprint through retained recovery access before accepting SSH. Unexpected identity must stop automation; do not disable strict host checking or silently replace known_hosts. Deliberate rotation needs explicit approval and an authenticated trust update. Rollback must restore the original protected identity and original service settings, without retaining secret copies in project reports. Current configuration/boot-file backups do not include a server key.
