"""Reproduce the original extraction of one digest-verified DSL-G2562DG image.

Recovered from the October 19 investigation's inline Python commands. Firmware
paths stay in a local manifest; symlinks and files become numeric inode blobs.
This is an artifact-specific research tool, not a general JFFS2 extractor.
"""

import argparse
import collections
import hashlib
import json
import re
import stat
import struct
import sys
import zlib
from pathlib import Path

IMAGE_SIZE = 24_272_267
IMAGE_SHA256 = "2f7cf1c4992f6521265480dbb78d4989a80bf090ff636a3081ce6f1e275ebbd7"
REPOSITORY = Path(__file__).resolve().parents[2]


def crc(data):
    return zlib.crc32(data, 0xFFFFFFFF) ^ 0xFFFFFFFF


def validate_output(output):
    output = output.resolve()
    if output.is_relative_to(REPOSITORY):
        raise ValueError("output_inside_repository")
    if output.exists():
        raise ValueError("output_already_exists")
    return output


def scan_nodes(image):
    nodes = []
    for match in re.finditer(b"\x85\x19", image):
        offset = match.start()
        if offset + 12 > len(image):
            continue
        _, kind, size, checksum = struct.unpack_from("<HHII", image, offset)
        if (
            size >= 12
            and offset + size <= len(image)
            and crc(image[offset : offset + 8]) == checksum
        ):
            nodes.append((offset, kind, size))
    return nodes


def rtime(data, size):
    positions = [0] * 256
    output = bytearray()
    index = 0
    while len(output) < size:
        if index + 2 > len(data):
            raise ValueError("truncated_rtime_data")
        value, repeat = data[index : index + 2]
        index += 2
        back = positions[value]
        output.append(value)
        positions[value] = len(output)
        for _ in range(repeat):
            if back >= len(output) or len(output) >= size:
                raise ValueError("invalid_rtime_reference")
            output.append(output[back])
            back += 1
    return bytes(output)


def reconstruct(image, nodes, output):
    entries = {}
    inodes = collections.defaultdict(list)
    for offset, kind, length in nodes:
        if kind == 0xE001:
            if length < 40:
                raise ValueError("truncated_directory_node")
            parent, version, ino, _, name_size, dtype = struct.unpack_from(
                "<IIIIBB", image, offset + 12
            )
            if 40 + name_size > length:
                raise ValueError("truncated_directory_name")
            name = image[offset + 40 : offset + 40 + name_size]
            node_crc, name_crc = struct.unpack_from("<II", image, offset + 32)
            if crc(image[offset : offset + 32]) != node_crc or crc(name) != name_crc:
                raise ValueError("node_crc_mismatch")
            key = (parent, name.decode("utf8", "replace"))
            if key not in entries or version >= entries[key][0]:
                entries[key] = (version, ino, dtype)
        elif kind == 0xE002:
            if length < 68:
                raise ValueError("truncated_inode_node")
            ino, version, mode = struct.unpack_from("<III", image, offset + 12)
            size = struct.unpack_from("<I", image, offset + 28)[0]
            start, compressed, expanded = struct.unpack_from("<III", image, offset + 44)
            compression = image[offset + 56]
            data_crc, node_crc = struct.unpack_from("<II", image, offset + 60)
            if 68 + compressed > length:
                raise ValueError("truncated_inode_data")
            data = image[offset + 68 : offset + 68 + compressed]
            if crc(image[offset : offset + 60]) != node_crc or crc(data) != data_crc:
                raise ValueError("node_crc_mismatch")
            inodes[ino].append(
                (version, mode, size, start, expanded, compression, data)
            )

    paths = {1: "/"}
    for _ in range(100):
        count = len(paths)
        for (parent, name), (_, ino, _) in entries.items():
            if ino and parent in paths and ino not in paths:
                paths[ino] = paths[parent].rstrip("/") + "/" + name
        if len(paths) == count:
            break

    store = output / "inode-store"
    store.mkdir()
    manifest = {}
    for ino, chunks in inodes.items():
        latest = max(chunks, key=lambda chunk: chunk[0])
        mode, size = latest[1:3]
        if stat.S_ISDIR(mode):
            continue
        if size > 32 * 1024 * 1024:
            raise ValueError("inode_size_limit")
        contents = bytearray(size)
        for _, _, _, start, expanded, compression, data in sorted(
            chunks, key=lambda c: c[0]
        ):
            if compression == 0:
                raw = data
            elif compression == 1:
                raw = b"\0" * expanded
            elif compression == 2:
                raw = rtime(data, expanded)
            elif compression == 6:
                raw = zlib.decompress(data)
            else:
                raise ValueError("unsupported_compression")
            if len(raw) != expanded:
                raise ValueError("decompressed_size_mismatch")
            if start < size:
                contents[start : min(size, start + expanded)] = raw[
                    : max(0, size - start)
                ]
        artifact = store / f"{ino}.bin"
        with artifact.open("xb") as handle:
            handle.write(contents)
        manifest[paths.get(ino, f"UNRESOLVED/{ino}")] = {
            "ino": ino,
            "mode": mode,
            "size": size,
            "symlink": stat.S_ISLNK(mode),
            "file": str(artifact),
        }
    return manifest


def extract(image_path, output):
    output = validate_output(output)
    if image_path.stat().st_size != IMAGE_SIZE:
        raise ValueError("firmware_size_mismatch")
    image = image_path.read_bytes()
    if hashlib.sha256(image).hexdigest() != IMAGE_SHA256:
        raise ValueError("firmware_digest_mismatch")
    nodes = scan_nodes(image)
    # No reuse or overwrite: failed runs retain their partial output for inspection.
    output.mkdir(parents=True, exist_ok=False)
    manifest = reconstruct(image, nodes, output)
    (output / "jffs2-nodes.json").write_text(json.dumps(nodes), encoding="utf-8")
    (output / "filesystem-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "nodes": len(nodes),
        "artifacts": len(manifest),
        "crc_failures": 0,
        "reconstruction_errors": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "image", type=Path, help="Exact older vendor image; never executed"
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="New private directory outside this repository",
    )
    args = parser.parse_args()
    try:
        result = extract(args.image, args.output)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (OSError, struct.error, zlib.error):
        print("extraction_failed_review_private_output", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
