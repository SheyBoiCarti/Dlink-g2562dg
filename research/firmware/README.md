# Firmware extraction, provenance, and structural metadata

No firmware image or extracted file bytes are included. The retained metadata helps readers identify the original artifact and audit the extraction results.

- `*.provenance.json`: acquisition URL, expected size, and SHA-256 for the older vendor image.
- `jffs2-nodes.json`: ordered triples `[image byte offset, node type, total node length]` recorded by the original scan. Values are metadata, not a filesystem image.
- `filesystem-manifest.json`: original filesystem paths mapped to inode number, mode, size, symlink classification, and a portable backing-artifact filename. `inode-artifacts/` is a reference namespace; its file contents are not supplied.

## Artifact verification

Obtain the image from the [recorded vendor source](../../docs/RESEARCH.md#1-finding-a-management-account), independently consider its provenance, and compare the size and digest before using artifact-specific offsets:

```powershell
Get-Item -LiteralPath 'C:\local-research\firmware\DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin' | Select-Object Length
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\local-research\firmware\DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin'
```

Expected size: 24,272,267 bytes. Expected SHA-256: `2f7cf1c4992f6521265480dbb78d4989a80bf090ff636a3081ce6f1e275ebbd7`. The older image was analyzed offline, not flashed. It predates the installed build; successful live verification, not its filename alone, established the management account's applicability.

## Extraction method and limits

The original custom Python parser located JFFS2 nodes, verified node/header/data CRCs, reconstructed directory/inode information, and decoded uncompressed, zlib, and RTIME data. It retained symlinks as data rather than materializing paths on Windows. No extracted executable was run on the PC. Exact observed counts and the account-table lead are in [the research explanation](../../docs/RESEARCH.md#1-finding-a-management-account).

The original scanner and reconstruction algorithm were recovered from inline Python tool calls in the October 19 investigation. The maintained [extractor](extract_jffs2.py) combines them with an explicit image/output interface, exact size/SHA-256 verification, safe numeric output filenames, and count-only console output. Its public entry point rejects other images; this is not a general-purpose or adversarial-input JFFS2 parser.

## Reproduce extraction offline

Use Python 3.12+ and keep both the vendor image and output outside this repository, preferably outside cloud-synced folders. The command does not download firmware, contact the router, run extracted programs, or print credentials. From the repository root:

```powershell
python research/firmware/extract_jffs2.py `
  'C:\local-research\firmware\DSL-G2562DG_TK_1.00TK_V1.2.12ak_20210420_telkom-Image-all.bin' `
  --output 'C:\local-research\dlink-extracted'
```

The output directory must not already exist and must resolve outside the repository. It contains `jffs2-nodes.json`, `filesystem-manifest.json`, and `inode-store/<inode>.bin`. Firmware paths appear only as manifest labels. Symlink targets are saved as ordinary bytes, never created as host symlinks. The manifest's `file` values point to local absolute artifact paths and may disclose your local username; never upload this generated manifest or the extracted files. They may include firmware credentials, keys, and other sensitive vendor data. No recovered secret is automatically displayed or installed.

On success, expect a JSON count summary with `nodes=17405`, `artifacts=3627`, `crc_failures=0`, and `reconstruction_errors=0`. A rejected image creates no output. An interrupted or failed reconstruction can leave partial output; inspect it locally and choose a new directory for the next attempt.

### Validation and limits

On 2026-11-09 the packaged extractor was run against the retained original image after verifying its recorded digest. All 17,405 node triples matched the original inventory. All 3,627 reconstructed artifacts matched the original bytes and inode/mode/size/symlink metadata. See [the validation record](EXTRACTION_VALIDATION.json). The retained original bytes are private, so readers can rerun the extraction but cannot independently compare against those private reference files. The published filesystem manifest omits one redacted path and normalizes backing paths; it is not an exact output oracle.

Offline tests cover CRC rejection, RTIME overlap, symlink-as-data handling, wrong-image rejection, and output protection. The method retains the historical single-path-per-inode mapping and 100-pass path resolution. It has only been verified against this exact image; it does not promise general JFFS2 recovery, hard-link preservation, other compression types, or recovery of other firmware versions.

After reconstruction, the [archived console collector](../controllers/phase5_console.py.txt) shows how the original workflow loaded the reconstructed CLI artifact and selected the account-table fields documented in the research notes. Its offsets apply only to the exact analyzed artifact. This historical collector also connects to the router when executed; it is reference text, not a local-only credential viewer or the recommended installation path. The supported restoration controller still requires an existing authorized management credential.

Publication detail: 1 manifest entry was omitted because its path text collided with a known management-credential literal. The remaining manifest is a sanitized subset, not an exact inventory for count/hash comparison.
