> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 3 execution plan

## Completed continuation

- [x] Resume from existing Phase 3 results without repeating earlier reconnaissance.
- [x] Inspect both SSH clients' effective configuration, user/global trust locations, known_hosts backup and PuTTY/WinSCP caches read-only; no prior matching trusted record found.
- [x] Assess independent sources using prior authenticated UI evidence and targeted vendor/ISP searches; no independent fingerprint source established.
- [x] Compare the live prompt with the exact prior fingerprint, obtain explicit TOFU approval, and record the approved public key locally. Strict checking preserved; no blind yes entered.
- [x] Use secure local askpass for a single configured password-method attempt; record Permission denied and offered publickey,password methods. Stop further credential attempts.
- [x] Preserve earlier evidence, update current results/root assessment/readiness and verify local report links and required artifacts. Conditional shell diagnostics were correctly skipped because no shell opened.

Current conclusion: Phase 3 has documented authentication failure (Outcome D). No authenticated username, UID or Linux runtime established. The password dialog contents/cancellation status were not logged, so rejection reason is not inferred. No router changes or Phase 4 action. The client public known_hosts entry is the only intentional persistent change, explicitly approved by the user.

## Historical initial execution plan (preserved)

The user-supplied Phase 3 specification authorizes bounded SSH authentication and read-only investigation. No changes, escalation, persistence implementation, Telnet passwords, firmware operations or hardware access.

- [x] Read Phase 1 research, Phase 2 results and authenticated follow-up.
- [x] Establish current SSH reachability and normal transport outcome without credentials.
- [x] Apply only observed per-connection compatibility requirements and retain strict host-key verification.
- [x] Document independent host-key-verification blocker; no credentials attempted because trust could not be established. User question pending. Authentication and conditional router diagnostics remain pending for a resumed investigation, not claimed completed.
- [x] Prepare review-gated, read-only, privacy-filtered shell diagnostics and offline safety tests. Not uploaded or executed on router.
- [x] Document actual outcomes, unknowns and Phase 4 recommendation; preserve historical findings and verify all nine deliverables and local links.

Implementation choice: POSIX shell for optional diagnostics, using awk to summarize mounts and suppress arbitrary mount options/source identifiers. Identity/kernel/CPU and known service summaries only; no raw process arguments, environment dumps, account databases, private keys or configuration exports. Review the complete script before `--reviewed`. It is for an already authenticated POSIX shell, not a restricted CLI.

Final verification: all five offline tests and Bash syntax check pass. Independent review confirmed evidence qualifications; its capacity-query finding was fixed by restricting df to recognized local mounts, with a passing local/network mount regression test. All nine required artifacts exist and local links resolve. No router diagnostics executed. Documentation and preparation are complete; actual authentication and conditional runtime objectives remain blocked on independent host-key verification and are not claimed complete.
