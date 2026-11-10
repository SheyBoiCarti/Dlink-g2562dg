> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 8 results: external SSH restoration automation

Date: 2026-10-19. Target firmware remains `TK_1.00TK_V1.2.12ak_20221018`; fixed address 10.0.0.2. This phase implemented local software and ran offline verification only. It did not contact the router, access/store real router credentials, register/start a Windows task or change Windows startup configuration.

## Delivered

The [automation project](../../automation/README.md) contains the requested Python package/modules, secret-free example TOML, interactive setup, restore/status/rollback CLI, bounded monitor, Windows task installer/uninstaller and offline/live-opt-in tests. Bundled Phase 6A setup and rollback scripts are byte-identical to existing project scripts; previous research and scripts remain unchanged. A wheel is built under automation/dist. Local isolated dependency environments were created for Python 3.12 and 3.14; no global dependency installation was required.

Transport, provisioning, SSH verification and rollback are separate. No firmware-derived credential extraction is used. The explicit Windows vault backend stores Telnet password/key passphrase only during a later owner-invoked setup. RSA >=3072 and an encrypted private key are required; the public/private pair is checked locally. Router IP/account/ports/paths are fixed to verified values, not interpolated arbitrary configuration. SSH handshakes pin SHA-256 identity before Telnet credentials and custom SSH authentication. No password SSH/agent fallback or silent identity update exists.

The original RAM chroot/stock Dropbear method is reused. An additional RAM owner marker, atomic mkdir and host-local process lock protect ownership/idempotence. Cleanup streams the unchanged local rollback asset so interrupted remote uploads cannot corrupt the cleanup code. Existing-owned security failures trigger scoped cleanup; missing owned listeners can be reconstructed. Same-boot/trusted-identity checks prevent cleanup in an unknown reboot state. Inactive/disconnected transports use bounded retries; authentication/trust/policy/ownership failures stop for intervention.

Success requires actual public-key authentication, UID 0/id account output, an allocated PTY login shell with terminal stdin/stdout and a second shell command, plus fresh boot/identity and exposure audits. IPv4 evaluation fails closed on non-LAN ACCEPT or unsupported predicates; any custom IPv6/wildcard listener is rejected. All six private bind targets and source propagation are checked. No firewall edits or WAN probes are included.

## Validation

- Full repository pytest suite on Python 3.12 and Python 3.14: **58 passed, 1 skipped**. The skipped case is the explicitly authorized-only real-router round trip.
- Offline coverage includes unreachable router, actual rejection classification, host mismatch before credentials, encrypted SSH mismatch/key rejection/UID and PTY proof, SSH connection loss after handshake, duplicate execution, partial upload recovery, boot/disconnect handling, low RAM, guarded rollback, foreign listener/tree refusal, IPv4/IPv6 policy and mount/propagation checks.
- The encrypted integration server runs locally over a socket pair. It is not a real-router or Dropbear integration test.
- Both Windows task files passed PowerShell parser checks without execution. Generated provisioning commands were checked with local Bash syntax-only parsing; the assets were compared byte-for-byte against the original scripts.
- Paramiko 5 compatibility test correctly failed because required legacy algorithms were removed. Dependencies constrain Paramiko to >=4,<5, and algorithms are scoped to the fixed router's transports. Runtime dependency consistency and CLI help were checked.
- Independent review identified interrupted rollback upload, existing-owned exposure cleanup and startup/post-handshake retry gaps. Each was reproduced or covered by regression tests and addressed before completion.

## Security limitations and deployment blockers

1. Real-router integration and a separately approved controlled reboot remain unperformed. No claim of operational reboot restoration is made.
2. A regenerated router host identity intentionally blocks automation until independently verified and explicitly trusted through local setup --update-trust. Fully unattended operation cannot be promised across key rotation without violating this requirement.
3. Task registration/event behavior and real Windows vault access remain untested. The task uses the same interactive user with limited privileges; pre-logon/signed-out restoration is unsupported. No Windows account password is saved.
4. Existing firewall rules may contain unsupported syntax and be refused. Source binding and conservative INPUT/socket checks do not prove physical topology, guest isolation or end-to-end WAN denial. br0 must remain the trusted LAN. Existing stock service exposure is unchanged, not globally certified safe.
5. Telnet is unencrypted and separate from the pinned SSH connection. Only a trusted wired LAN is suitable; pinning does not cryptographically authenticate Telnet or stop an active on-path attacker targeting that transport.
6. The boot-ID interface and complete prerequisite/policy probes need live validation. No substitute unknown path or guessed boot hook is used. Vendor sysmgr can terminate Dropbear; restoration is eventual, not uninterrupted-session supervision.
7. The original Phase 6 client key must be protected or replaced; unencrypted keys are rejected. Same-user Windows malware can access the user's vault. Application/key/config ACL review is an installation prerequisite.
8. Damaged ownership markers or refused unmounts require original-root Telnet recovery inspection. No automatic reboot, force/lazy unmount, broad killall, persistent write or escalation is attempted. One controller configuration must not be copied across multiple PCs.

## Stop state

Phase 8 implementation and offline verification are complete. Local setup, real router restoration/rollback, Windows task installation and any reboot require owner authorization and were not performed. The [README](../../automation/README.md) gives exact command effects, recovery procedures and the opt-in live test. No Phase 9 work began.
