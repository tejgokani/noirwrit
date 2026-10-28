import subprocess
import sys
import time
from pathlib import Path

from noirwrit.guardrails import GuardLimits, ThermalGate, run_guarded, thermal_level

ROOT = Path(__file__).resolve().parents[1]

# Allocates 64 MB per step and touches every page so the memory is resident.
RAM_HOG = (
    "import time\n"
    "chunks = []\n"
    "for _ in range(64):\n"
    "    chunks.append(bytearray(b'x' * (64 * 1024 * 1024)))\n"
    "    time.sleep(0.05)\n"
    "time.sleep(30)\n"
)


def fast_limits(**kw) -> GuardLimits:
    base = dict(interval_s=0.2, caffeinate=False, duty_load_s=3600, timeout_s=60)
    base.update(kw)
    return GuardLimits(**base)


def test_guard_kills_ram_hog():
    t0 = time.monotonic()
    report = run_guarded(
        [sys.executable, "-c", RAM_HOG],
        fast_limits(max_rss_gb=0.5),
        thermal_fn=lambda: "nominal",
        swap_fn=lambda: 0,
        nice=0,
    )
    assert report.killed_reason and report.killed_reason.startswith("rss")
    assert report.returncode != 0
    # Killed well before the hog's 30 s sleep would finish.
    assert time.monotonic() - t0 < 20
    # Caught near the ceiling, not after it ran away.
    assert report.peak_rss_gb < 1.0


def test_guard_passes_exit_code():
    report = run_guarded(
        [sys.executable, "-c", "import sys; sys.exit(3)"],
        fast_limits(),
        thermal_fn=lambda: "nominal",
        swap_fn=lambda: 0,
        nice=0,
    )
    assert report.killed_reason is None
    assert report.returncode == 3


def test_guard_kills_on_swap_storm():
    counter = iter(range(0, 10**9, 100000))
    report = run_guarded(
        [sys.executable, "-c", "import time; time.sleep(20)"],
        fast_limits(max_swapout_pages=1000),
        thermal_fn=lambda: "nominal",
        swap_fn=lambda: next(counter),
        nice=0,
    )
    assert report.killed_reason and "swap storm" in report.killed_reason


def test_guard_pauses_when_hot():
    levels = iter(["serious"] + ["nominal"] * 1000)
    report = run_guarded(
        [sys.executable, "-c", "import time; time.sleep(1.5)"],
        fast_limits(hot_pause_s=0.5),
        thermal_fn=lambda: next(levels),
        swap_fn=lambda: 0,
        nice=0,
    )
    assert report.returncode == 0
    assert "thermal:serious" in report.pauses


def test_guard_duty_cycle_rests():
    report = run_guarded(
        [sys.executable, "-c", "import time; time.sleep(1.5)"],
        fast_limits(duty_load_s=0.5, duty_rest_s=0.3),
        thermal_fn=lambda: "nominal",
        swap_fn=lambda: 0,
        nice=0,
    )
    assert report.returncode == 0
    assert "duty" in report.pauses


def test_guard_cli_kills_ram_hog():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "guard.py"), "--max-rss-gb", "0.5",
         "--interval", "0.2", "--no-caffeinate", "--nice", "0", "--timeout-min", "1",
         "--", sys.executable, "-c", RAM_HOG],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 137
    assert "KILL" in r.stderr


def test_thermal_level_returns_known_value():
    assert thermal_level() in {"nominal", "fair", "serious", "critical", "unknown"}


def test_thermal_gate_pauses_only_when_hot():
    gate = ThermalGate(interval_s=0, hot_pause_s=0.01, thermal_fn=lambda: "critical")
    assert gate.wait_if_hot() is True
    gate = ThermalGate(interval_s=0, hot_pause_s=0.01, thermal_fn=lambda: "nominal")
    assert gate.wait_if_hot() is False
