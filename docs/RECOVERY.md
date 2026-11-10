> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7 recovery update

Read-only Telnet login again reached UID 0; shell and CLI closed normally. Fresh evidence confirms root JFFS2 ro, original SSH/Telnet PIDs 3244/1037 and listeners, no port 2222/test tree/global key directory, and unchanged public host fingerprint. No reboot, persistent provisioning, package, startup, service or firewall change occurred. Ordinary vendor login/logging may update its own files.

The [tested RAM rollback](SSH_ROLLBACK.md) requires original-root Telnet and scoped process/mount checks. Reexecution needs separate approval. External reprovisioning can be stopped and its RAM state cleaned; it does not provide autonomous persistence.

Future persistent rollback needs exact startup baseline restoration, original service configuration, owned process/mount cleanup and protected host-key handling. Preserve Telnet; do not use reboot as the first cleanup action. A nonblocking launcher reduces risk but does not establish boot recovery. Factory reset may erase ISP/network settings and has unverified data-retention behavior. Bootloader/UART, exact installed firmware and NAND restore remain unverified; stock boot-file backups alone do not make a failed boot recoverable. No flashing, bank switching or raw MTD operations are authorized.

See [boot findings](BOOT_PROCESS.md), [ranked options](SSH_PERSISTENCE.md) and [host identity](SSH_HOST_KEYS.md). Historical backup details follow; no private-key backup was acquired in Phase 7.

# Phase 5: backup, recovery and rollback assessment

No restore, reboot, flash operation or router write was performed. Recovery is not established merely because the current shell has UID 0.

## Backups actually available

| Artifact | Verified status and scope |
|---|---|
| Existing configuration export | `router-config.bin`, 1,416,545 bytes, integrity rechecked against the prior acquisition record; not a firmware/rootfs backup |
| Current boot-file baselines | Exact read-only downloads of `/etc/inittab` (292 bytes), `/etc/rc.d/rcS` (7678 bytes) and `/usr/syscfg/sys.init_after.sh` (274 bytes); each inventoried with a local SHA-256 digest |
| Live service executables for analysis | Dropbear, `sysmgr`, `srvcmgr` and `ams_cli` copies were inspected offline; not a complete restore set |
| Official older firmware | `ak_20210420` image retained with provenance; **not** the installed `ak_20221018` recovery image |

The configuration export and boot baselines reside outside OneDrive:

```text
<WORKSPACE_OR_USER_HOME>\AppData\Local\DLinkResearch\private\20261019-195059\
    router-config.bin
    decoded-base64.bin
    phase5-baseline\manifest.json
    phase5-baseline\etc__inittab
    phase5-baseline\etc__rc.d__rcS
    phase5-baseline\usr__syscfg__sys.init_after.sh
```

The baseline directory inherits access only for the current Windows user and SYSTEM from its restricted parent; ACLs were inspected. No backup credential values were printed. Configuration files contain secrets and must not be uploaded, emailed, committed or copied into the project. The boot baselines exclude the credential-bearing account-generation script. No `/etc/passwd`, `/etc/shadow`, authorized key or private host key was copied into these baselines.

`/etc/rc.d/rc.shutdown` was confirmed to be a zero-byte file. An attempted Base64 transfer did not match the collector's nonempty-payload framing; no successful backup of it is claimed. The three boot-file baselines and manifest were separately verified. Phase 5 observations are also redacted evidence, not a substitute for exact backups.

## What is still missing

- A provenance-checked exact installed firmware/recovery image or verified equivalent restore procedure.
- A tested bootloader recovery procedure; no bootloader interruption or recovery mode was attempted.
- Verified physical UART pinout, voltage and electrically safe access. Software console settings do not establish hardware wiring.
- An approved, protected host-key backup if its identity will be relocated or replaced. Phase 5 extracted only public fingerprint information.
- A validated NAND dump/restore procedure with partition offsets, active-bank mapping, ECC, OOB and bad-block handling. Only geometry and named MTD views are known.
- A tested configuration restore; the export is intact but restoring it could alter network/ISP settings and reboot the device. It is not permission to restore now.

The MTD layout includes overlapping `all`, `html`, kernel and backup views. Do not add their sizes, infer offsets from numbering, or assume a backup bank automatically recovers a bad edit. NAND is not a simple NOR byte array. A raw `dd` read from an MTD block view is not by itself a complete bad-block/OOB-aware recovery image, and writing such a file back is not a validated restore procedure. No flash-dump utility was installed or executed.

## Rollback requirements for a future temporary SSH proof

Before any approved test, record exact original paths, symlinks, owners and modes and the current service PID/argv/listeners. Keep Telnet root and web access open. Scope cleanup to the test daemon's verified PID and files; avoid `killall dropbear`.

For a RAM-only `/etc` copy/bind design, first review how every symlink and device/runtime reference is preserved. Rollback must be an explicit unmount of the temporary view followed by inspection that the original read-only `/etc` is visible. Do not assume unmount succeeds while services hold references. No such temporary mount was attempted here.

Do not treat reboot as the default rollback for an untested boot hook: a broken hook can make reboot the point at which access is lost. A temporary proof should have a cleanup path that works from the retained root shell without rebooting.

## Rollback requirements for persistent rootfs edits

Any proposal to create `/etc/dropbear`, edit a boot script, persist a host key or change a service must enumerate the exact changes and inverse operations for approval. Before writing, acquire restorable backups for those specific files and protected key material, resolve NAND recovery, confirm free space/log behavior and inspect the files' true backing mounts.

If rootfs edits are approved later, restore the exact boot script from its verified baseline rather than reconstructing it from documentation. Remove only newly introduced links/files after verifying their identity; preserve original host identity and vendor configuration values. Restore initial permissions and read-only mount state, then verify Telnet/web and the original SSH listener policy. This is a rollback specification, not a tested sequence or authorization to remount.

Persistent boot modifications are **not presently cleared as low risk**. A backup of three boot files cannot recover an erased partition or a device that no longer reaches a shell. Retain Telnet until independent key-only SSH persistence and a separate recovery path have passed their explicitly authorized tests.
