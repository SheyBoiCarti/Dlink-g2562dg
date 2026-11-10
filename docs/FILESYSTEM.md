> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Filesystem assessment — Phase 3

## Continuation result

Host trust was approved through TOFU, but the single SSH password-method attempt ended Permission denied. No authenticated filesystem access occurred. All filesystem properties below remain unknown; no mount, df, directory check, write test or script execution was performed on the router.

## Preserved filesystem assessment

No authenticated shell was opened. `mount`, `df`, `/proc/mounts`, home-directory checks and filesystem inspection were not run on the router.

| Property | Current status |
|---|---|
| Root filesystem type | Unknown |
| Read-only versus writable root | Unknown |
| Overlay / persistent partitions | Unknown |
| Temporary filesystems | Unknown |
| Account home and permissions | Unknown |
| Writable storage | Unknown; no write test allowed or attempted |
| Startup configuration persistence | Unknown |

Community read-only-filesystem reports remain hypotheses for another owner's firmware, not observations of this device. An `rw` flag or a writable-permission check alone would not prove successful writes or reboot persistence.

After a trusted SSH login and POSIX-shell confirmation, individual approved read-only commands may identify mount flags and capacity. Raw mount options can contain network credentials; raw process output can contain tokens. Do not capture these blindly. The prepared [diagnostic script](../scripts/shell_diagnostics.sh) emits filesystem types/modes and capacity while withholding mount sources, arbitrary options and nonstandard mountpoint names. It requires explicit review, has not been uploaded, and has not run on the router.

No remount, write test, permission change, package installation or persistence action performed.
