> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7: persistence decision

No supported autonomous persistence mechanism satisfying unchanged read-only rootfs has been verified. Flashing custom firmware is not proven necessary: a minimal stock boot-file edit is plausible but violates this phase's constraints and remains unvalidated. No persistence was implemented. See [boot trace](BOOT_PROCESS.md), [host keys](SSH_HOST_KEYS.md), [recovery](RECOVERY.md) and [results](../archive/phase-history/PHASE7_RESULTS.md). Historical Phase 6A PTY failures below were resolved in Phase 6B through maintained client stdin.

## Ranked approaches

Rank favors reversibility and current evidence; none is a ready autonomous installer.

| Rank | Approach / evidence | Prerequisites and risks | Recovery |
|---|---|---|---|
| 1 | External trusted LAN host reapplies proven RAM chroot after boot; automation untested | Retained Telnet; separate runtime-change approval; secure credential handling and public host verification; external host dependency; sysmgr may kill daemon. This is not autonomous router persistence | Stop automation; scoped Phase 6 rollback from original-root Telnet; unmount owned targets before deleting RAM tree |
| 2 | Minimal stock boot-script invocation of `/data/ssh` launcher; plausible without image flashing | Revised rootfs-write authorization; safe write method, exact-build recovery, data retention, stable identity, single service owner. Mount ordering/NAND safety/lifecycle untested | Restore exact baseline startup file through retained Telnet, stop owned processes and unmount before deleting owned files; boot failure recovery currently unverified |
| 3 | Vendor-supported configurable hook, if discovered | No such consumer identified; Enable/Port do not supply custom argv/key paths. Needs exact-build vendor evidence | Supported inverse settings; config export is not a rootfs backup |
| 4 | USB/extroot/overlay | Shipped callbacks lack established active caller; no mounted overlay; enabling may itself require boot changes. Media failure/root substitution risk | Removing USB is not a proven fallback; validate original-root recovery first |
| 5 | Modified firmware or bootloader | Excluded now; exact-build image and NAND/ECC/bad-block-aware recovery required; not proven necessary | Validated exact-build restoration, currently unavailable |

Configuration injection, library hijacking and guessed log/USB autorun are not supported mechanisms and are not proposed.

## Proposed mechanism, not implemented

If constraints are revised, use a minimal fixed invocation in the existing after-script and a private `/data/ssh` launcher. This is a proposed new call, not a discovered hook. The launcher would wait a bounded time for the expected JFFS2 mount and LAN address, validate UID-0 ownership/private modes/non-symlink paths, recreate the proven six-bind RAM chroot and supply the validated public authorized key at the vendor-required path. It must return promptly, fail closed and preserve vendor startup and Telnet. No launcher was created.

Before writes: resolve safe rootfs editing and exact-build recovery; establish `/data` cleanup/reset retention; approve exact files and inverses; protect client key and server identity. Stable host identity needs an explicitly approved protected backup/restore design. Decide one SSH owner: original stock argv has password authentication and wildcard binds; sysmgr's killall can terminate custom daemons. Do not assume a disabled setting isolates a replacement. Review vendor events and any supervisor before replacing the original port-22 service. Explicit LAN bind, key-only flags, forwarding disablement and both-family ingress policy need separate reviewed changes.

Then obtain explicit persistent-write/service/mount/network approval and separate reboot approval. Validate strict host identity, two independent UID-0 PTY sessions, expected binds/listener ownership, retained web/Telnet recovery and relevant vendor service updates. Repeated controlled reboot validation precedes any Telnet retirement. None of these deployment gates has passed here.

Rollback before reboot: restore exact original startup-file baseline, restore original service settings, stop only verified owned processes, unmount only owned scratch descendants, and remove only positively identified new files. Never delete through a bind mount or use broad killall. Keep protected identity backups. A boot failure cannot currently be promised recoverable. Factory reset is not an established rollback.

## Historical Phase 5-6B record

# Phase 5: persistent key-only SSH proposal

## Phase 6B decision: interactive proof passed; autonomous persistence blocked

The approved RAM-only chroot test now supports interactive UID 0 SSH. The old failure was client stdin handling, not missing kernel PTYs. See [PTY diagnostics](SSH_PTY_DIAGNOSTICS.md) and [execution evidence](../archive/raw-evidence/PHASE6B_EXECUTION.json). Temporary files/mounts/listener were removed afterward. Original service configuration and host identity were unchanged.

