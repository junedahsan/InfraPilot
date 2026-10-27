"""Human-friendly rendering and local report writing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _bytes(value: int | None) -> str:
    if value is None:
        return "unknown"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return "unknown"


def render_text(report: dict[str, Any]) -> str:
    system = report["system"]
    lines = ["InfraPilot — Local Infrastructure Health Report", "=" * 48]
    lines += [f"Computer: {system['hostname']}", f"OS: {system['operating_system']}", f"Logical CPUs: {system['logical_cpu_count']}"]
    memory = system.get("memory")
    if memory:
        lines.append(f"Memory: {memory['used_percent']}% used ({_bytes(memory['available_bytes'])} available)")
    lines += ["", "Disk space:"]
    for disk in report["disks"]:
        status = "WARNING" if disk["free_percent"] < 15 else "PASS"
        lines.append(f"  [{status}] {disk['path']} — {disk['free_percent']}% free ({_bytes(disk['free_bytes'])})")
    lines += ["", "Selected services:"]
    for service in report["services"]:
        status = "PASS" if service["state"] == "RUNNING" else "CHECK"
        lines.append(f"  [{status}] {service['name']}: {service['state']}")
    adapters = report["network"].get("adapters", [])
    lines += ["", f"Network adapters found: {len(adapters)}", "", "Privacy: this report was collected locally. InfraPilot did not upload it."]
    return "\n".join(lines)


def write_json(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
