"""Windows-only, read-only task-definition integration. Registration is forbidden."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(
    os.name != "nt" or shutil.which("pwsh") is None,
    reason="Windows PowerShell 7/CIM required",
)
def test_task_installer_whatif_builds_valid_event_trigger_without_registration(
    tmp_path,
):
    installer = Path(__file__).resolve().parents[1] / "windows/install-task.ps1"
    config = tmp_path / "config.toml"
    config.write_text("# nonsecret syntax-only test fixture\n")
    wrapper = tmp_path / "whatif.ps1"
    wrapper.write_text("""param([string]$Installer,[string]$Python,[string]$Config)
$ErrorActionPreference='Stop'
function Get-ScheduledTask { param($TaskName,$ErrorAction) return $null }
function Register-ScheduledTask { throw 'Registration forbidden in offline test' }
& $Installer -Python $Python -Config $Config -WhatIf
""")
    result = subprocess.run(
        [
            shutil.which("pwsh"),
            "-NoProfile",
            "-NonInteractive",
            "-File",
            str(wrapper),
            "-Installer",
            str(installer),
            "-Python",
            sys.executable,
            "-Config",
            str(config),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr
