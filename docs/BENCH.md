# Benchmarks

Machine: Apple M3, 16 GB, macOS 27.0.1. Date: 2026-10-28. version: 0.4.1 (build 10964, commit b29c606e2).

Generation speed feeds the ETA shown in the app (the worker keeps a rolling average of real tok/s).
Small and base rows use random weights in the exact trained layout; speed and memory do not depend on what the weights learned.

| Model | Params | Runtime | File | Gen tok/s | Prompt tok/s | Peak RAM |
|---|---|---|---|---|---|---|
| tiny (trained) | 4.9M | llama.cpp Q8_0 | 9.1 MB | 1190.3 | 58265.4 | 0.093 GB |
| tiny (trained) | 4.9M | llama.cpp Q4_K_M | 7.3 MB | 1536.7 | 87158.3 | 0.092 GB |
| tiny (trained) | 4.9M | PyTorch CPU int8 |  | 241.39 |  |  |
| tiny (trained) | 4.9M | PyTorch CPU fp32 |  | 321.86 |  |  |
| small (random weights) | 34.1M | llama.cpp Q8_0 | 45.7 MB | 588.1 | 29846.6 | 0.153 GB |
| small (random weights) | 34.1M | llama.cpp Q4_K_M | 28.7 MB | 740.0 | 31511.0 | 0.137 GB |
| small (random weights) | 34.1M | PyTorch CPU int8 |  | 110.12 |  |  |
| small (random weights) | 34.1M | PyTorch CPU fp32 |  | 166.82 |  |  |
| base (random weights) | 97.5M | llama.cpp Q8_0 | 117.6 MB | 213.4 | 10660.4 | 0.259 GB |
| base (random weights) | 97.5M | llama.cpp Q4_K_M | 69.2 MB | 291.4 | 10233.9 | 0.214 GB |
| base (random weights) | 97.5M | PyTorch CPU int8 |  | 50.72 |  |  |
| base (random weights) | 97.5M | PyTorch CPU fp32 |  | 66.6 |  |  |

## Quality gates (plan.md section 6) for the base model

- Speed, at least 20 tok/s int8: **213.4 tok/s** with llama.cpp Q8_0 (pass).
- Laptop RAM under 3 GB during generation: **0.259 GB** peak for llama.cpp (pass).
- Chapter under 5 min for 3000 words (~4050 tokens): **0.3 min** of pure generation (pass). Prompt prefill per scene adds a few seconds.
