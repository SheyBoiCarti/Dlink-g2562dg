> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# SSH service investigation — Phase 3

## Current authentication finding

After explicit TOFU approval, the recorded RSA key matched under strict host-key checking. The service offers `publickey,password`; the single password-method attempt ended `Permission denied (publickey,password)`. Agent and user-key authentication were disabled. No accepted account, shell, UID, executable path, startup policy, root-login policy or persistent configuration was established. Server method support does not establish that admin is permitted or that any particular key is authorized.

No further SSH or Telnet authentication attempted. All earlier network/service observations remain valid; the historical trust blocker below is superseded by explicit first-use approval.

## Historical transport/service assessment (preserved)

Observed current SSH 2.0 identification: Dropbear 2014.63 on TCP 22. Default OpenSSH crypto policy fails; narrowly scoped KEX/host-signature options complete key exchange. Strict host-key checking then blocks authentication. See [authentication evidence](SSH_AUTHENTICATION.md).

| Service property | Evidence / limitation |
|---|---|
| Listener / version | Live SSH banner and KEX; version self-reported, executable not inspected |
| Executable location | Unknown; no authenticated command lookup |
| Startup configuration | Unknown; no startup files or links inspected |
| Auto-start / persistence | Unknown; current listening state does not prove reboot behavior |
| Password / public-key methods | Unknown; stopped before user-authentication exchange |
| Root login permitted | Unknown |
| Accepted web-admin credentials | Unknown; no SSH credential submission |
| Interface restriction | Phase 2 UI lists LAN SSH ACCEPT row on port 22; global ACL unchecked. Binding and WAN exposure unverified. |
| Home directory / persistent config | Unknown |

If authentication later succeeds, first establish whether it is a normal shell or a restricted router CLI. Do not feed shell syntax into a restricted CLI or try bypasses. Numeric `id -u` establishes effective privilege; username and web administrator status do not.

For a normal shell, the prepared script can report Dropbear PATH location, readable conventional config-file **existence**, known process names, and conventional startup-link counts without dumping sensitive config or arguments. These hints are not proof that OEM firmware uses OpenWrt init, that root login is enabled, or that keys/configuration survive reboot. Further config reading must be limited to documented non-secret fields under the account's existing permissions. No host/private keys, authorized_keys, shadow, account databases or raw environment dumps are needed.

Package-manager presence does not imply repository compatibility. ARMv7 alone does not establish ABI, libc, float ABI or instruction extensions for custom binaries. None was measured or executed. No package installation, binary transfer, reboot or startup/authentication modification occurred.
