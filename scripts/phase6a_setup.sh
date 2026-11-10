#!/bin/sh
# Executed under Phase 6A approval; obtain explicit approval before re-execution.
# Controller must first verify /tmp/dlink-phase6a absent, create it in tmpfs,
# stage this script and phase6a_rollback.sh, and create .phase6a-owned marker.
# Argument 1 is Base64 of ONE PUBLIC key line, never a client private key.
set -eu
P=/tmp/dlink-phase6a
R=$P/root
fail() { printf '%s\n' "$1" >&2; exit 1; }
[ "$#" -eq 1 ] || fail 'Expected one encoded public key argument'
[ -d "$P" ] && [ ! -L "$P" ] || fail 'Scratch directory missing or unsafe'
[ "$(cat "$P/.phase6a-owned")" = dlink-phase6a-v1 ] || fail 'Ownership marker missing'
[ -f "$P/phase6a_rollback.sh" ] || fail 'Rollback script must be staged first'
[ ! -e "$R" ] || fail 'Temporary root already exists'
[ ! -e /etc/dropbear ] || fail 'Global key-directory baseline changed'
[ "$(id -u)" = 0 ] || fail 'UID 0 required'
awk '$2=="/tmp" && $3=="tmpfs" {ok=1} END {exit !ok}' /proc/mounts || fail '/tmp is not tmpfs'
awk '$2=="/" && $3=="jffs2" && $4 ~ /(^|,)ro(,|$)/ {ok=1} END {exit !ok}' /proc/mounts || fail 'Root JFFS2 is not read-only'
[ -r /var/dropbear/rsa_host_key ] || fail 'Existing host key missing'
ip -o -4 addr show br0 | grep -q '10\.0\.0\.2/24' || fail 'Expected LAN address missing'
if netstat -lnt | awk '$4 ~ /:2222$/ {found=1} END {exit !found}'; then
    fail 'Port 2222 already occupied'
fi
umask 077
mkdir "$R"
for d in bin lib usr dev var run etc tmp; do mkdir "$R/$d"; done
mkdir "$R/dev/pts" "$R/etc/dropbear"
printf '%s' "$1" | base64 -d > "$R/etc/dropbear/authorized_keys"
awk 'NR!=1 || $1!="ssh-rsa" {bad=1} END {exit (bad || NR!=1)}' "$R/etc/dropbear/authorized_keys" || fail 'Expected exactly one RSA public key'
chmod 700 "$P" "$R" "$R/etc" "$R/etc/dropbear"
chmod 600 "$R/etc/dropbear/authorized_keys"
ln -s /var/passwd "$R/etc/passwd"
ln -s /var/group "$R/etc/group"
# Do not copy, create, modify or print the original passwd/shadow data.
# No shadow file is supplied; getspnam fallback uses the unchanged passwd view.
trap 'sh "$P/phase6a_rollback.sh"' 1 2 15
for d in bin lib usr dev var; do
    mount -n --bind "/$d" "$R/$d" || fail "Bind failed: $d; run rollback"
    mount -n --make-private "$R/$d" || fail "Private propagation failed: $d; run rollback"
done
mount -n --bind /dev/pts "$R/dev/pts" || fail 'devpts bind failed; run rollback'
mount -n --make-private "$R/dev/pts" || fail 'devpts propagation failed; run rollback'
chroot "$R" /bin/sh -c 'test "$(id -u)" = 0 && test -r /etc/passwd && test -r /etc/dropbear/authorized_keys && test -r /var/dropbear/rsa_host_key' || fail 'Temporary-root prerequisites failed; run rollback'
chroot "$R" /usr/sbin/dropbear -F -E -r /var/dropbear/rsa_host_key -p 10.0.0.2:2222 -s -j -k -P /run/dropbear.pid > "$P/dropbear.log" 2>&1 &
test_pid=$!
printf '%s\n' "$test_pid" > "$P/launcher.pid"
sleep 1
kill -0 "$test_pid" || fail 'Test process exited; run rollback'
[ "$(readlink "/proc/$test_pid/root")" = "$R" ] || fail 'Unexpected process root; run rollback'
netstat -lnt | awk '$4=="10.0.0.2:2222" && $6=="LISTEN" {ok=1} $4 ~ /:2222$/ && $4!="10.0.0.2:2222" {bad=1} END {exit (!ok || bad)}' || fail 'Unexpected listener; run rollback'
printf '%s\n' 'Temporary IPv4 LAN-only test listener ready; original services untouched.'
# Controller must retain its Telnet recovery session and invoke rollback after
# the two approved key-authentication checks, including on failure.