**A persistence implementation is not ready under the current constraints.** Read-only rootfs, no stock startup edits, no original Dropbear/host-key changes, no duplicate permanent listener and retained host identity across reboot cannot currently be combined using a verified mechanism. This is a bounded research result, not proof that every vendor feature is incapable of supporting a hook. No deliberate permanent provisioning writes or reboot were approved or attempted. Ordinary vendor login/logging activity may still update its own logs.

### Storage is not startup integration

Live `/data` is `/dev/mtdblock7`, JFFS2, rw, 2 MiB total; the new sample had 1516 KiB available. Its existing `log` directory has unusual mode 0644; do not reuse or repair it for SSH. A separate root-owned `/data/ssh` mode 0700 with a public `authorized_keys` file mode 0600 is the conservative storage design. Verify real mount, ownership, no symlinks and retention policy before creating it. No `/data/ssh` was created in this phase; retention, log cleanup, factory reset and reboot survival remain untested. A public key is not confidential, but modification permits root access.

The actual UID 0 lookup remains `/etc/dropbear/authorized_keys`, absent on read-only `/`. A file in `/data/ssh` will not be consumed by the original daemon automatically. Phase 6A/6B proved a RAM chroot can supply that path with no stock-rootfs writes. Its success does not turn `/data` into an executable boot hook.

### Existing mechanisms inspected

Evidence: [boot/device inspection](../archive/raw-evidence/PHASE6B_BOOT.json), [hook follow-up](../archive/raw-evidence/PHASE6B_FOLLOWUP.json), prior [Phase 5 binary analysis](../archive/raw-evidence/PHASE5_BINARY_ANALYSIS.json).

- BusyBox inittab starts rcS; vendor init launches tdsmgr and sys.init_after.sh. The inspected active scripts reside on read-only rootfs. No configurable `/data` script invocation was established.
- `/etc/rc.local` is absent. `/etc/crontabs` is empty and read-only-rootfs-backed; no active crond was found. The shipped cron init file does not establish boot execution.
- Kernel hotplug points to `/sbin/mdev`; mdev configuration is generated by a stock script. USB automount invokes fixed vendor mounting/media/config-backup helpers. The inspected scripts do not execute a user autorun script from USB or `/data`. Do not run these scripts manually as a test: they perform mounts, configuration changes and service operations.
- A bounded `/data` reference search in rc.d/init.d/syscfg returned a debug-log copy in tr069_proc.sh, not a startup hook. One earlier wrapped grep capture was unusable and was repeated; only the later targeted result supports this statement.
- sysmgr's observed SSH configuration supports Enable/Port and starts `dropbear -r /var/dropbear/rsa_host_key`; no authorized-key or arbitrary-startup setting was established. Runtime service updates can `killall dropbear`, including a separately launched instance.

### Host identity and single-listener design gates

Both successful phases reused the existing host key read-only; its fingerprint is unchanged. `/var` is RAM, and sysmgr's initializer generates the host key there. Preserving the current identity after reboot would require a verified persistent host-key provision/restore path. None was found. Backing up or restoring a private host key would itself require a separately approved protected procedure; it was not done. Never silently accept a new key or overwrite the original to make a reboot test pass.

A final deployment should have exactly one intended SSH service on port 22, with the original host identity, public-key-only authentication and forwarding disabled. The temporary 2222 listener was necessary to test without changing original service ownership, and is now gone. Replacing the port 22 process or giving it a global alternate `/etc` view requires separate service/mount approval and vendor-lifecycle validation; neither is recommended as ready. Do not start another daemon on occupied port 22 or use `killall`.

### Exact commands available for review, not deployment authorization

The following is **public-key storage staging only**, not a persistence installer. It must be separately approved and supplied exactly one previously validated public key in `CLIENT_PUBLIC_KEY`; do not put a private key or credential in this variable. Confirm the expected public fingerprint locally before transfer. Refuse an existing destination instead of overwriting it.

