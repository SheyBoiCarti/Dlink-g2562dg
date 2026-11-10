> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Verified Phase 3 command evidence

## Phase 3B actual local evidence

2026-10-19 17:33 UTC initial bounded metadata checks; meaningful Telnet banner confirmed on a subsequent bounded read. Target only 10.0.0.2, TCP 23/21.

```text
TELNET banner: welcome to D-Link ams_cli system
TELNET prompt: LOGIN#
FTP greeting: 220, vsFTPd 3.0.2
FTP FEAT: 211; EPRT EPSV MDTM PASV REST STREAM SIZE TVFS UTF8
FTP SYST: 530
FTP PWD: 530
FTP HELP: 530 (USER/PASS mentioned)
FTP QUIT: 221
```

No Telnet application input, USER/PASS, anonymous login, file transfers or data connections. Telnet negotiation declined optional features; its LOGIN# prompt is not a Linux/root shell. The initial colon-only prompt detector missed this shape, so its false login_prompt value was not used to infer absence. FTP errors establish an authentication gate, not unsupported commands or a Linux rootfs. No OS identity inferred.

### Fresh authenticated web evidence

After secure local entry and normal intermediate-page redirect handling: authenticated `/index.html`, then GETs of the previously known normal FTP/storage/password/ping/traceroute/xDSL menu pages. No speculative state-changing request or hidden-role override.

```text
FTP controls: INPUT_EnableFTP; SELECT_UsbPartion
FTP generated configuration keys: InternetGatewayDevice.Services.ServiceFTP.Enable; InternetGatewayDevice.Services.ServiceFTP.RootDIR
Account controls: userName; oldPassword; newPassword; confirmPassword
Ping controls: INPUT_Host; INPUT_NumberOfRepetitions; INPUT_TimeOut; INPUT_DataBlockSize; SELECT_Protocol; select_wan_interface
Traceroute controls: INPUT_Host; INPUT_MAXTTL; INPUT_WaitTime; select_wan_interface
xDSL control: INPUT_DebugToolEnable
Normal logout endpoint requested: /cgi-bin/logout.cgi
```

Only control identifiers, static paths and key names retained. No field values or initialization-derived setting states recorded. No form submission after login, FTP authentication or router diagnostic execution.

## Preserved Phase 3 SSH evidence

## Continuation: approved trust establishment

Before trust acceptance, existing known-host records were searched with `ssh-keygen -F` for both address spellings. No match in active/backup user records; no alternate/global or PuTTY/WinSCP cache record found. No trust store was modified during inspection.

The actual interactive SSH prompt showed:

```text
The authenticity of host '10.0.0.2 (10.0.0.2)' can't be established.
RSA key fingerprint is: [PUBLIC_KEY_FINGERPRINT_1]
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

After explicit user TOFU approval, that exact fingerprint was entered and OpenSSH reported:

```text
Warning: Permanently added '10.0.0.2' (RSA) to the list of known hosts.
```

That connection was cancelled before password entry. A subsequent strict-checking connection produced:

```text
debug1: Host '10.0.0.2' is known and matches the RSA host key.
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: password
debug1: read_passphrase: requested to askpass
```

Local public-key verification returned:

```text
2048 [PUBLIC_KEY_FINGERPRINT_1] 10.0.0.2 (RSA)
```

The single password-method connection used `-tt -v`, the two legacy options, `StrictHostKeyChecking=yes`, `IdentityFile=none`, `IdentityAgent=none`, `PubkeyAuthentication=no`, `KbdInteractiveAuthentication=no`, `PreferredAuthentications=password`, `NumberOfPasswordPrompts=1`, `ConnectionAttempts=1`, `ConnectTimeout=5`, and target `admin@10.0.0.2`. Git askpass supplied the local interactive dialog; no credential was present in command arguments, environment variables or saved artifacts.

Final exact output (nonzero exit):

```text
debug1: Authentications that can continue: publickey,password
debug1: No more authentication methods to try.
admin@10.0.0.2: Permission denied (publickey,password).
```

No prompt contents or cancellation status were logged. No authenticated router command or additional credential attempt followed. This trust is user-approved TOFU, not independent verification. The following older transport results are preserved for chronology.

Collected 2026-10-19 from the owner's Windows environment. This file retains the relevant exact transport/error lines and public fingerprint, not local identity paths or full debug noise. No credentials, tokens, private keys or authenticated router output were collected.

Client:

```text
OpenSSH_10.3p1, OpenSSL 3.5.6 7 Apr 2026
```

Initial command:

```text
ssh -vv -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentityAgent=none -o PubkeyAuthentication=no -o ConnectionAttempts=1 -o ConnectTimeout=5 admin@10.0.0.2
```

Relevant exact output (tool reports nonzero exit status):

```text
debug1: Connection established.
debug1: Remote protocol version 2.0, remote software version dropbear_2014.63
debug2: KEX algorithms: diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,[EMAIL_REDACTED]
debug2: host key algorithms: ssh-rsa
Unable to negotiate with 10.0.0.2 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,[EMAIL_REDACTED]
```

Single compatibility retry:

```text
ssh -v -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentityAgent=none -o PubkeyAuthentication=no -o ConnectionAttempts=1 -o ConnectTimeout=5 -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa admin@10.0.0.2
```

Relevant exact output (nonzero):

```text
debug1: kex: algorithm: diffie-hellman-group14-sha1
debug1: kex: host key algorithm: ssh-rsa
debug1: kex: server->client cipher: aes128-ctr MAC: hmac-sha1 compression: none
debug1: kex: client->server cipher: aes128-ctr MAC: hmac-sha1 compression: none
debug1: Server host key: ssh-rsa [PUBLIC_KEY_FINGERPRINT_1]
No RSA host key is known for 10.0.0.2 and you have requested strict checking.
Host key verification failed.
```

The fingerprint is **unverified**; it was not accepted. Strict checking prevented an authentication attempt. Both invocations ran without a terminal and printed the normal pseudo-terminal warning; that warning is not the failure cause. The future password attempt requires a real interactive terminal and secure non-echoing prompt, after independent host trust is resolved.

No `whoami`, `id`, shell identification, OS/release read, CPU read, BusyBox execution, mount/df/proc inspection, process listing or service-config read was performed on the router. No Telnet credential or account enumeration. Zero SSH credential attempts.
