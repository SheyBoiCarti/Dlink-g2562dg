> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 6A: temporary root SSH key test

Date: 2026-10-19. **Status: approved temporary test completed and rolled back. Public-key SSH as `admin` returned UID 0 on two independent command sessions.** Interactive PTY validation failed; reboot persistence was not implemented. No test listener remains running.

## Completed investigation

Read the Phase 5 environment, Dropbear analysis, persistence proposal, recovery assessment, results and Phase 6 readiness. Re-entered the verified Telnet management console and root shell for read-only checks; UID 0, ARMv7/Linux 3.14.18 and exact `TK_1.00TK_V1.2.12ak_20221018` software identity were reconfirmed. Recovery sessions closed normally after inspection.

The running Dropbear digest matches the previously analyzed executable. Its UID 0 public-key lookup remains `/etc/dropbear/authorized_keys`; the permission/signature code is recorded in [the Phase 5 analysis](../raw-evidence/PHASE5_BINARY_ANALYSIS.json). RSA/DSA algorithm names are present; Ed25519, ECDSA and RSA-SHA2 names are absent. RSA 3072 is the selected test key type; RSA-3072 authentication with an RSA/SHA-1 signature was subsequently verified at runtime.

Live prerequisites:

- `chroot NEWROOT [PROG ARGS]` is provided by BusyBox 1.19.4. `mount` and `umount` are the installed util-linux-style commands, with `--bind`, `--make-private` and `-n` support. Merely having BusyBox mount/umount applets does not identify the active commands; their actual help was inspected.
- Root effective/bounding capability masks include mount and chroot capabilities. Bind/chroot service startup subsequently succeeded within the approved temporary scope.
- `/tmp` is tmpfs; root JFFS2 remains `ro`. About 39 MiB was available RAM at the preflight sample. The tmpfs 512 MiB limit is not available physical memory.
- `/tmp/dlink-phase6a` and global `/etc/dropbear` were absent. Port 2222 was not listening.
- `/bin`, `/lib`, `/usr`, `/dev`, `/dev/pts`, `/var`, account-file symlinks and the existing server host key were inspected. Mount-info records show no shared/master propagation tags on the relevant original mounts.
- `br0` retains `10.0.0.2/24`. IPv4 INPUT is DROP and `service_list` admits `br0`; auxiliary INPUT chains were inspected. IPv6 INPUT remains ACCEPT, so the proposed test listener has an explicit **IPv4-only** address and no wildcard/IPv6 bind. No firewall or WAN/NAT rule would be added.
- The current host-key public fingerprint still matches the Phase 5 identity. No private server key bytes were captured or overwritten.

Evidence: [initial preflight](../raw-evidence/PHASE6A_PREFLIGHT.json), [additional preflight](../raw-evidence/PHASE6A_ADDITIONAL_PREFLIGHT.json), [rollback tool preflight](../raw-evidence/PHASE6A_ROLLBACK_PREFLIGHT.json).

## Client preparation

A dedicated RSA-3072 key-generation process was started with 100 OpenSSH KDF rounds and a secure local passphrase dialog, outside OneDrive:

```text
<WORKSPACE_OR_USER_HOME>\AppData\Local\DLinkResearch\ssh\phase6a-20261019-202134\
    id_rsa_dlink_phase6a
    id_rsa_dlink_phase6a.pub
    known_hosts_phase6a
```

Key generation completed. The resulting private key is **not passphrase-encrypted** (OpenSSH cipher `none`); its local ACL permits only the current Windows user and SYSTEM. It remains outside OneDrive and was never uploaded to the router or included in reports. Only its public half was installed temporarily. Public fingerprint: `[PUBLIC_KEY_FINGERPRINT_3]`. See [non-secret key metadata](../raw-evidence/PHASE6A_CLIENT_KEY.json). A passphrase should be added locally before any future ongoing use; that was not part of this proof.

