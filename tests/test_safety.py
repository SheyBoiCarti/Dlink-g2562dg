"""Offline safety checks. Run: python -m unittest discover -s dlink-g2562dg/tests -v"""
import pathlib
import os
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASH = shutil.which('bash')
if os.name == 'nt':
    git = shutil.which('git')
    candidates = ([pathlib.Path(git).parents[1] / 'bin' / 'bash.exe'] if git else [])
    candidates.append(pathlib.Path('C:/Program Files/Git/bin/bash.exe'))
    BASH = next((str(p) for p in candidates if p.is_file()), BASH)
if not BASH:
    raise RuntimeError('Tests require Bash: Git Bash on Windows, or bash on Linux.')

class SafetyTests(unittest.TestCase):
    def test_rejects_other_targets_before_network(self):
        for script in ('check_ports.sh', 'inspect_http.sh'):
            self.assertTrue((ROOT / 'scripts' / script).exists(), script + ' missing')
            for target in ('127.0.0.1', '10.0.0.3', '--bad', '10.0.0.2/other'):
                r = subprocess.run([str(BASH), str(ROOT / 'scripts' / script), target],
                                   capture_output=True, text=True, timeout=5)
                self.assertEqual(r.returncode, 2, (script, target, r.stdout, r.stderr))
                self.assertNotIn('UTC', r.stdout)

    def test_http_header_redaction(self):
        script = ROOT / 'scripts' / 'inspect_http.sh'
        self.assertTrue(script.exists(), 'inspect_http.sh missing')
        source = script.read_text().split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
        # Exercise actual production formatter without making any connections.
        scope = {'__name__': 'offline_test'}
        exec(compile(source, str(script), 'exec'), scope)
        from email.message import Message
        headers = Message()
        headers['Server'] = 'test-server/1.0'
        headers['Content-Type'] = 'text/html; token=SECRET'
        headers['Set-Cookie'] = 'session=SECRET'
        headers['Location'] = 'http://elsewhere/?token=SECRET'
        headers['WWW-Authenticate'] = 'Basic realm="SECRET"'
        result = scope['summarize_headers'](302, headers)
        self.assertNotIn('SECRET', str(result))
        self.assertNotIn('elsewhere', str(result))
        self.assertEqual(result['auth_challenge'], 'Basic')
        self.assertTrue(result['redirect_present'])

if __name__ == '__main__':
    unittest.main()
