> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Phase 3 SSH authentication investigation

## Continuation: user-approved TOFU

The user explicitly approved TOFU for the exact previously observed RSA fingerprint. Before acceptance, both Git and native Windows SSH effective configuration and trust-file locations were inspected read-only. No matching record was found for `10.0.0.2` or `[10.0.0.2]:22` in the active user trust file; its backup also had none. Alternate/global trust files were absent, and PuTTY/WinSCP host-key caches were absent. No target-specific host-key alias/proxy override was observed. Previously inspected authenticated router pages exposed no host fingerprint; vendor-domain searches found no fingerprint or host-key procedure. No private keys were read.

A fresh interactive SSH trust prompt displayed the exact prior fingerprint. This was consistency checking, not independent verification. After the user's approval, the exact fingerprint was entered at the host-key prompt (no automatic `yes`). OpenSSH recorded it in the client's existing `known_hosts`; `ssh-keygen` confirms an RSA 2048-bit key with fingerprint `[PUBLIC_KEY_FINGERPRINT_1]`. Trust is **explicitly approved TOFU**, not independently authenticated identity. First-connection interception remains the accepted residual risk.

The trust-establishment connection was cancelled at its password prompt without submitting a credential. A new strict-checking connection then confirmed the saved key and reached server user authentication. The server offers `publickey,password`. Agent/key authentication is disabled and `NumberOfPasswordPrompts=1`. Git's installed local `git-askpass.exe` provides the secure interactive password dialog; only its executable path, not a credential, is configured through the process environment. No secret is placed in tool arguments, history, files or chat. The single configured password-method attempt then ended with `admin@10.0.0.2: Permission denied (publickey,password).` No authenticated session opened. No credential retry or alternate account attempted. The secure dialog contents and cancellation status were deliberately not logged, so this does not prove which value was supplied or why the server denied it.

Current outcome is authentication failure (Outcome D), with server methods publickey,password. Earlier results below are preserved as historical observations; their unknown-host-key blocker was resolved by the explicit TOFU decision, not independent verification.

Date: 2026-10-19. Target only `10.0.0.2:22`; requested account `admin`. Existing Phase 1, Phase 2 and authenticated web follow-up were read first. Client: Git for Windows OpenSSH 10.3p1 / OpenSSL 3.5.6. Native Windows execution; WSL was not required or established.

## Actual connection sequence

Two credential-free SSH transport connections were made. Both used BatchMode, strict host-key verification, disabled agent/public-key authentication, one connection attempt and a five-second timeout. No password prompt, password submission, user-key authentication, host-key acceptance or remote command occurred.

1. Normal algorithm policy fails before authentication:

```text
Unable to negotiate with 10.0.0.2 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,[EMAIL_REDACTED]
```

The server's proposal also offers only `ssh-rsa` for host-key signatures, which does not overlap the client's default proposal. AES128-CTR and HMAC-SHA1 already overlap; no cipher/MAC configuration change needed.

2. One compatibility retry adds only:

```text
-o KexAlgorithms=+diffie-hellman-group14-sha1
-o HostKeyAlgorithms=+ssh-rsa
```

This completes key exchange, choosing DH group14/SHA-1, ssh-rsa host signature, AES128-CTR and HMAC-SHA1. It stops at:

```text
No RSA host key is known for 10.0.0.2 and you have requested strict checking.
Host key verification failed.
```

Observed public host fingerprint:

```text
RSA [PUBLIC_KEY_FINGERPRINT_1]
```

**This fingerprint is unverified.** It is a network observation, not a trust anchor. No independently trusted copy was available in the reviewed material or local client trust decision. The user was asked to compare it against a previously trusted client or independent router-side display; verification remains outstanding. Reconnecting or ssh-keyscan over the same LAN is not independent verification. No unknown key was accepted, and no known_hosts or SSH configuration was changed.

## Authentication outcomes

| Question | Observed answer |
|---|---|
| SSH reachable? | Yes; current Dropbear 2014.63 identification and key exchange observed. |
| Cryptographic compatibility? | Defaults fail; the two per-connection options above get past negotiation. |
| Requested username? | admin; no proof the account is accepted. |
| Password offered? | Unknown: host verification stops the connection before user authentication. |
| Public-key auth offered? | Unknown: server user-authentication methods were not reached; local agent/key auth disabled. |
| Authorized credentials accepted/rejected? | Neither tested nor inferred; zero credential attempts. |
| Restricted CLI / Linux shell / termination after auth? | Unknown; no authenticated session. |

The debug phrase “Authenticating ... as admin” is a client status message, not proof authentication succeeded. An SSH RSA **host key** is also not evidence the server permits user public-key authentication.

## Security implications

DH group14 uses a stronger group than group1, but this server's KEX and RSA signature still depend on legacy SHA-1 mechanisms. `ssh-rsa` denotes the RSA/SHA-1 signature algorithm; the fingerprint remains SHA-256. HMAC-SHA1 is a separate negotiated integrity mechanism. No group1, CBC, MD5, system-wide legacy policy or host-key-verification bypass was enabled. The `+` options append only the necessary legacy algorithms for this command. See [OpenSSH legacy guidance](https://www.openssh.org/legacy.html).

## Exact next connection, only after independent trust is resolved

Review the displayed fingerprint against an independent trusted source before answering any host-key acceptance prompt. If trust cannot be established, stop rather than accepting it blindly.

```bash
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa -o StrictHostKeyChecking=ask -o IdentityAgent=none -o PubkeyAuthentication=no -o PreferredAuthentications=password -o NumberOfPasswordPrompts=1 -o ConnectionAttempts=1 -o ConnectTimeout=5 admin@10.0.0.2
```

Use a real interactive terminal and enter the known authorized password only at SSH's non-echoing password prompt. Do not place it in chat, command arguments, environment variables, scripts, transcripts or files. If the account/password is rejected, stop; no guessing or second credential attempt. Do not add user public-key algorithm overrides without observing a relevant error; password auth needs none.

No further agent connections are scheduled in this run. The user can provide independent fingerprint verification for a resumed bounded attempt. No Telnet authentication is authorized, and none was attempted.