`known_hosts_phase6a` was prepared from the previously verified RSA public host identity, for `[10.0.0.2]:2222`. The client's original `known_hosts` was unchanged. Existing local boot-file baseline digests were revalidated. No configuration that the proposal would overwrite exists: it would create a new owned RAM tree, not replace live account, SSH, init or firewall files.

## Selected temporary method

**Run an additional instance of the existing Dropbear inside a new RAM-backed chroot.** This changes that process's root-directory view, not the live router's `/etc`. It avoids a global `/etc` bind mount and any flash remount. It is a temporary alternate filesystem view, not a security sandbox: the authenticated account still has UID 0 on the router.

New tree:

```text
/tmp/dlink-phase6a/
    .phase6a-owned
    phase6a_setup.sh
    phase6a_rollback.sh
    dropbear.log
    launcher.pid
    root/
        bin/ lib/ usr/ dev/ var/   five bind mounts of existing paths
        dev/pts/                   sixth bind mount for PTY access
        etc/passwd -> /var/passwd  existing account data, not modified/copied
        etc/group  -> /var/group   existing group data, not modified/copied
        etc/dropbear/authorized_keys  only the dedicated client PUBLIC key
        run/dropbear.pid           test daemon PID file
        tmp/
```

No original `/etc/passwd` or `/etc/shadow` is edited. No shadow copy is created. The existing passwd view resolves the UID 0 account; the vendor's already analyzed password-field override and public-key path do not require a replacement account database. Runtime checks and successful command sessions verified the dependencies needed for this proof; interactive PTY operation remains unresolved.

Each new bind is marked private at its new target. No existing mount's propagation or read-only state is changed. Bind mounts under the scratch tree are global mount-table additions, but only the test chroot uses these paths. Original Telnet, HTTP and port 22 SSH retain their existing filesystem views.

Exact listener command used under explicit approval:

```sh
chroot /tmp/dlink-phase6a/root /usr/sbin/dropbear \
  -F -E -r /var/dropbear/rsa_host_key \
  -p 10.0.0.2:2222 -s -j -k -P /run/dropbear.pid
```

Its stderr/stdout were redirected to the owned RAM log. The existing private host key is read through the `/var` bind; `-R` is not used. No original service is restarted/replaced, and no persistent partition is written. The executed setup confirmed the socket is exactly `10.0.0.2:2222` and rejects an unexpected wildcard or IPv6 listener.

## Exact execution files and approval scope

The locally prepared [setup script](../../scripts/phase6a_setup.sh) and [rollback script](../../scripts/phase6a_rollback.sh) contain the exact commands. Both passed local Bash syntax checking and were staged and executed after the user explicitly approved the temporary proof and cleanup. The first attempt demonstrated one command login but failed PTY validation and was rolled back; a repeat within the same scope demonstrated two command logins, recorded the PTY limitation, and was also rolled back. Only their explanatory headers were updated afterward; operational commands are unchanged.

The approved sequence executed by the controller was:

1. Keep an original-root Telnet shell open and capture current mount/listener/account metadata without secret values. Recheck rootfs `ro`, `/tmp` tmpfs, scratch-path absence and unused port 2222. Verify the completed local public key and host identity.
2. Create only `/tmp/dlink-phase6a` with mode 0700, marker `dlink-phase6a-v1`, and the two reviewed control scripts. Public scripts and the client public key may be transferred; credentials and client private-key bytes must never be transferred.
3. Run the setup script with Base64 of the single public-key line as its argument. It creates private RAM directories, the two account symlinks and mode-0600 authorized-key file; creates six binds; tests the temporary root; launches the second listener. Any error triggers controller-directed rollback through the retained Telnet connection.
4. Connect twice as `admin` with the dedicated key and strict host checking. Run `id -u`, `id` and `uname -srm`; separately test PTY allocation. No service/configuration commands or persistent writes are part of those SSH checks.
5. By default, run rollback after the proof, then independently verify the scratch tree and port 2222 are gone, original mounts remain unchanged, and a fresh Telnet `AMS# -> sh -> id -u` still works. This approval scope is a temporary proof with cleanup, not permission to leave a new daemon running indefinitely.

