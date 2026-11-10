#!/bin/sh
# Read this entire script before use. For an ALREADY AUTHENTICATED POSIX shell.
# No authentication, network requests, installation, router writes or changes.
# Do not upload it to the router without separate approval. Prefer individual
# commands. After review, it may be streamed over an existing trusted SSH
# connection with `sh -s -- --reviewed`; do not do this in a restricted CLI.
# This script is prepared only; it has NOT been executed on the router.

usage() {
    printf '%s\n' 'Review shell_diagnostics.sh first; then run: sh shell_diagnostics.sh --reviewed'
    printf '%s\n' 'Requires POSIX sh and awk. Existing authenticated shell only. No files written.'
}
if [ "$#" -ne 1 ]; then usage; exit 2; fi
case "$1" in
    --help) usage; exit 0 ;;
    --reviewed) ;;
    *) usage; exit 2 ;;
esac
if ! command -v awk >/dev/null 2>&1; then
    printf '%s\n' 'awk unavailable; aborting to preserve output filtering.' >&2
    exit 1
fi
export LC_ALL=C
section() { printf '\n=== %s ===\n' "$1"; }
available() { command -v "$1" >/dev/null 2>&1; }

section Identity
# Numeric identifiers avoid dumping supplementary account names.
if available id; then
    printf 'effective_uid='; id -u 2>/dev/null || printf 'unavailable\n'
    printf 'effective_gid='; id -g 2>/dev/null || printf 'unavailable\n'
else printf '%s\n' 'id unavailable'; fi
if available whoami; then
    whoami 2>/dev/null | awk '{if ($0=="root" || $0=="admin") print "user=" $0; else print "user=[other account; value withheld]"}'
else printf '%s\n' 'whoami unavailable'; fi
case "${SHELL-}" in
    /bin/sh|/bin/ash|/bin/bash|/bin/dash|/bin/rbash|/sbin/nologin|/bin/false)
        printf 'SHELL=%s\n' "$SHELL" ;;
    '') printf '%s\n' 'SHELL unset' ;;
    *) printf '%s\n' 'SHELL=[unrecognized path withheld]' ;;
esac
printf '%s\n' 'SHELL is an environment hint; it does not prove the active interpreter.'
if [ -n "${HOME-}" ] && [ -d "$HOME" ]; then
    printf '%s\n' 'HOME directory exists (path withheld)'
    if [ -w "$HOME" ]; then printf '%s\n' 'HOME permission check says writable; no write test'; fi
else printf '%s\n' 'HOME directory unavailable'; fi

section 'Kernel and architecture'
# Deliberately avoid uname -a/-n, which can disclose the hostname.
if available uname; then
    uname -srm 2>/dev/null | awk '{
        if ($1=="Linux" && $2 ~ /^[0-9][0-9A-Za-z._+-]*$/ && $3 ~ /^(armv[5-9][a-z0-9]*|aarch64|mips[a-z0-9]*|x86_64|i[3-6]86)$/) print;
        else print "Kernel/architecture format unrecognized; output withheld"
    }'
else printf '%s\n' 'uname unavailable'; fi

