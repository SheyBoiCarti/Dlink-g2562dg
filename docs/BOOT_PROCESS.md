> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 7: boot process investigation

Read-only live inspection on 2026-10-19, firmware `TK_1.00TK_V1.2.12ak_20221018`. Evidence: [live batch](../archive/raw-evidence/PHASE7_READONLY.json), [follow-up](../archive/raw-evidence/PHASE7_FOLLOWUP.json), [prior binary analysis](../archive/raw-evidence/PHASE5_BINARY_ANALYSIS.json). Script contents describe configured behavior; no reboot or boot trace was performed.

## Boot chain and evidence boundaries

1. Bootloader loads kernel/rootfs: exact bank selection, bootloader environment and recovery behavior remain unverified. Kernel command line is `mem=110M console=ttyAMA1,115200 root=mtd:rootfs ro rootfstype=jffs2`.
2. PID 1 is `/bin/busybox`, reached through `/sbin/init` symlink. `/etc/inittab` specifies `console::sysinit:-/etc/rc.d/rcS`, `ttyAMA0::respawn:-/bin/sh`, shutdown script and disabled Ctrl-Alt-Del action. The difference between kernel ttyAMA1 and inittab ttyAMA0 is verified configuration, not verified physical UART wiring.
3. `rcS` exports vendor PATH/library paths; mounts proc, sysfs, RAM `/dev`, `/mnt`, `/tmp`; creates `/tmp/var`, runtime directories, device nodes and devpts. It loads hardware/network/acceleration modules, programs hardware through fixed vendor commands, sets VM values, invokes `histart`, brings loopback up, invokes `sys.init.sh`, then dongle reset and `/bin/sh`. These are inspected instructions, not commands executed during Phase 7.
4. `histart` creates br0/br1, assigns initial 192.168.1.1/192.168.253.1 addresses and brings eth0 up; current LAN is subsequently configured as 10.0.0.2. `sys.init.sh` prepares RAM state/account data, invokes vendor ebtables/firewall setup and starts `tdsmgr &`. Credential-generating lines were not collected. Exact intermediate configuration initialization inside tdsmgr remains partially traced.
5. tdsmgr contains the fixed command `sh /usr/syscfg/sys.init_after.sh`, corroborating prior investigation. The after script starts `sysmgr`, `srvcmgr`, `utils`, `neighevent`, uhttpd, mdev setup, ramonitor and VLAN policy. Several run in parallel: script order does not guarantee their completion order.
6. `sysmgr` controls SSH and Telnet services. Current SSH settings are Enable=1, Port=22. Prior live-binary analysis identifies host-key generation and `killall dropbear` stop/update paths. Current argv is `dropbear -r /var/dropbear/rsa_host_key -p 22`; current Telnet is `telnetd -l /usr/sbin/ams_cli -p 23`.
7. `utils` contains `mount -t jffs2 /dev/mtdblock7 /data`; the matching mount exists. The exact call/conditional error handling and its ordering against SSH initialization were not newly disassembled. `/data` readiness must therefore be tested explicitly by any future launcher, not assumed from the after-script position.

## Storage and overlay behavior

The effective `/` mount is `mtd:rootfs` JFFS2 **ro**. The additional `rootfs / rootfs rw` record does not make the overlying JFFS2 writable. `/data` is `/dev/mtdblock7` JFFS2 rw, 2048 KiB total, 1512 KiB available at this sample. `/var -> /tmp/var`; `/etc/passwd` and `/etc/group` point into `/var`. `/etc` itself remains on rootfs. `/tmp`, `/mnt`, `/dev` and devpts are volatile mounts.

`/overlay` exists as a directory but is not mounted; `/rom` is absent. `/proc/filesystems` does not currently list overlay/overlayfs; module availability was not exhaustively established. No active union overlay or automatic data-to-root substitution was observed.

## Candidate hooks checked

- Complete rcS, inittab, histart and after-script contents were inspected. No `/data` user-script call appears.
- Bounded recursive searches of `/etc/rc.d`, `/etc/init.d`, `/usr/syscfg`, hotplug dispatcher and `/lib/preinit` found `/data/log/debug.txt` copying in TR-069 diagnostics, not autorun. Results were limited to 100 lines; returned matches were below that bound.
- `/etc/rc.local`, Dropbear init/config and `/data/ssh` are absent. Cron files are shipped but prior live inspection found empty rootfs crontabs and no crond.
- `/usr/syscfg/ScriptFiles` contains fixed rootfs scripts, not a `/data` consumer. Searching management binaries for matching path strings found no new consumer; negative strings searches are not exhaustive control-flow proof.
- USB/mdev paths inspected in Phase 6B mount media and invoke vendor backup/media helpers; no user autorun was established. No helper was executed.
- Shipped `/lib/preinit` extroot files register `preinit_mount_root` callbacks and depend on preinit helpers/configuration. `/etc/preinit`, `/init` and `/sbin/mount_root` did not appear in the live listing; `/sbin/init` is BusyBox and active inittab goes directly to rcS. No active caller or mounted external root was found. These files are insufficient evidence for supported extroot boot on this build. Running them would perform writes/mount changes and was not attempted.

## Conclusion

The main configured boot path is traced through vendor service startup, with proprietary initialization and bootloader details explicitly unresolved. No supported arbitrary `/data` script execution or active overlay bootstrap is established. Full negative proof over all firmware behavior is not claimed. A future custom launcher needs an existing verified consumer or an approved persistent change to the boot path; a RAM bind/chroot alone cannot supply reboot execution.
