> Historical research record (2026-10-19), sanitized for publication. Earlier conclusions may be superseded. Start with the [reading guide](../docs/READING_GUIDE.md). Local approval notes describe that original investigation, not actions performed by this export.

# Authorized configuration-backup inspection

Later outcome: [root Linux access was verified](ROOT_ACCESS_VERIFIED.md) using credentials recovered from an official older firmware image. The configuration export itself did not supply that credential. The observations below remain the backup-specific findings.

Date: 2026-10-19. Follow-up explicitly authorized by the owner after Phase 4; this was a configuration export, not firmware extraction or UART work.

## Actions and evidence

The normal web login used a secure local Git askpass dialog, with the password held in memory and transformed using the login page's observed SHA-256 scheme. No password or login hash was printed or saved. The normal management navigation referenced `/page/management/mngt_backup.shtml`; its Backup action navigates to `/cgi-bin/config_download.cgi?action=download`. The page's `validateCode()` implementation returns true immediately. Only this normal export action was requested; no settings, restore, update or reboot action was submitted. The normal logout endpoint was requested afterward.

The export is stored outside OneDrive in a directory whose inherited permissions were removed and access granted to the current Windows user and SYSTEM:

```text
<WORKSPACE_OR_USER_HOME>\AppData\Local\DLinkResearch\private\20261019-195059\router-config.bin
```

Size: 1,416,545 bytes. SHA-256:

```text
fb5682fdb785a4dd2bf78f1c4a2bf508d0f89bdbb991d797a257c05c23fff8a2
```

Base64 decoding produced `decoded-base64.bin` in the same restricted directory, 1,048,609 bytes. It contains readable null-separated configuration records and extensive `0xff` padding. Base64 is encoding, not encryption. Neither artifact was copied into the project or uploaded elsewhere.

## Findings and limits

- Readable settings include WAN/management/WLAN password-related fields. Their values were not displayed; names alone do not establish whether each value is a real credential, placeholder or transformed value. Treat both files as secret-bearing.
- A `X_CT-COM_UserInfo.UserList.1` record exists, but no usable SSH/root username-and-password pair was established. `Services.ServiceSSH.Enable` is a configuration field, not account-policy evidence.
- No standard md5crypt, sha256crypt, sha512crypt or bcrypt strings matched in the decoded artifact. No shadow-file-style `root:` entry or standalone 64-hex string matched. These checks do not exclude other encodings, binary structures or omitted/default accounts.
- The export is configuration data, not a demonstrated firmware/root-filesystem dump. It did not provide a verified Linux password hash to crack. No password recovery or new SSH attempt was performed from its contents.

No router configuration was changed. No secret values are included in this report. Further firmware investigation would require a separately obtained authentic image or another legitimate read-access mechanism; this export does not establish one.