```sh
test "$(id -u)" = 0 || exit 1
awk '$2=="/data" && $1=="/dev/mtdblock7" && $3=="jffs2" && $4 ~ /(^|,)rw(,|$)/ {ok=1} END {exit !ok}' /proc/mounts || exit 1
test -d /data && test ! -L /data || exit 1
test ! -e /data/ssh && test ! -L /data/ssh || exit 1
# Manually verify /data is UID/GID 0 and not group/other writable first.
test -n "$CLIENT_PUBLIC_KEY" || exit 1
umask 077
mkdir /data/ssh || exit 1
printf '%s\n' "$CLIENT_PUBLIC_KEY" > /data/ssh/authorized_keys.new || exit 1
awk 'NR!=1 || $1!="ssh-rsa" {bad=1} END {exit (bad || NR!=1)}' /data/ssh/authorized_keys.new || exit 1
chmod 700 /data/ssh || exit 1
chmod 600 /data/ssh/authorized_keys.new || exit 1
mv /data/ssh/authorized_keys.new /data/ssh/authorized_keys || exit 1
```

The awk check validates line shape, not the cryptographic key; deploy only the exact previously validated public line and compare content/fingerprint afterward. On error preserve/inspect the newly created directory; use reviewed rollback, not broad recursive deletion. Flash writes incur wear even if removed. There is deliberately **no fabricated boot-hook command**: an exact autonomous startup implementation cannot be supplied until its consumer and host-key handling are verified.

The tested runtime commands and exact six mounts are retained in [Phase 6A setup](../scripts/phase6a_setup.sh); [rollback](SSH_ROLLBACK.md) is tested. Reexecution needs approval. For a future data-backed runtime test, read and validate `/data/ssh/authorized_keys` and copy only that public file into the owned RAM chroot; no new bind to `/data` is necessary. That variation has not been executed.

### IPv4 and IPv6 policy

The test bound only `10.0.0.2:2222`, created no IPv6 socket and changed no firewall rule. Address binding alone is not an ingress-interface firewall guarantee; IPv4 INPUT is DROP with br0 accepted, but earlier chains and routing still matter. Original port 22 remains wildcard on both families. IPv6 INPUT is ACCEPT, with lo/br0 and established traffic accepted in its service chain; link-local addresses are not a durable protection policy. Full management protection is **not established**.

A future reviewed firewall design should place an SSH-specific chain before general accepts for **each** family, return for lo/br0, and drop other ingress. A concrete candidate, **not applied or lifecycle-tested**, is:

```sh
# First require that DLINK_SSH_LAN is absent in BOTH families.
# Execute one command at a time and stop/review any error.
iptables -N DLINK_SSH_LAN
iptables -A DLINK_SSH_LAN -i lo -j RETURN
iptables -A DLINK_SSH_LAN -i br0 -j RETURN
iptables -A DLINK_SSH_LAN -j DROP
iptables -I INPUT 1 -p tcp --dport 22 -j DLINK_SSH_LAN
ip6tables -N DLINK_SSH_LAN
ip6tables -A DLINK_SSH_LAN -i lo -j RETURN
ip6tables -A DLINK_SSH_LAN -i br0 -j RETURN
ip6tables -A DLINK_SSH_LAN -j DROP
ip6tables -I INPUT 1 -p tcp --dport 22 -j DLINK_SSH_LAN
```

Returning preserves the vendor's subsequent lo/br0 policy; it does not independently permit traffic. Verify counters and access from LAN and a non-LAN path in each family. Partial application needs immediate inspection and exact inverse removal, not global flushing. These rules do not secure HTTP, FTP or Telnet and are not reboot-persistent. Prefer an explicit LAN address listener plus both-family ingress policy; verify web/Telnet recovery separately. Vendor regeneration and startup ordering must be addressed before calling policy persistent. See [rollback](SSH_ROLLBACK.md).

### Remaining implementation gates

1. Protect the local client private key with a passphrase before ongoing deployment; current test key is ACL-restricted but unencrypted.
2. Approve and verify only public-key staging in `/data`, including retention/cleanup policy and exact inverse removal.
3. Discover a supported existing startup consumer or explicitly revise the no-stock-rootfs-change requirement. External client re-provisioning is a separate operational approach, not autonomous router persistence, and must not embed Telnet credentials in scripts.
4. Resolve stable original host-key retention without violating the no-host-key-change rule, single-service ownership, and IPv4/IPv6 rule restoration.
5. Only then review implementation/rollback and request separate persistent-write/service/firewall/reboot approvals. Keep Telnet until independent reboot and lifecycle validation succeeds.

The historical Phase 5 proposals below include stock-rootfs edits and remain **incompatible with Phase 6B's current constraints**. They are preserved for history, not recommended for execution. See [Phase 7 readiness](../archive/phase-history/PHASE7_READINESS.md).

