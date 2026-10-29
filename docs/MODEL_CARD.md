# Model card: noirwrit-base

## Summary

| Item | Value |
|---|---|
| Architecture | Decoder-only transformer written from scratch, Llama-compatible layout: 12 layers, d_model 768, 12 heads, SwiGLU (2048), RMSNorm, RoPE (theta 10000), tied embeddings |
| Parameters | 97.5M |
| Context | 2048 tokens |
| Tokenizer | Own byte-level BPE, 16,384 tokens, trained on the same corpus |
| Training data | 1,828 public domain books from Project Gutenberg, all published 1930 or earlier (`data/SOURCES.md`) |
| Training tokens | 719M (4 epochs over 180M tokens) |
| Hardware | One Tesla T4 on Kaggle's free tier, fp16 with a gradient scaler, `torch.compile` |
| Training time | 9.6 hours, 10,973 steps of 65,536 tokens, median 21,080 tokens/s |
| Cost | $0 |
| Files | `noirwrit-base-q8_0.gguf` (112 MB), `noirwrit-base-q4_k_m.gguf` (66 MB), `best.pt` (fp16 PyTorch, 210 MB) |
| License | MIT (code and weights); the training text is public domain in the US |

## Training

Three-stage curriculum:

| Stage | Data | Share of steps | Learning rate | Best validation loss |
|---|---|---|---|---|
| 1. General fiction | adventure, gothic and other pre-1931 fiction (40M tokens) | 15% | 6e-4, cosine | 3.79 |
| 2. Crime and detective | Doyle, Christie's early novels, Chesterton, Collins, Green, Rinehart and others (136M tokens) | 75% | 6e-4, cosine | 3.14 |
| 3. Noir voice | Hammett, Burnett, Whitfield, Packard and dated pulp (4M tokens) | 10% | 0.3x, early stop | 2.55 |

Validation is the last 2% of every book. Each stage's loss is measured on that stage's own validation set, so the numbers compare within a stage, not across stages. The released weights are the best noir-stage checkpoint (validation loss 2.55, perplexity about 12.8). For comparison, the 5M tiny smoke-test model reached 5.31 on the crime set.

## Speed on a MacBook Air M3 (16 GB)

| Runtime | Generation | Peak RAM |
|---|---|---|
| llama.cpp Q8_0 (Metal) | 229 tokens/s | 0.26 GB |
| llama.cpp Q4_K_M | 298 tokens/s | 0.21 GB |
| PyTorch CPU int8 (fallback) | 57 tokens/s | |

A 3,000-word chapter takes about 23 seconds. ETA error with this model is under 6% (`docs/BENCH.md`).

## What it does well

Writes grammatical, period-flavoured English prose in the voice of early twentieth-century detective and pulp fiction: dialogue with natural attribution, scene description, and the cadence of the Gutenberg-era crime novel. Samples are in `docs/samples/`.

## Limits

- It is a 98M model. It keeps a sentence and usually a paragraph together, but loses track of details over a page: a character found dead may be spoken to a paragraph later, or a woman's hair may change colour. The planner, story bible, memory and consistency pass supply the plot logic and fix what they can (names, dead characters speaking, clue order). They do not make the model reason.
- Public domain data means a classic voice (1880s to 1930), not modern thriller pacing or modern idiom. Expect archaic spellings like "clew".
- It reproduces the attitudes and stereotypes of its source era. Read samples with that in mind.
- It sometimes echoes famous characters from its training books; the consistency pass replaces their names with the story's own cast.
- "Learns" means Noirwrit remembers and retrieves earlier stories. The weights do not change on the laptop.

## Reproduce

```
python -m noirwrit.corpus.build
python -m noirwrit.tokenizer.train_tokenizer
make train-online        # Kaggle, see docs/ONLINE_TRAINING.md
```
