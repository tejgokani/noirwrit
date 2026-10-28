# Progress

Last updated 2026-10-29.

| Phase | Status | Acceptance |
|---|---|---|
| 1. Repo and tooling | done | pytest runs; the guard kills a deliberate RAM hog (API and CLI) |
| 2. Data | done | 1,828 public domain books, 134.7M words, 99.71% of paragraphs pass the sanity filter (`data/STATS.md`) |
| 3. Tokenizer | done | 16k BPE, exact round trip, 1.36 tokens per word, uint16 shards (180M training tokens) |
| 4. Model and local smoke test | done | tiny loss 9.7 to 4.96 in 330 steps, resume works, 3.15 GB peak, no thermal pause |
| 5. Runtime and export | done | greedy output identical in PyTorch, llama.cpp f32 and Q8_0; base layout 213 tok/s, 0.26 GB (`docs/BENCH.md`) |
| 6. Online training | **blocked on the human step** | kit, plan and launcher ready; needs `~/.kaggle/kaggle.json` (see `docs/ONLINE_TRAINING.md`) |
| 7. Memory | done | ingest, retrieval accuracy, duplicate detection tests pass |
| 8. Story engine | done | tiny model wrote a 5-chapter story end to end; checker catches a planted name error |
| 9. Worker and ETA | done | SIGKILL mid-chapter then resume finishes without rewriting saved scenes; real ETA error 4% |
| 10. Interface | mostly done | all screens, live typing, exports verified in the browser; still to do: offline run with network blocked, epubcheck |
| 11. Packaging | not started | |

## Why the prose is not good yet

Every chapter so far came from the 5M parameter tiny model, trained for 7 minutes on the laptop. Its job is to prove the pipeline. It cannot write grammatical English, and decoding tricks do not change that (best-of-3 reranking moved the non-word rate from 1.8% to 1.5%). Proper prose needs the 98M base model trained on the full corpus: 4 epochs, about 8 hours on a free Kaggle T4 (`docs/TRAINING_PLAN.txt`).

## Next

1. User adds the Kaggle token, then `make train-online`.
2. Pull the base model, export, benchmark, write five sample chapters to `docs/samples/`.
3. Phase 10 offline check and epubcheck, then Phase 11.
