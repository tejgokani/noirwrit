# Progress

## Phase 1: Repo and tooling (done)
- Scaffold, pyproject (Python 3.11 via uv), ruff, pytest, pre-commit, MIT license, README, CONTRIBUTING, Makefile.
- `tools/guard.py` wraps any command: RSS ceiling (polled every 0.5 s), swap-storm kill, thermal pause, 10/3 minute duty cycle, `caffeinate -i` for the job only, `nice`.
- `tools/monitor.py` logs RAM, swap, swapouts and thermal level to `logs/monitor.csv`.
- Acceptance: `pytest` runs (8 guard tests pass). The guard kills a deliberate RAM hog through both the API and the CLI (exit 137).
- Notes: the network was slow during setup; torch is pinned to the cached 2.14.1 wheel.

## Phase 2: Data (in progress)
- Catalog-driven selection with per-title PD rules, cleaner, dedupe and stats writer are built and tested. The full download is running.

## Next
- Finish the Phase 2 download, then Phase 3 (tokenizer and shards).
