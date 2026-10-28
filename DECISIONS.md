# Decisions

Each entry: date, decision, reason.

## 2026-10-28

- **Phase 0 answers** are in `config/requirements.json`: local web app, dark and light themes, reader mode with a chapter sidebar, a progress/ETA bar, keyboard shortcuts, public MIT repo, own model plus a tiny pretrained embedder, public domain data only, English, 3000-word chapters with a noir-first genre mix.
- **GPU and budget.** The answers first conflicted: RunPod (paid) as the provider with a $0 budget. The user resolved it as Kaggle free first, with RunPod/Vast.ai as a fallback capped at $8. All cost guards use $8.
- **Package layout.** plan.md lists `tokenizer/ model/ train/ runtime/ memory/ planner/ app/` at the top level. Those names make poor top-level Python packages (`model`, `app` and `memory` collide easily) and would block a clean PyPI install. They live under `noirwrit/` instead: `noirwrit/tokenizer`, `noirwrit/model`, and so on. `data/ tools/ tests/ config/ docs/` stay at the top level. Large outputs go to the gitignored `artifacts/` folder.
- **Python.** The system default is 3.14. The venv uses Python 3.11 through `uv` for wheel availability (torch, WeasyPrint).
- **Disk.** Only 34 GB free (93% used). Keep the raw corpus compressed or deleted after cleaning, keep only the latest and best checkpoints, and never download multi-GB datasets.
- **Thermal check without sudo.** `powermetrics` needs root and passwordless sudo is not set up. The guard tries `sudo -n powermetrics` and falls back to `pmset -g therm` (CPU speed limit and warning level), which works without a password.
- **Guard polling.** RSS is polled every 0.5 s even though the plan says 30 s, because memory can spike past the ceiling between 30 s checks. Swap and thermal checks run every 30 s.
- **No AI attribution** on commits, per the user's standing preference.