section 'Release metadata'
for file in /etc/os-release /etc/openwrt_release; do
    if [ -r "$file" ]; then
        printf '%s\n' "$file (selected fields)"
        awk -F= '
        $1 ~ /^(ID|NAME|VERSION_ID|PRETTY_NAME|DISTRIB_ID|DISTRIB_RELEASE|DISTRIB_CODENAME|DISTRIB_TARGET)$/ {
            val=substr($0,index($0,"=")+1); gsub(/"/,"",val);
            if (length(val)<=100 && val ~ /^[A-Za-z0-9 ._\/+()-]+$/ && val !~ /[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/)
                print $1 "=" val;
            else print $1 "=[value withheld]"
        }' "$file" 2>/dev/null
    else printf '%s unavailable\n' "$file"; fi
done

section 'CPU (numeric fields only; serial and host identifiers omitted)'
if [ -r /proc/cpuinfo ]; then
    awk -F: '
    $1 ~ /^CPU (architecture|implementer|part|variant|revision)[ \t]*$/ {
        key=$1; val=$2; gsub(/^[ \t]+|[ \t]+$/,"",key); gsub(/^[ \t]+|[ \t]+$/,"",val);
        if (val ~ /^(0x[0-9a-fA-F]+|[0-9]+)$/ && !seen[key,val]++) print key ": " val
    }
    END {print "SoC name not inferred from CPU numeric fields"}' /proc/cpuinfo 2>/dev/null
else printf '%s\n' '/proc/cpuinfo unavailable'; fi

section BusyBox
if available busybox; then
    busybox 2>&1 | awk '
    match($0,/BusyBox v[0-9]+\.[0-9]+(\.[0-9]+)?/) {print substr($0,RSTART,RLENGTH); found=1}
    END {if (!found) print "BusyBox present; version not recognized"}'
    printf '%s\n' 'Common diagnostic applets available:'
    for tool in sh ash id whoami uname awk cat mount df ps readlink opkg; do
        if busybox --list 2>/dev/null | awk -v wanted="$tool" '$0==wanted {ok=1} END {exit !ok}'; then printf '%s\n' "$tool"; fi
    done
else printf '%s\n' 'BusyBox not found in PATH'; fi

section 'Mounts (no source identifiers or arbitrary mount options)'
mount_summary() {
# BEGIN MOUNT FORMATTER
awk '{
    target=$2;
    if (target !~ /^\/(|rom|overlay|tmp|proc|sys|dev|dev\/pts|var|run|mnt|data|config)$/) target="[other mountpoint]";
    type=$3;
    if (type !~ /^(squashfs|jffs2|ubifs|overlay|overlayfs|tmpfs|ramfs|rootfs|proc|sysfs|devpts|devtmpfs|ext[234]|vfat|cifs|nfs|debugfs|mqueue|pstore|fuseblk)$/) type="[other type]";
    mode="unknown"; n=split($4,opts,",");
    for (i=1;i<=n;i++) if (opts[i]=="ro" || opts[i]=="rw") mode=opts[i];
    print target, type, mode
}'
# END MOUNT FORMATTER
}
if [ -r /proc/mounts ]; then mount_summary < /proc/mounts
else printf '%s\n' '/proc/mounts unavailable'; fi
printf '%s\n' 'rw is a reported mount flag, not a write test or reboot-survival guarantee.'

section 'Filesystem capacity (KiB; source identifiers omitted)'
local_capacity_targets() {
# BEGIN LOCAL CAPACITY TARGETS
awk '$3 ~ /^(squashfs|jffs2|ubifs|overlay|overlayfs|tmpfs|ramfs|rootfs|ext[234]|vfat)$/ &&
     $2 ~ /^\/(|rom|overlay|tmp|dev|var|run|mnt|data|config)$/ {if (!seen[$2]++) print $2}'
# END LOCAL CAPACITY TARGETS
}
if available df && [ -r /proc/mounts ]; then
    # Never run df across all filesystems: network mounts can contact servers.
    local_capacity_targets < /proc/mounts | while IFS= read -r target; do
    df -Pk "$target" 2>/dev/null | awk '
    $2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ && $4 ~ /^[0-9]+$/ && $5 ~ /^[0-9]+%$/ {
        target=$NF;
        if (target !~ /^\/(|rom|overlay|tmp|proc|sys|dev|var|run|mnt|data|config)$/) target="[other mountpoint]";
        print target, "total=" $2, "used=" $3, "available=" $4, "use=" $5
    }'
    done
else printf '%s\n' 'df or local mount inventory unavailable; capacity skipped'; fi

section 'Known visible management processes (names only; never arguments)'
# Fail closed if this ps does not support comm-only output. No raw-ps fallback.
if available ps; then
    ps -o comm 2>/dev/null | awk '
    /^(dropbear|sshd|telnetd|vsftpd|httpd|uhttpd|lighttpd|nginx|dnsmasq|cwmp|cwmpd|tr069|tr069c|netifd|procd|init)$/ {if (!seen[$0]++) print}
    END {print "Only exact known process names retained; missing names do not prove absent services"}'
else printf '%s\n' 'ps unavailable'; fi

section 'SSH startup and package-manager hints'
if available dropbear; then
    location=$(command -v dropbear)
    case "$location" in
        /usr/sbin/dropbear|/usr/bin/dropbear|/sbin/dropbear|/bin/dropbear) printf 'Dropbear executable: %s\n' "$location" ;;
        *) printf '%s\n' 'Dropbear exists in PATH; path withheld' ;;
    esac
else printf '%s\n' 'Dropbear not in current PATH; daemon may still be running'; fi
for file in /etc/init.d/dropbear /etc/config/dropbear /etc/default/dropbear; do
    if [ -r "$file" ]; then printf 'Readable configuration candidate: %s (contents not dumped)\n' "$file"; fi
done
startup=0
for file in /etc/rc.d/S*dropbear /etc/rc*.d/S*dropbear; do
    if [ -e "$file" ]; then startup=$((startup+1)); fi
done
printf 'Existing Dropbear startup-link candidates: %s (not a reboot test)\n' "$startup"
for tool in opkg apt-get rpm; do
    if available "$tool"; then printf 'Package tool present: %s (not invoked)\n' "$tool"; fi
done
printf '%s\n' 'No account database, private key, authorized_keys, environment dump or raw startup config read.'
printf '%s\n' 'No binary ABI compatibility, root-login policy or reboot persistence inferred.'
