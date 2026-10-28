#!/usr/bin/env python3
"""Run a command under RAM, swap, thermal and duty-cycle limits.

Usage:
    python tools/guard.py [options] -- <command> [args...]

Example:
    python tools/guard.py --max-rss-gb 9 --timeout-min 10 -- python -m noirwrit.train.train --preset tiny

Exit code is the child's exit code, or 137 if the guard killed it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from noirwrit.guardrails import GuardLimits, log, run_guarded  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--" not in argv:
        print(__doc__, file=sys.stderr)
        return 2
    split = argv.index("--")
    opts, cmd = argv[:split], argv[split + 1:]
    if not cmd:
        print("guard: no command given", file=sys.stderr)
        return 2

    p = argparse.ArgumentParser(prog="guard")
    p.add_argument("--max-rss-gb", type=float, default=9.0)
    p.add_argument("--interval", type=float, default=30.0, help="seconds between swap/thermal checks")
    p.add_argument("--max-swapout-pages", type=int, default=32768)
    p.add_argument("--hot-pause-min", type=float, default=4.0)
    p.add_argument("--duty-load-min", type=float, default=10.0)
    p.add_argument("--duty-rest-min", type=float, default=3.0)
    p.add_argument("--timeout-min", type=float, default=None)
    p.add_argument("--no-caffeinate", action="store_true")
    p.add_argument("--nice", type=int, default=10)
    a = p.parse_args(opts)

    limits = GuardLimits(
        max_rss_gb=a.max_rss_gb,
        interval_s=a.interval,
        max_swapout_pages=a.max_swapout_pages,
        hot_pause_s=a.hot_pause_min * 60,
        duty_load_s=a.duty_load_min * 60,
        duty_rest_s=a.duty_rest_min * 60,
        timeout_s=a.timeout_min * 60 if a.timeout_min else None,
        caffeinate=not a.no_caffeinate,
    )
    report = run_guarded(cmd, limits, nice=a.nice)
    log(
        f"done rc={report.returncode} peak_rss={report.peak_rss_gb:.2f}GB "
        f"duration={report.duration_s:.0f}s pauses={report.pauses} killed={report.killed_reason}"
    )
    if report.killed_reason:
        return 137
    return report.returncode or 0


if __name__ == "__main__":
    sys.exit(main())
