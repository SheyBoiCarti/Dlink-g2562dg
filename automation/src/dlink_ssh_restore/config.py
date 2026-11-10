"""Strict configuration: the verified device and shell layout are fixed."""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    host: str = "10.0.0.2"
    trusted_network: str = "10.0.0.0/24"
    local_address: str = "10.0.0.10"
    telnet_user: str = "root"
    owner: str = ""
    host_fingerprint: str = ""
    private_key: str = ""
    public_key: str = ""
    timeout: int = 15
    min_ram_kib: int = 16384
    attempts: int = 5
    backoff_seconds: int = 15
    monitor_seconds: int = 120

    def __post_init__(self) -> None:
        import ipaddress

        if (
            self.host != "10.0.0.2"
            or self.trusted_network != "10.0.0.0/24"
            or self.telnet_user != "root"
        ):
            raise ValueError("Only the verified router and trusted LAN are supported")
        addr = ipaddress.IPv4Address(self.local_address)
        if addr not in ipaddress.IPv4Network(self.trusted_network) or str(addr) in (
            self.host,
            "10.0.0.0",
            "10.0.0.255",
        ):
            raise ValueError("Invalid trusted local source address")
        if self.owner and not re.fullmatch(r"[a-f0-9]{32}", self.owner):
            raise ValueError("Invalid owner identifier")
        if self.host_fingerprint and not re.fullmatch(
            r"SHA256:[A-Za-z0-9+/]{43}", self.host_fingerprint
        ):
            raise ValueError("Invalid host fingerprint")
        for value, low, high in [
            (self.timeout, 2, 60),
            (self.min_ram_kib, 16384, 1048576),
            (self.attempts, 1, 10),
            (self.backoff_seconds, 5, 60),
            (self.monitor_seconds, 60, 3600),
        ]:
            if type(value) is not int or not low <= value <= high:
                raise ValueError("Invalid bounded timing or RAM setting")

    @classmethod
    def load(cls, path: Path) -> "Config":
        with path.open("rb") as f:
            data = tomllib.load(f)
        obj = cls(**data)
        if not all((obj.owner, obj.host_fingerprint, obj.private_key, obj.public_key)):
            raise ValueError("Run setup to complete configuration")
        if (
            not Path(obj.private_key).is_absolute()
            or not Path(obj.public_key).is_absolute()
        ):
            raise ValueError("Key paths must be absolute")
        return obj
