#!/usr/bin/env python3
"""Print and log system health every N seconds: RAM, swap, thermal level.

Usage:
    python tools/monitor.py [--interval 30] [--csv logs/monitor.csv]

Stop with Ctrl+C.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import psutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from noirwrit.guardrails import swapouts, thermal_level  # noqa: E402


def top_python(n: int = 3) -> str:
    rows = []
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        name = (p.info.get("name") or "").lower()
        if "python" in name and p.info.get("memory_info"):
            rows.append((p.info["memory_info"].rss, p.info["pid"]))
    rows.sort(reverse=True)
    return " ".join(f"{pid}:{rss / 1024**3:.2f}G" for rss, pid in rows[:n])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=30.0)
    ap.add_argument("--csv", default="logs/monitor.csv")
    ap.add_argument("--count", type=int, default=0, help="stop after N samples (0 = forever)")
    a = ap.parse_args()

    path = Path(a.csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "ram_used_gb", "ram_pct", "swap_used_gb", "swapouts", "thermal"])
        i = 0
        try:
            while True:
                vm = psutil.virtual_memory()
                sw = psutil.swap_memory()
                row = [
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{vm.used / 1024**3:.2f}",
                    f"{vm.percent:.0f}",
                    f"{sw.used / 1024**3:.2f}",
                    swapouts(),
                    thermal_level(),
                ]
                w.writerow(row)
                f.flush()
                print(" ".join(map(str, row)), "py:", top_python(), flush=True)
                i += 1
                if a.count and i >= a.count:
                    break
                time.sleep(a.interval)
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
