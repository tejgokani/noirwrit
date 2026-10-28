# Online training

The real `base` model (98M parameters) trains on a free Kaggle GPU. The Mac only runs the `tiny` smoke test.

## What you do (three steps, once)

1. Sign in at kaggle.com, verify your phone number (Kaggle requires it for GPUs), then open **Settings, API, Create New Token**. This downloads `kaggle.json`.
2. Run `mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json`
3. Run `make train-online`

Everything else is automatic. Cost: $0.

## What happens

`make train-online` runs `tools/online/kaggle_train.py`, which:

1. Uploads the code, the tokenizer and the packed shards as a private Kaggle dataset, `noirwrit-data` (public domain text only).
2. Pushes a private GPU kernel, `noirwrit-train-a`. On Kaggle it:
   - measures real tokens per second for two minutes on whatever GPU Kaggle assigned (T4 or P100),
   - logs the plan: FLOPs ~ 6 x params x tokens, hours, and dollars ($0 on Kaggle),
   - picks `base` if at least one epoch fits the time cap, otherwise `small`, and up to 4 epochs,
   - trains in three stages (general fiction, crime and detective, then the noir set at a lower learning rate with early stopping), with fp16 on a T4, `torch.compile`, fused AdamW and SDPA attention,
   - checkpoints every 30 minutes.
3. Polls every 5 minutes. Kaggle stops a GPU session at 12 hours. If training is not finished by then, the launcher pushes `noirwrit-train-b` with the first session's output attached, and it resumes from `latest.pt`. It alternates until the run finishes.
4. Downloads `best.pt` and `latest.pt` to `artifacts/base/` (or `artifacts/small/`), then exports GGUF Q8_0 and Q4_K_M.

Check on it any time with `python tools/online/kaggle_train.py --status`, or watch `logs/online.log`.

The estimate with the current corpus is in `docs/TRAINING_PLAN.txt` (regenerate it with `python -m noirwrit.train.plan_run --gpu t4`).

Kaggle's free quota is about 30 GPU hours a week. Check the current quota at kaggle.com before starting, since it changes.

## Optional: checkpoints on the Hugging Face Hub

Kaggle keeps each session's output, so the Hub is not required. To also push a checkpoint to the Hub every 30 minutes, add two secrets in the Kaggle kernel's settings (Add-ons, Secrets): `HF_TOKEN` (a write token) and `HF_REPO` (for example `tejgokani/noirwrit-base`). Secrets can only be added in Kaggle's web UI, not through the API.

## Fallback: RunPod (paid, hard cap $8)

Only if Kaggle cannot finish the run. Put these in `.env` (never committed):

```
RUNPOD_API_KEY=...
HF_TOKEN=...          # a Hugging Face write token
HF_REPO=tejgokani/noirwrit-train
```

Then run `python tools/online/runpod_train.py --budget-usd 8`. It uploads the bundle to a private Hub repo, starts one RTX 4090 pod (it refuses pods above $0.60/hour), runs a two-minute probe and trims the plan to fit the budget, trains, uploads the checkpoints, and stops the pod. The launcher also polls the pod and deletes it when the bill reaches the cap, so a paid GPU is never left idle.

This path is written but has not been run, since it needs a paid account. Rule from the plan: never debug on a paid GPU. Prove changes on the Mac `tiny` run first.

## After training

```
make bench          # docs/BENCH.md with the trained model
make samples        # five sample chapters in docs/samples/
```
