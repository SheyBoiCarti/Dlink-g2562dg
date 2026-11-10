"""Conservative exposure proof. Unsupported firewall syntax fails closed."""

import shlex

from .restore import RestoreError


class ExposureError(RestoreError):
    pass


def check_exposure(sockets: str, ipv4: str, ipv6: str) -> None:
    listeners = []
    for line in sockets.splitlines():
        fields = line.split()
        if (
            len(fields) >= 6
            and fields[0].startswith("tcp")
            and fields[-1] == "LISTEN"
            and fields[3].endswith(":2222")
        ):
            listeners.append(fields[3])
    if listeners != ["10.0.0.2:2222"]:
        raise ExposureError("unexpected_ipv4_or_ipv6_listener")
    # IPv6 policy is inspected, but absence of ANY v6 custom socket is the proof.
    if not any(line.startswith("-P INPUT ") for line in ipv6.splitlines()):
        raise ExposureError("ipv6_policy_unavailable")
    rules: dict[str, list[list[str]]] = {}
    policy = None
    for line in ipv4.splitlines():
        t = shlex.split(line)
        if t[:2] == ["-P", "INPUT"]:
            policy = t[2]
        if t and t[0] == "-N":
            rules.setdefault(t[1], [])
        if t and t[0] == "-A":
            rules.setdefault(t[1], []).append(t[2:])
    if policy not in ("DROP", "ACCEPT"):
        raise ExposureError("ipv4_policy_unavailable")

    def deny_only(chain: str, stack: tuple[str, ...] = ()) -> bool:
        # Removing a chain that can only drop or return enlarges the accepted
        # packet set. Proving denial in that larger set remains conservative.
        # Never ignore ACCEPT, state-changing targets, goto, or cycles.
        if chain in ("DROP", "REJECT", "RETURN"):
            return True
        if chain not in rules or chain in stack or len(stack) > 16:
            return False
        for rule in rules[chain]:
            if (
                len(rule) < 2
                or rule[-2] != "-j"
                or rule.count("-j") != 1
                or "-g" in rule
                or "--goto" in rule
            ):
                return False
            if not deny_only(rule[-1], stack + (chain,)):
                return False
        return True

    def walk(chain: str, interface: str, stack: tuple[str, ...]) -> str:
        if chain in stack or len(stack) > 16:
            raise ExposureError("firewall_cycle")
        for t in rules.get(chain, []):
            if (
                len(t) >= 2
                and t[-2] == "-j"
                and t.count("-j") == 1
                and t[-1] != "RETURN"
                and "-g" not in t
                and "--goto" not in t
                and deny_only(t[-1])
            ):
                continue
            match = True
            target = None
            i = 0
            negate = False
            while i < len(t):
                token = t[i]
                if token == "!":
                    if negate:
                        raise ExposureError("unsupported_firewall_syntax")
                    negate = True
                    i += 1
                    continue
                if token not in (
                    "-i",
                    "-p",
                    "--dport",
                    "--destination-port",
                    "-m",
                    "--state",
                    "--ctstate",
                    "--pkt-type",
                    "-j",
                ) or i + 1 >= len(t):
                    raise ExposureError("unsupported_firewall_syntax")
                value = t[i + 1]
                i += 2
                if token == "-j":
                    if negate:
                        raise ExposureError("unsupported_firewall_syntax")
                    target = value
                    continue
                if token == "-m":
                    if (
                        value not in ("tcp", "udp", "state", "conntrack", "pkttype")
                        or negate
                    ):
                        raise ExposureError("unsupported_firewall_match")
                    continue
                if token == "-i":
                    result = (
                        interface.startswith(value[:-1])
                        if value.endswith("+")
                        else interface == value
                    )
                elif token == "-p":
                    result = value in ("tcp", "6", "all")
                elif token == "--pkt-type":
                    if value not in ("unicast", "multicast", "broadcast"):
                        raise ExposureError("unsupported_packet_type")
                    result = value == "unicast"
                elif token in ("--state", "--ctstate"):
                    result = "NEW" in value.split(",")
                else:
                    try:
                        parts = value.split(":")
                        result = int(parts[0]) <= 2222 <= int(parts[-1])
                    except ValueError:
                        raise ExposureError("unsupported_firewall_port") from None
                match = match and (not result if negate else result)
                negate = False
            if negate or target is None:
                raise ExposureError("unsupported_firewall_syntax")
            if not match:
                continue
            if target in ("ACCEPT", "DROP", "REJECT", "RETURN"):
                return target
            if target in ("LOG", "NFLOG"):
                continue
            if target not in rules:
                raise ExposureError("unsupported_firewall_target")
            verdict = walk(target, interface, stack + (chain,))
            if verdict != "RETURN":
                return verdict
        return "RETURN"

    # Include every named ingress and an abstract future/unlisted interface.
    interfaces = {"__untrusted__"}
    for chain_rules in rules.values():
        for t in chain_rules:
            for i, v in enumerate(t[:-1]):
                if v == "-i":
                    interfaces.add(t[i + 1].replace("+", "__probe"))
    for interface in interfaces - {"lo", "br0"}:
        verdict = walk("INPUT", interface, ())
        if verdict == "ACCEPT" or (verdict == "RETURN" and policy != "DROP"):
            raise ExposureError("non_lan_ipv4_accept")


def check_mounts(mountinfo: str, staged: bool = False) -> None:
    """Reject source propagation surprises and incomplete/foreign scratch mounts."""
    scratch = "/tmp/dlink-phase6a"
    expected = {
        scratch + "/root/" + name
        for name in ("bin", "lib", "usr", "dev", "var", "dev/pts")
    }
    found = set()
    relevant = {"/", "/tmp", "/dev", "/dev/pts", "/bin", "/lib", "/usr", "/var"}
    for line in mountinfo.splitlines():
        fields = line.split()
        if len(fields) < 10 or "-" not in fields:
            raise ExposureError("mountinfo_unavailable")
        target = fields[4]
        if target in relevant or target.startswith(scratch + "/"):
            tags = fields[6 : fields.index("-")]
            if any(
                tag.startswith(("shared:", "master:", "propagate_from:"))
                for tag in tags
            ):
                raise ExposureError("unexpected_mount_propagation")
        if target == scratch or target.startswith(scratch + "/"):
            if target not in expected or target in found:
                raise ExposureError("unexpected_scratch_mount")
            found.add(target)
    if staged and found != expected:
        raise ExposureError("incomplete_owned_mounts")
    if not staged and found:
        raise ExposureError("unexpected_existing_mounts")
