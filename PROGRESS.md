# Progress

Last updated 2026-10-29 (evening).

| Phase | Status | Acceptance |
|---|---|---|
| 1. Repo and tooling | done | pytest runs; the guard kills a deliberate RAM hog (API and CLI) |
| 2. Data | done | 1,828 public domain books, 134.7M words, 99.71% of paragraphs pass the sanity filter (`data/STATS.md`) |
| 3. Tokenizer | done | 16k BPE, exact round trip, 1.36 tokens per word, uint16 shards (180M training tokens) |
| 4. Model and local smoke test | done | tiny loss 9.7 to 4.96 in 330 steps, resume works, 3.15 GB peak, no thermal pause |
| 5. Runtime and export | done | greedy output identical in PyTorch, llama.cpp f32 and Q8_0; base layout 213 tok/s, 0.26 GB (`docs/BENCH.md`) |
| 6. Online training | done | base 97.5M trained on a free Kaggle T4: 719M tokens, 9.6 h, $0; best val 2.55 (noir set); five 3,000-word samples in `docs/samples/`; model card in `docs/MODEL_CARD.md` |
| 7. Memory | done | ingest, retrieval accuracy, duplicate detection tests pass |
| 8. Story engine | done | tiny model wrote a 5-chapter story end to end; checker catches a planted name error |
| 9. Worker and ETA | done | SIGKILL mid-chapter then resume finishes without rewriting saved scenes; real ETA error 4% |
| 10. Interface | mostly done | all screens, live typing, exports verified in the browser; still to do: offline run with network blocked, epubcheck |
| 11. Packaging | not started | |

## Prose quality

The trained base model writes grammatical, period-style English (see `docs/samples/`). It still loses track of details across a page, which is the expected limit of a 98M model; the planner and consistency pass cover plot logic. The earlier unreadable chapters came from the 5M tiny smoke-test model.

## Next

1. Phase 10: run the full flow with the network blocked, and validate EPUBs with epubcheck.
2. Phase 11: `make setup` from a clean clone, README with the architecture diagram and honest limits, name check, CI, and (with your OK) the public GitHub repo, PyPI and Hugging Face release.