Successful command-session invocation template (client paths resolved locally; requires the temporary listener to be running):

```text
ssh -T -F none -p 2222 -i <dedicated-client-key>
  -o UserKnownHostsFile=<known_hosts_phase6a>
  -o GlobalKnownHostsFile=none -o StrictHostKeyChecking=yes
  -o UpdateHostKeys=no -o IdentitiesOnly=yes -o IdentityAgent=none
  -o PreferredAuthentications=publickey -o PasswordAuthentication=no
  -o KbdInteractiveAuthentication=no -o BatchMode=yes
  -o KexAlgorithms=+diffie-hellman-group14-sha1
  -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa
  admin@10.0.0.2 "id -u; id; uname -srm"
```

These exceptions apply only to this invocation. The test used public-key authentication only; no router password fallback or agent identity was permitted. Host checking stayed strict against the dedicated known-hosts file. The private key used for this proof has no passphrase, as disclosed above.

## Rollback and failure modes

Run the reviewed rollback from the **original-root Telnet shell**, not inside the chroot. It sends TERM only to processes whose `/proc/<pid>/root` exactly equals `/tmp/dlink-phase6a/root`. It never uses `killall`. If any such process remains, cleanup stops without forced unmount or deletion.

It then unmounts only these targets, in order, if mounted:

```text
/tmp/dlink-phase6a/root/dev/pts
/tmp/dlink-phase6a/root/var
/tmp/dlink-phase6a/root/dev
/tmp/dlink-phase6a/root/usr
/tmp/dlink-phase6a/root/lib
/tmp/dlink-phase6a/root/bin
```

Unmount uses `-n` to avoid mtab writes. No lazy/forced unmount, remount or reboot is included. Before deleting RAM files, rollback verifies the exact scratch path, its ownership marker and absence of any descendant mounts. If an unmount fails, preserve the scratch tree and investigate; deleting through a remaining `/var` or `/dev` bind could damage live state.

Remaining failure possibilities include libc/account lookup inside the alternate root, a missing runtime dependency, key algorithm/signature refusal, insufficient RAM, unavailable port/bind/chroot operation, PTY differences, a vendor `sysmgr` event terminating the additional daemon, or busy mounts during cleanup. Root access within the temporary root is not proof of reboot persistence or a normal host-root filesystem view. No automatic fallback to a global `/etc` overlay, flash changes or firewall changes is authorized.

## Verified results and final state

[Execution evidence](../raw-evidence/PHASE6A_EXECUTION.json) records two independent non-PTY SSH connections, both exiting 0 with explicit client confirmation of authentication using `publickey` and this output:

```text
PHASE6A_SSH_PROOF
0
uid=0(admin) gid=0(admin)
Linux 3.14.18 armv7l
```

The separate `-tt` check also authenticated using the public key, but produced no command output and closed with client exit 255 (remote status -1). Interactive shell operation is **not verified**. The captured server log did not establish the cause; do not infer that all PTY use is unsupported. An earlier attempt and its automatic cleanup are retained in [attempt-one evidence](../raw-evidence/PHASE6A_EXECUTION_ATTEMPT1.json).

The approved rollback terminated only the temporary chroot processes, unmounted all six temporary binds, and removed the owned RAM tree. A fresh original Telnet login again returned UID 0. [Independent final checks](../raw-evidence/PHASE6A_FINAL_CHECKS.json) confirmed:

- `/tmp/dlink-phase6a` and global `/etc/dropbear` are absent; no port 2222 listener remains.
- Original Dropbear PID 3244 and Telnet PID 1037 still run on their original ports.
- Root JFFS2 remains read-only; account-file metadata and the existing host-key public fingerprint remain unchanged.
- No startup, firewall, passwd/shadow, persistent storage or firmware changes were made; no reboot occurred.

Phase 6A's public-key/UID-0 proof is complete. This does **not** enable public-key access on the original port 22 daemon or survive reboot. Future interactive troubleshooting, reactivation, key passphrase protection and persistence require their own scope; no persistence has been implemented.
