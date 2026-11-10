# Security and recovery

This tool provides real router UID 0. The RAM chroot is a filesystem view, not a security sandbox. Use it only on equipment you own or are authorized to administer.

- Supply the existing Telnet credential locally. Passwords and key passphrases belong in Windows Credential Manager, not TOML, source code, command arguments, or issue reports.
- Keep the encrypted RSA client key and installed configuration outside the repository and cloud-synced folders. Restrict local permissions to the Windows user and SYSTEM.
- Independently verify the router's SSH host fingerprint. Never copy a fingerprint from someone else's installation. A changed identity stops automation; update trust only after independent verification.
- Telnet is unencrypted. The preliminary pinned SSH check does not cryptographically authenticate the separate Telnet connection. Use a physically trusted wired LAN; do not forward management ports to the Internet.
- The tool checks the custom listener's address, socket state, and supported logical firewall policy. It does not establish end-to-end Internet isolation or certify the stock management services.
- The controller uses temporary router RAM resources and preserves stock management services. Firmware, flash, bootloader, startup scripts, and firewall rules are not deliberately modified.

## Recovery

Stop the Windows monitor/task before manual commands; its single-instance lock prevents concurrent controllers. Stopping the monitor alone leaves the custom RAM service running. Use `dlink-ssh rollback` for scoped cleanup after reviewing its effects. Task removal leaves router resources, the local configuration, keys, and credential-vault entries intact.

Rollback verifies ownership, process roots, boot identity, and canonical script bytes. It refuses unknown or unsafe resources. If cleanup refuses, preserve the tree and inspect through the original trusted management path. Never delete through live bind mounts, use broad process-kill commands, or guess ownership. Do not disable the original recovery path while relying on this experimental service.

## Reporting problems

Use a minimal description and sanitized application error codes. Exclude passwords, keys, router exports, raw Telnet/SSH transcripts, packet captures, account identifiers, and public network addresses from public reports. Review any attachment before uploading it.
