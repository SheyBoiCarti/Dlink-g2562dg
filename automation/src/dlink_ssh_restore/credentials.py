"""Explicit Windows vault backend; no plaintext fallback."""

import sys

from .restore import RestoreError


class Credentials:
    def __init__(self, owner: str):
        if sys.platform != "win32":
            raise RestoreError("windows_credential_manager_required")
        from keyring.backends.Windows import WinVaultKeyring

        self.backend = WinVaultKeyring()
        self.service = "dlink-ssh-restore/" + owner

    def get(self, name: str) -> str:
        try:
            value = self.backend.get_password(self.service, name)
        except Exception:
            raise RestoreError("credential_vault_unavailable") from None
        if value is None:
            raise RestoreError("credential_missing_run_setup")
        return value

    def set(self, name: str, value: str) -> None:
        try:
            self.backend.set_password(self.service, name, value)
        except Exception:
            raise RestoreError("credential_vault_write_failed") from None
