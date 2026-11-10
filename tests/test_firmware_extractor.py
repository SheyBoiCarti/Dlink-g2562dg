"""Offline extractor boundaries and a small CRC-valid JFFS2 fixture."""

import importlib.util
import stat
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research" / "firmware" / "extract_jffs2.py"


def crc(data):
    return zlib.crc32(data, 0xFFFFFFFF) ^ 0xFFFFFFFF


def node(kind, body):
    header = struct.pack("<HHI", 0x1985, kind, 12 + len(body))
    return header + struct.pack("<I", crc(header)) + body


def fixture():
    name = b"link"
    entry = struct.pack("<IIIIBB2x", 1, 1, 2, 0, len(name), 10)
    header = struct.pack("<HHI", 0x1985, 0xE001, 40 + len(name))
    prefix = header + struct.pack("<I", crc(header)) + entry
    directory = node(0xE001, entry + struct.pack("<II", crc(prefix), crc(name)) + name)
    data = b"../../private-target"
    body = struct.pack(
        "<IIIHH7IBBH",
        2,
        1,
        stat.S_IFLNK | 0o777,
        0,
        0,
        len(data),
        0,
        0,
        0,
        0,
        len(data),
        len(data),
        0,
        0,
        0,
    )
    header = struct.pack("<HHI", 0x1985, 0xE002, 68 + len(data))
    prefix = header + struct.pack("<I", crc(header)) + body
    inode = node(0xE002, body + struct.pack("<II", crc(data), crc(prefix)) + data)
    return directory + inode, data


class FirmwareExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.exists():
            return
        spec = importlib.util.spec_from_file_location("extract_jffs2", SCRIPT)
        cls.extractor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.extractor)

    def module(self):
        self.assertTrue(SCRIPT.exists(), "Recovered extractor must be distributed")
        return self.extractor

    def test_wrong_image_does_not_create_output(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "wrong.bin"
            image.write_bytes(b"not the verified image")
            output = Path(tmp) / "output"
            with self.assertRaisesRegex(ValueError, "firmware_size_mismatch"):
                module.extract(image, output)
            self.assertFalse(output.exists())

    def test_same_size_wrong_digest_does_not_create_output(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "wrong.bin"
            image.write_bytes(b"\0" * module.IMAGE_SIZE)
            output = Path(tmp) / "output"
            with self.assertRaisesRegex(ValueError, "firmware_digest_mismatch"):
                module.extract(image, output)
            self.assertFalse(output.exists())

    def test_output_must_be_new_and_outside_repository(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "output_already_exists"):
                module.validate_output(Path(tmp))
        with self.assertRaisesRegex(ValueError, "output_inside_repository"):
            module.validate_output(ROOT / "private-extraction-test")

    def test_crc_scan_rejects_damaged_header(self):
        module = self.module()
        data, _ = fixture()
        self.assertEqual(len(module.scan_nodes(data)), 2)
        broken = bytearray(data)
        broken[8] ^= 1
        self.assertEqual(len(module.scan_nodes(broken)), 1)

    def test_reconstruction_keeps_symlink_as_numeric_file(self):
        module = self.module()
        data, target = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = module.reconstruct(data, module.scan_nodes(data), Path(tmp))
            record = manifest["/link"]
            self.assertTrue(record["symlink"])
            artifact = Path(record["file"])
            self.assertEqual(artifact.name, "2.bin")
            self.assertFalse(artifact.is_symlink())
            self.assertEqual(artifact.read_bytes(), target)
            self.assertEqual(list((Path(tmp) / "inode-store").iterdir()), [artifact])

    def test_corrupted_inode_data_is_rejected(self):
        module = self.module()
        data, _ = fixture()
        broken = data[:-1] + bytes([data[-1] ^ 1])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "node_crc_mismatch"):
                module.reconstruct(broken, module.scan_nodes(broken), Path(tmp))

    def test_rtime_overlap(self):
        self.assertEqual(
            self.module().rtime(b"A\x00B\x00A\x03", 6), b"ABA" + b"BA" + b"B"
        )


if __name__ == "__main__":
    unittest.main()
