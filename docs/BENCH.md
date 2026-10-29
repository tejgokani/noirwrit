# Benchmarks

Machine: Apple M3, 16 GB, macOS 27.0.1. Date: 2026-10-29. version: 0.4.1 (build 10964, commit b29c606e2).

Generation speed feeds the ETA shown in the app (the worker keeps a rolling average of real tok/s).
Rows marked random weights use the exact trained layout; speed and memory do not depend on what the weights learned.

| Model | Params | Runtime | File | Gen tok/s | Prompt tok/s | Peak RAM |
|---|---|---|---|---|---|---|
| tiny (trained) | 4.9M | llama.cpp Q8_0 | 9.1 MB | 1601.1 | 80174.1 | 0.093 GB |
| tiny (trained) | 4.9M | llama.cpp Q4_K_M | 7.3 MB | 596.3 | 63501.0 | 0.092 GB |
| tiny (trained) | 4.9M | PyTorch CPU int8 |  | 232.72 |  |  |
| tiny (trained) | 4.9M | PyTorch CPU fp32 |  | 332.97 |  |  |
| small (random weights) | 34.1M | llama.cpp Q8_0 | 45.7 MB | 293.7 | 26432.9 | 0.153 GB |
| small (random weights) | 34.1M | llama.cpp Q4_K_M | 28.7 MB | 767.0 | 31420.4 | 0.137 GB |
| small (random weights) | 34.1M | PyTorch CPU int8 |  | 111.86 |  |  |
| small (random weights) | 34.1M | PyTorch CPU fp32 |  | 168.23 |  |  |
| base (trained) | 97.5M | llama.cpp Q8_0 | 117.6 MB | 229.0 | 8704.9 | 0.259 GB |
| base (trained) | 97.5M | llama.cpp Q4_K_M | 69.2 MB | 298.3 | 9934.5 | 0.214 GB |
| base (trained) | 97.5M | PyTorch CPU int8 |  | 56.74 |  |  |
| base (trained) | 97.5M | PyTorch CPU fp32 |  | 67.58 |  |  |

## Quality gates (plan.md section 6) for the base model

- Speed, at least 20 tok/s int8: **229.0 tok/s** with llama.cpp Q8_0 (pass).
- Laptop RAM under 3 GB during generation: **0.259 GB** peak for llama.cpp (pass).
- Chapter under 5 min for 3000 words (~4050 tokens): **0.3 min** of pure generation (pass). Prompt prefill per scene adds a few seconds.

## ETA accuracy

Model: `noirwrit-base-q8_0.gguf`, 4 chapters of 3000 words. The rolling tok/s is calibrated on chapter 1.

| Chapter | Predicted | Actual | Error |
|---|---|---|---|
| 1 | calibrating | 22.2 s |  |
| 2 | 21.9 s | 23.2 s | 6% |
| 3 | 21.6 s | 22.7 s | 5% |
| 4 | 22.2 s | 23.5 s | 6% |

Worst error after calibration: **6%** (target under 20%: pass).
