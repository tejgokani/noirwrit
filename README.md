# Noirwrit

Offline crime and noir chapter generator. Noirwrit runs its own small language model, trained from scratch on public domain detective and pulp fiction, on a laptop with no network calls.

Status: under construction. See `PROGRESS.md`.

## Quickstart

```bash
make setup
source .venv/bin/activate
pytest
```

## Running heavy jobs on a MacBook Air

The Air has no fan. Run every heavy local job through the guard, which kills the job if RAM passes 9 GB or swap starts to churn, and pauses it when the Mac runs hot:

```bash
python tools/guard.py --max-rss-gb 9 --timeout-min 10 -- <command>
```

## License

MIT. Training data is public domain in the US; see `data/SOURCES.md`.
