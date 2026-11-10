> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Root access assessment — Phase 3

## Superseding verified outcome

The owner's later authorized investigation obtained **UID 0 Linux access** through Telnet, a firmware-derived built-in CLI account and the normal `sh` command. Actual output: `uid=0(admin) gid=0(admin)` and `Linux 3.14.18 armv7l`. See [reproduction and evidence](../findings/ROOT_ACCESS_VERIFIED.md). No firmware/configuration modification was needed. Earlier assessments below reflect their original phase boundaries.

## Phase 3B alternative-access update

No new Linux shell or root access. Telnet now confirms a D-Link ams_cli frontend at LOGIN#, but nothing establishes post-login shell privileges. FTP exposes metadata while requiring authentication for SYST/PWD/HELP; no filesystem access. The UART root claim is the strongest root-specific community lead, with electrical and exact-build details still unverified. See [Phase 3B results](../archive/phase-history/PHASE3B_RESULTS.md). No login guessing, shell escape, exploit, configuration change or hardware interaction.

## Preserved Phase 3 assessment

## Current classification: Outcome D — authentication failure

After explicit TOFU approval and strict saved-key matching, the single password-method attempt returned `admin@10.0.0.2: Permission denied (publickey,password).` The server offers publickey and password. No authenticated account, shell or UID was established. This does not prove an invalid password or distinguish account restrictions; the local password dialog contents and cancellation status were not recorded.

Root access is **not confirmed**. No identity, operating-system, hardware, filesystem, process or service-startup commands were executed. No bypass, guessing or privilege escalation attempted. The previous host-key blocker is now resolved through user-approved TOFU, with first-use interception risk accepted rather than independently disproved.

The appropriate next objective is supported SSH account/CLI research, then possibly separately scoped offline exact-image analysis. No more login attempts in this phase.

## Historical pre-approval assessment (preserved)

**Root access is not confirmed. Authentication is blocked before credentials by an unverified host key.** Transport compatibility has a demonstrated per-connection workaround; identity trust remains unresolved.

| Requested outcome | Assessment |
|---|---|
| A: root shell | Not established; no `id` output |
| B: non-root shell | Not established; no authenticated session |
| C: restricted CLI | Not established; no authenticated session |
| D: authentication rejected | Not observed; no credential was sent |
| E: incompatible connection | Initial KEX mismatch observed; legacy KEX/host-signature options resolve it. Remaining blocker is host-key verification, not proof of incompatible transport or rejected credentials. |

No outcome is fabricated to fit the categories. Requested username `admin` is known, but accepted SSH username, effective UID, shell, root filesystem, kernel, CPU and privilege policy are unknown. Phase 2 web authentication remains valid evidence only for the web interface.

No privilege escalation attempted or recommended as an immediate next step. Resolve trusted host identification, then make the single bounded interactive credential attempt. If it fails, stop rather than guessing alternate accounts. If it yields UID 0, record that fact and stop before changes. If it yields a non-root shell or restricted CLI, stay within its normal permissions and documented commands.

Persistence feasibility is unknown. Do not add keys, alter startup/config, enable root login, install packages or reboot to test it. Existing service availability is not evidence of persistent root entitlement.