## Phase 6A temporary proof completed

After explicit approval, a separate RAM-backed chroot supplied the vendor key path through six bind mounts beneath `/tmp/dlink-phase6a`. Account data remained unchanged, and the existing host key was reused. A key-only Dropbear bound explicitly to IPv4 `10.0.0.2:2222`, with forwarding disabled. Two independent non-PTY connections authenticated using the dedicated RSA-3072 public key and returned UID 0. Interactive PTY validation failed after authentication; its cause remains unresolved.

The temporary daemon, all binds and RAM files were removed afterward. Original SSH/Telnet remained available, and fresh Telnet root recovery was verified. See [exact method, evidence and rollback](../archive/phase-history/PHASE6A_RESULTS.md). This proves temporary command access without changing stock rootfs contents; it does not provide a boot hook, stable host-key storage or persistent SSH. The client private key remained local, ACL-restricted but not passphrase-encrypted.

**Persistence remains unverified and unimplemented.** Sections below retain Phase 5 candidate designs for separate review and authorization. No persistent partition, startup configuration, account file or firewall rule was changed in Phase 6A.

## Constraints established on the device

- UID 0 SSH must use Unix `admin`; its key file is hard-coded to `/etc/dropbear/authorized_keys`.
- `/etc/dropbear` is absent, and the root JFFS2 filesystem is mounted read-only. A bind mount cannot target an absent directory; a symlink cannot be created there without changing the filesystem or mounting an alternate `/etc` view.
- `/var` and `/tmp` are RAM, not persistent storage. Current host keys are under `/var/dropbear`.
- `/data` is a writable 2 MiB JFFS2 **log** partition with about 1.44 MiB free at inspection. Persistence is inferred from flash backing, not reboot-tested. Log growth, cleanup/format behavior and confidentiality of future stored keys need review.
- `/etc/rc.local`, an active overlay, a Dropbear init script and a verified custom `/data` startup hook were not found. OpenWrt branding does not make normal UCI/rc.local recipes valid here.
- Vendor `sysmgr` launches Dropbear with config-managed Enable/Port, and service updates can kill every process named Dropbear. A one-time manual hardened launch can later be undone or terminated by the vendor lifecycle.

## Candidate mechanisms and verdict

| Mechanism | Assessment |
|---|---|
| Add `~/.ssh/authorized_keys` | Wrong location for this vendor UID 0 implementation |
| Put keys/scripts only in `/var` | Volatile; no boot restoration established |
| Put files only in `/data` | Flash-backed but not automatically consumed or executed |
| Add `/etc/config/dropbear` / `/etc/rc.local` | Files absent and no active consumer verified |
| RAM copy/bind of `/etc` | Could permit a temporary key test without flash writes, but affects every service using `/etc`; requires explicit approval, exact symlink/mode preservation and rollback. Not tested |
| One-time JFFS2 changes for `/etc/dropbear` and a boot hook | Concrete candidate without replacing a firmware image, but **does modify stock rootfs contents**; requires NAND recovery gates and a separately approved scope |
| Separate modern SSH executable | Could avoid some vendor limitations, but introduces ABI/storage/startup work and additional software; outside Phase 5 and not the preferred initial route |

No zero-write route to installing a public key exists in the evidence. No guaranteed persistent solution can be claimed under a requirement that the stock root filesystem remain completely untouched.

## Proposed staged plan for separate approval

### 1. Recovery and design gates

Complete [RECOVERY.md](RECOVERY.md): preserve the existing configuration export, refresh it if appropriate, back up exact files targeted for edits, choose protected host-key backup/rotation handling, and resolve exact-build/NAND recovery. Review `/data` log cleanup and mount timing. Keep a working Telnet root session and web administration throughout testing. Do not disable either early.

Decide explicitly whether one-time stock-rootfs file changes are acceptable. “No firmware replacement” and “no rootfs modification” are different constraints. If rootfs edits are unacceptable, stop short of promising autonomous persistence; a RAM-only proof or alternate supported provisioning path needs its own design.

### 2. Temporary public-key proof

After approval for a specific temporary filesystem arrangement, install **only a client public key** at the vendor's required path, owned by UID 0 with directory/file modes 0700/0600. Do not edit passwd/shadow or change the existing UID 0 home.

The historical Phase 5 candidate below is superseded by the executed chroot command in the Phase 6A report:

