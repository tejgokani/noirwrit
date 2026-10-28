"""Resource guard for running heavy jobs on a fanless MacBook Air.

Watches a child process tree and enforces:
- an RSS ceiling (kill when exceeded),
- a swap-out growth limit (kill to protect the SSD),
- thermal pressure (pause with SIGSTOP when Serious or Critical),
- a duty cycle (pause after N minutes of load, then resume).

Used by tools/guard.py and by the background worker.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field

import psutil

THERMAL_LEVELS = ["nominal", "fair", "serious", "critical", "unknown"]


@dataclass
class GuardLimits:
    max_rss_gb: float = 9.0
    interval_s: float = 30.0
    # Swap pages written per interval before we treat it as a swap storm.
    # 16 KB pages on Apple Silicon, so 32768 pages is about 512 MB.
    max_swapout_pages: int = 32768
    hot_levels: tuple[str, ...] = ("serious", "critical")
    hot_pause_s: float = 240.0
    duty_load_s: float = 600.0
    duty_rest_s: float = 180.0
    timeout_s: float | None = None
    caffeinate: bool = True


@dataclass
class GuardReport:
    returncode: int | None = None
    killed_reason: str | None = None
    peak_rss_gb: float = 0.0
    pauses: list[str] = field(default_factory=list)
    duration_s: float = 0.0


def tree_rss_bytes(proc: psutil.Process) -> int:
    """RSS of a process and all its descendants."""
    total = 0
    try:
        procs = [proc, *proc.children(recursive=True)]
    except psutil.NoSuchProcess:
        return 0
    for p in procs:
        try:
            total += p.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return total


def swapouts() -> int | None:
    """Cumulative swap-out page count from vm_stat, or None if unavailable."""
    if not shutil.which("vm_stat"):
        return None
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"Swapouts:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def thermal_level() -> str:
    """Best effort thermal pressure level without asking for a password.

    Tries `sudo -n powermetrics` (works only if passwordless sudo is set up),
    then falls back to `pmset -g therm`, which reports warning levels.
    """
    if shutil.which("powermetrics"):
        try:
            r = subprocess.run(
                ["sudo", "-n", "powermetrics", "--samplers", "thermal", "-i", "1", "-n", "1"],
                capture_output=True, text=True, timeout=10,
            )
            m = re.search(r"pressure level:\s*(\w+)", r.stdout, re.IGNORECASE)
            if r.returncode == 0 and m:
                return m.group(1).lower()
        except (OSError, subprocess.SubprocessError):
            pass
    if shutil.which("pmset"):
        try:
            out = subprocess.run(
                ["pmset", "-g", "therm"], capture_output=True, text=True, timeout=5
            ).stdout.lower()
        except (OSError, subprocess.SubprocessError):
            return "unknown"
        if "no thermal warning level has been recorded" in out or "no performance warning" in out:
            if "speed_limit" not in out:
                return "nominal"
        m = re.search(r"cpu_speed_limit\s*=\s*(\d+)", out)
        if m:
            limit = int(m.group(1))
            if limit >= 100:
                return "nominal"
            if limit >= 80:
                return "fair"
            if limit >= 50:
                return "serious"
            return "critical"
        m = re.search(r"thermal warning level[^0-9]*(\d+)", out)
        if m:
            return ["nominal", "fair", "serious", "critical"][min(int(m.group(1)), 3)]
        return "nominal"
    return "unknown"


def _signal_tree(proc: psutil.Process, sig: int) -> None:
    try:
        procs = [*proc.children(recursive=True), proc]
    except psutil.NoSuchProcess:
        return
    for p in procs:
        try:
            p.send_signal(sig)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def kill_tree(proc: psutil.Process, popen: subprocess.Popen | None = None, grace_s: float = 3.0) -> None:
    """SIGTERM the tree, then SIGKILL. Waits through Popen when given, so the
    exit code is not lost (psutil's wait would reap the child first)."""
    _signal_tree(proc, signal.SIGTERM)
    try:
        if popen is not None:
            popen.wait(timeout=grace_s)
        else:
            proc.wait(timeout=grace_s)
    except (psutil.TimeoutExpired, subprocess.TimeoutExpired):
        _signal_tree(proc, signal.SIGKILL)


def log(msg: str) -> None:
    print(f"[guard {time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def run_guarded(
    cmd: list[str],
    limits: GuardLimits | None = None,
    thermal_fn=thermal_level,
    swap_fn=swapouts,
    nice: int = 10,
) -> GuardReport:
    """Run cmd under the guard. Returns a report; never raises on limit breach."""
    limits = limits or GuardLimits()
    report = GuardReport()
    start = time.monotonic()

    def preexec() -> None:
        os.setpgrp()
        if nice:
            os.nice(nice)

    popen = subprocess.Popen(cmd, preexec_fn=preexec)
    proc = psutil.Process(popen.pid)
    caf = None
    if limits.caffeinate and shutil.which("caffeinate"):
        caf = subprocess.Popen(["caffeinate", "-i", "-w", str(popen.pid)])

    last_swap = swap_fn()
    load_since = time.monotonic()
    max_rss = limits.max_rss_gb * 1024**3
    # Poll RSS often (memory can spike fast) but run the slower thermal and
    # swap checks only every interval_s.
    fast_poll = min(0.5, limits.interval_s)
    next_slow = time.monotonic() + limits.interval_s

    try:
        while popen.poll() is None:
            time.sleep(fast_poll)
            if popen.poll() is not None:
                break
            rss = tree_rss_bytes(proc)
            report.peak_rss_gb = max(report.peak_rss_gb, rss / 1024**3)
            if rss > max_rss:
                report.killed_reason = f"rss {rss / 1024**3:.2f} GB > {limits.max_rss_gb} GB"
                log("KILL: " + report.killed_reason)
                kill_tree(proc, popen)
                break

            now = time.monotonic()
            if limits.timeout_s and now - start > limits.timeout_s:
                report.killed_reason = f"timeout {limits.timeout_s:.0f}s"
                log("KILL: " + report.killed_reason)
                kill_tree(proc, popen)
                break
            if now < next_slow:
                continue
            next_slow = now + limits.interval_s

            cur_swap = swap_fn()
            if cur_swap is not None and last_swap is not None:
                delta = cur_swap - last_swap
                if delta > limits.max_swapout_pages:
                    report.killed_reason = f"swap storm: {delta} pages swapped out in one interval"
                    log("KILL: " + report.killed_reason)
                    kill_tree(proc, popen)
                    break
            last_swap = cur_swap

            level = thermal_fn()
            if level in limits.hot_levels:
                report.pauses.append(f"thermal:{level}")
                log(f"thermal {level}: pausing {limits.hot_pause_s:.0f}s")
                _signal_tree(proc, signal.SIGSTOP)
                time.sleep(limits.hot_pause_s)
                _signal_tree(proc, signal.SIGCONT)
                load_since = time.monotonic()
                continue

            if now - load_since > limits.duty_load_s:
                report.pauses.append("duty")
                log(f"duty cycle: resting {limits.duty_rest_s:.0f}s")
                _signal_tree(proc, signal.SIGSTOP)
                time.sleep(limits.duty_rest_s)
                _signal_tree(proc, signal.SIGCONT)
                load_since = time.monotonic()
                last_swap = swap_fn()
    except KeyboardInterrupt:
        report.killed_reason = "interrupted"
        kill_tree(proc, popen)
    finally:
        if caf and caf.poll() is None:
            caf.terminate()

    report.returncode = popen.wait()
    report.duration_s = time.monotonic() - start
    return report


class ThermalGate:
    """In-process thermal check for long running workers.

    Call `wait_if_hot()` between units of work. Checks at most every interval_s.
    """

    def __init__(self, interval_s: float = 30.0, hot_pause_s: float = 240.0,
                 hot_levels: tuple[str, ...] = ("serious", "critical"), thermal_fn=thermal_level):
        self.interval_s = interval_s
        self.hot_pause_s = hot_pause_s
        self.hot_levels = hot_levels
        self.thermal_fn = thermal_fn
        self._last = 0.0

    def wait_if_hot(self) -> bool:
        now = time.monotonic()
        if now - self._last < self.interval_s:
            return False
        self._last = now
        level = self.thermal_fn()
        if level in self.hot_levels:
            log(f"thermal {level}: worker pausing {self.hot_pause_s:.0f}s")
            time.sleep(self.hot_pause_s)
            return True
        return False
