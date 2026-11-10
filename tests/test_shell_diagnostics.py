"""Offline checks: no router connections, authentication or router writes."""
import pathlib
import subprocess
import unittest
from test_safety import BASH

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts/shell_diagnostics.sh'

class ShellDiagnosticSafety(unittest.TestCase):
    def test_capacity_never_targets_network_filesystems(self):
        text = SCRIPT.read_text()
        self.assertIn('# BEGIN LOCAL CAPACITY TARGETS', text)
        source = text.split('# BEGIN LOCAL CAPACITY TARGETS\n', 1)[1].split('# END LOCAL CAPACITY TARGETS', 1)[0]
        fixture = ('//host/share /mnt cifs rw 0 0\n'
                   'host:/data /data nfs rw 0 0\n'
                   '/dev/mtdblock3 / squashfs ro 0 0\n'
                   'overlay /overlay overlay rw 0 0\n'
                   'tmpfs /tmp tmpfs rw 0 0\n')
        run = subprocess.run([BASH, '-c', source], input=fixture, capture_output=True,
                             text=True, timeout=5)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines(), ['/', '/overlay', '/tmp'])

    def test_requires_review_before_collection(self):
        self.assertTrue(SCRIPT.exists(), 'shell_diagnostics.sh missing')
        for args, expected in (([], 2), (['--help'], 0), (['--unexpected'], 2)):
            run = subprocess.run([BASH, str(SCRIPT), *args], capture_output=True,
                                 text=True, timeout=5)
            self.assertEqual(run.returncode, expected, run.stderr)
            self.assertNotIn('=== Identity ===', run.stdout)

    def test_mount_formatter_withholds_secrets_and_preserves_mode(self):
        self.assertTrue(SCRIPT.exists(), 'shell_diagnostics.sh missing')
        # Test the actual awk formatter on hostile mount records, not the host mounts.
        source = SCRIPT.read_text().split('# BEGIN MOUNT FORMATTER\n', 1)[1].split('# END MOUNT FORMATTER', 1)[0]
        fixture = ('//SECRET-HOST/SECRET /mnt/SECRET cifs rw,user=SECRET,password=SECRET 0 0\n'
                   '/dev/mtdblock3 / squashfs ro,relatime 0 0\n'
                   'overlayfs /overlay overlay rw,lowerdir=SECRET 0 0\n')
        run = subprocess.run([BASH, '-c', source], input=fixture, capture_output=True,
                             text=True, timeout=5)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotIn('SECRET', run.stdout)
        self.assertIn('squashfs ro', run.stdout)
        self.assertIn('overlay rw', run.stdout)

if __name__ == '__main__':
    unittest.main()
