"""Small, dependency-free collectors for local diagnostic information."""

from __future__ import annotations

import ctypes
import json
import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime, timezone
from typing import Any


DEFAULT_SERVICES = ("LanmanServer", "Dnscache", "TermService", "w32time")


def _run(command: list[str]) -> subprocess.CompletedProcess[str] | None:
    """Run a short local command without raising if it is unavailable."""
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None


def collect_system() -> dict[str, Any]:
    """Collect basic host, OS, CPU and memory information."""
    result: dict[str, Any] = {
        "hostname": socket.gethostname(),
        "operating_system": platform.platform(),
        "architecture": platform.machine(),
        "logical_cpu_count": os.cpu_count(),
    }
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong), ("memory_load", ctypes.c_ulong),
                ("total_physical", ctypes.c_ulonglong), ("available_physical", ctypes.c_ulonglong),
                ("total_page_file", ctypes.c_ulonglong), ("available_page_file", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong),
                ("available_extended_virtual", ctypes.c_ulonglong),
            ]
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            result["memory"] = {
                "total_bytes": status.total_physical,
                "available_bytes": status.available_physical,
                "used_percent": status.memory_load,
            }
    return result


def _drive_roots() -> list[str]:
    if os.name != "nt":
        return [os.path.abspath(os.sep)]
    mask = ctypes.windll.kernel32.GetLogicalDrives()
    return [f"{chr(65 + index)}:\\" for index in range(26) if mask & (1 << index)]


def collect_disks() -> list[dict[str, Any]]:
    """Collect free-space figures for mounted drive letters."""
    disks = []
    for root in _drive_roots():
        try:
            usage = shutil.disk_usage(root)
        except OSError:
            continue
        disks.append({
            "path": root,
            "total_bytes": usage.total,
            "free_bytes": usage.free,
            "free_percent": round((usage.free / usage.total) * 100, 1) if usage.total else 0,
        })
    return disks


def collect_network() -> dict[str, Any]:
    """Get active Windows adapter addresses, gateway and DNS using read-only cmdlets."""
    result: dict[str, Any] = {"adapters": []}
    if os.name != "nt":
        result["hostname_addresses"] = sorted(set(socket.gethostbyname_ex(socket.gethostname())[2]))
        return result
    command = [
        "powershell", "-NoProfile", "-Command",
        "Get-NetIPConfiguration | Where-Object {$_.IPv4Address -or $_.IPv6Address} | "
        "Select-Object InterfaceAlias,InterfaceIndex,IPv4Address,IPv6Address,IPv4DefaultGateway,DnsServer | ConvertTo-Json -Depth 4",
    ]
    completed = _run(command)
    if not completed or completed.returncode != 0 or not completed.stdout.strip():
        result["note"] = "Network cmdlets were unavailable; no adapter details were collected."
        return result
    try:
        adapters = json.loads(completed.stdout)
        result["adapters"] = adapters if isinstance(adapters, list) else [adapters]
    except json.JSONDecodeError:
        result["note"] = "Network information could not be parsed."
    return result


def collect_services(names: tuple[str, ...] = DEFAULT_SERVICES) -> list[dict[str, str]]:
    """Query selected service states. This does not start, stop or alter services."""
    services = []
    for name in names:
        completed = _run(["sc", "query", name])
        text = (completed.stdout + completed.stderr) if completed else ""
        if not completed or completed.returncode != 0:
            state = "NOT_FOUND"
        elif "RUNNING" in text:
            state = "RUNNING"
        elif "STOPPED" in text:
            state = "STOPPED"
        else:
            state = "UNKNOWN"
        services.append({"name": name, "state": state})
    return services


def collect_report(services: tuple[str, ...] = DEFAULT_SERVICES) -> dict[str, Any]:
    """Build one timestamped, JSON-serialisable report."""
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "collection_mode": "local_read_only",
        "system": collect_system(),
        "disks": collect_disks(),
        "network": collect_network(),
        "services": collect_services(services),
    }
