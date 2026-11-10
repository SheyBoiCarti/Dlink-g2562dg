#!/bin/sh
# Executed under Phase 6A approval; obtain explicit approval before re-execution.
set -eu
P=/tmp/dlink-phase6a
R=$P/root
[ -d "$P" ] && [ ! -L "$P" ] || { echo 'No safe scratch directory'; exit 1; }
[ "$(cat "$P/.phase6a-owned")" = dlink-phase6a-v1 ] || { echo 'Wrong marker; refusing cleanup'; exit 1; }
test "$P" = /tmp/dlink-phase6a
# Terminate ONLY processes with this exact temporary filesystem root.
# Never use killall; never terminate the original Dropbear or Telnet service.
for p in /proc/[0-9]*/root; do
    [ "$(readlink "$p" 2>/dev/null || true)" = "$R" ] || continue
    n=${p#/proc/}; n=${n%/root}
    kill -TERM "$n" 2>/dev/null || true
done
sleep 1
for p in /proc/[0-9]*/root; do
    if [ "$(readlink "$p" 2>/dev/null || true)" = "$R" ]; then
        echo 'Test process remains; refusing to unmount or delete'
        exit 1
    fi
done
for path in "$R/dev/pts" "$R/var" "$R/dev" "$R/usr" "$R/lib" "$R/bin"; do
    if awk -v p="$path" '$2==p {ok=1} END {exit !ok}' /proc/mounts; then
        umount -n "$path" || { echo 'Unmount failed; scratch preserved'; exit 1; }
    fi
done
if awk -v p="$P/" 'index($5,p)==1 {found=1} END {exit !found}' /proc/self/mountinfo; then
    echo 'A scratch descendant remains mounted; refusing deletion'
    exit 1
fi
# Guarded exact path, owned marker and no remaining descendant mounts verified.
rm -rf "$P"
printf '%s\n' 'Temporary processes, six binds and owned RAM files removed.'
