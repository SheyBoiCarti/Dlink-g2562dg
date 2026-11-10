# Publication and redaction notes

The public copy preserves technical research while removing identifying data and secret-bearing artifacts. Imported reports are historical records; command transcripts are evidence to read, not a batch of commands to execute.

## Included

The device-specific controller and tests, reference setup/rollback scripts, original discovery/diagnostic scripts and offline tests, Phase 1 research, detailed technical reports, chronological findings, sanitized JSON command/result records, historical controller source, firmware acquisition metadata, JFFS2 node inventory, and a portable filesystem manifest.

## Redactions and transformations

- Personal Windows/WSL user paths and host identifiers are replaced with generic labels.
- The original PC address is replaced with the example `10.0.0.10`. Router address `10.0.0.2`, subnet/bridge assumptions, wildcard/loopback addresses, and firmware-default internal addresses remain where technically meaningful.
- Public host/client key fingerprints, public key lines, MAC-style identifiers, runtime UUIDs, and Windows SIDs are replaced by stable labels. Repeated labels preserve identity comparisons; different labels indicate different recorded values. These public identifiers are not private keys, but readers do not need this installation's identities.
- Known firmware-derived management credential text is removed if present. No personal password, client key passphrase, or private-key material is intentionally included.
- JSON is reserialized after sanitization. Device paths, command structure, output classifications, binary offsets/digests, error codes, and success/failure fields are retained wherever possible.
- Historical controller code is distributed as `.py.txt` / `.ps1.txt`. Personal paths and identifiers are sanitized. It is reference material rather than a supported runnable installation.
- Filesystem-manifest backing paths are normalized to `inode-artifacts/<original filename>`. Those extracted artifact files are not distributed.

Sanitized evidence is not byte-identical to the original and cannot be used to recompute original transcript hashes or identify the original router. Source-file/dump hashes recorded inside reports refer to the analyzed artifacts, not to the reserialized public reports. Redaction mappings and the original secrets are not included.

## Excluded

Vendor firmware images and extracted binaries, actual router configuration backups/decoded exports, private keys and installed credentials/configuration, browser sessions/cookies/HAR, screenshots and unrelated personal logs, virtual environments, third-party package trees, caches, build artifacts, and chat prompts. Third-party source snapshots downloaded for comparison are linked from reports rather than copied into this repository.

The original custom firmware-extraction parser was recovered from inline commands in the local investigation history after the initial export. The [packaged extractor](../research/firmware/extract_jffs2.py) and [validation record](../research/firmware/EXTRACTION_VALIDATION.json) are included. Raw chats are excluded. Reproduction writes firmware-derived contents only to a new external private directory; those outputs are not publication material. The public entry point accepts only the exact size/digest-verified image. General parser portability and fresh credential authentication on other devices remain unverified.

## Before publishing changes

Review added files for secrets and personal data, keep generated/local artifacts excluded, and run the offline test suites. The publication checks performed for this export are a bounded review, not a guarantee about future edits or previously unseen encodings. No repository remote, commit, or upload is created by this export.

Publication detail: 1 manifest entry was omitted because its path text collided with a known management-credential literal. The remaining manifest is a sanitized subset, not an exact inventory for count/hash comparison.