```text
/usr/sbin/dropbear -r /var/dropbear/rsa_host_key -p 10.0.0.2:2222 -s -j -k -P /var/run/dropbear-phase6.pid
```

Every listed flag was confirmed in the live help. This command still writes a PID file and starts a service, so requires approval. Its key-file prerequisite is not solved merely by this command. Avoid `-R`, which creates keys, and avoid `-w`, which rejects the intended UID 0 account.

Use a dedicated RSA client key and pin the verified host fingerprint. Scope the legacy algorithm exceptions to this host, including `PubkeyAcceptedAlgorithms=+ssh-rsa` only if required for the RSA authentication signature. Require publickey only, disable agent fallback and passwords in the test client, and verify `id -u` returns 0 over the actual SSH connection. Test a second connection before closing the first. Remove the test service and undo temporary mounts/files using the approved rollback.

### 3. Persistent files and boot integration, only after another approval gate

If recovery and rootfs-edit approval are satisfied, a concrete candidate layout is:

```text
/data/ssh/authorized_keys      public client key only, mode 0600
/data/ssh/rsa_host_key         chosen persistent host identity, mode 0600
/data/ssh/start.sh             small reviewed idempotent launcher, mode 0700
/etc/dropbear -> /data/ssh     new rootfs link, only if approved
```

All directories/files must be UID 0, private from group/other write/read as appropriate. The host key is a private **server identity**, not the client private key. Preserve or deliberately rotate its identity with a protected backup and explicit client trust procedure; never repeatedly generate it at each boot.

The candidate existing boot integration point is `/usr/syscfg/sys.init_after.sh`: it is called by live `tdsmgr`. A minimal reviewed addition could invoke the launcher after verifying `/data` is the expected JFFS2 mount. This is a proposed modification, not a discovered custom hook. The root mount's `ro` mode must not be changed until explicitly approved; exposed MTD write capability does not establish safe remount behavior.

The launcher would need bounded mount/address waits, strict ownership checks, a stable host key, key-only authentication and an explicit LAN bind. It must not mount an untrusted USB device or execute arbitrary log content. The init call and `/data` mount happen through different vendor components; ordering and service-update races remain unresolved and must be tested before adopting this hook.

### 4. Service ownership and network restriction

Do not just kill the existing daemon and assume a hardened replacement will survive. Decide how the supported `ServiceSSH.Enable` setting and the custom launcher interact. A candidate is disabling the vendor-managed instance through its normal configuration **only after** the new key-only instance is proven, then making the new launcher solely responsible for SSH. `sysmgr` stop/update uses `killall dropbear`, so subsequent configuration changes may terminate a custom instance too; this lifecycle must be verified, with a reviewed supervisor/restart policy if necessary. Port 22 migration is a separate step from the port 2222 proof.

For binding, prefer the verified `-p 10.0.0.2:<port>` syntax. This listens on the specific IPv4 address and avoids a wildcard IPv6 socket. Addresses and interfaces must be validated at startup; do not silently fall back to wildcard binding if the LAN address changes.

Firewall policy must additionally restrict ingress to the intended trusted LAN interface/subnet. Current IPv4 INPUT is DROP and `service_list` accepts `br0`, but IPv6 INPUT is ACCEPT with no observed deny on non-LAN new input. Only loopback/link-local IPv6 addresses were present. Lack of a global address today does not guarantee future isolation. Check both IPv4 and IPv6, guest/secondary bridges and later provisioning changes; no WAN reachability test or firewall edit occurred in Phase 5.

### 5. Persistence validation and retirement of Telnet

Only after explicit reboot authorization: verify fixed host identity, expected argv/listen addresses, password-auth disabled, successful key-only UID 0 login and continued web recovery across a controlled reboot. Exercise service/config changes that could recreate or kill Dropbear. Test non-LAN denial through a separately approved observation point.

Disable Telnet through its supported vendor service control only after repeated independent SSH reconnects, the approved reboot test, and a viable rollback path. Removing Telnet first would discard the only currently verified root recovery channel. Physical UART remains electrically unverified. No Telnet-disable change or reboot is authorized by Phase 5.

## Readiness outcome

Ready for a **separately scoped temporary key-authentication design/test**, once its exact filesystem writes and rollback are approved. **Not ready to assert safe unattended persistence or disable Telnet.** Rootfs edits, host-key retention, log-partition suitability, boot ordering and vendor service ownership remain material implementation gates, not minor details to guess.
