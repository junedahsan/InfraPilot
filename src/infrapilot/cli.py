"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from .collectors import DEFAULT_SERVICES, collect_report
from .report import render_text, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect a local, read-only infrastructure health report.")
    parser.add_argument("--output", type=Path, help="Save the full JSON report to this path.")
    parser.add_argument("--services", nargs="*", default=list(DEFAULT_SERVICES), help="Windows service names to query.")
    args = parser.parse_args()
    report = collect_report(tuple(args.services))
    print(render_text(report))
    if args.output:
        write_json(report, args.output)
        print(f"\nFull JSON report saved locally to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
