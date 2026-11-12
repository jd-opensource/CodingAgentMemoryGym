# OpenMLE-fast task

Task ID: `gold-price-1979-present@1`

Native metric: `GoldSmapeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (833 bytes)
- `data/sample_submission.csv` (2033422 bytes); columns: ["Date", "Currency", "Target"]
- `data/test.csv` (13484313 bytes); columns: ["Date", "Currency", "lag_1", "lag_2", "lag_3", "lag_4", "lag_5", "lag_6", "lag_7", "lag_8", "lag_9", "lag_10", "lag_11", "lag_12", "lag_13", "lag_14", "lag_15", "lag_16", "lag_17", "lag_18", "lag_19", "lag_20", "lag_21", "lag_22", "lag_23", "lag_24", "lag_25", "lag_26", "lag_27", "lag_28", "lag_29", "lag_30", "dow", "dom", "moy", "doy"]
- `data/train.csv` (3250294 bytes); columns: ["Date", "Currency", "Price"]
- `data/train_monthly.csv` (149564 bytes); columns: ["Date", "Currency", "Price"]
- `data/train_quarterly.csv` (20 bytes); columns: ["Date", "Currency", "Price"]

## Public description

Global Gold Across Currencies – Daily One‑Step Forecasting (1979–2022)

Files in this folder:
- train.csv: Long‑format daily panel [Date, Currency, Price] up to 2009‑12‑31.
- train_monthly.csv: Monthly panel [Date, Currency, Price] (train period only).
- train_quarterly.csv: Quarterly panel [Date, Currency, Price] (train period only).
- test.csv: Targets to predict with lag features and calendar columns.
- sample_submission.csv: Example submission with columns [Date, Currency, Target].
- description.txt: This file.

Submission:
- Provide a CSV named anything with header [Date, Currency, Target].
- The [Date, Currency] rows must exactly match test.csv and be in the same order.

Evaluation (for organizers):
- Symmetric Mean Absolute Percentage Error (SMAPE) macro‑averaged across currencies.
- Lower is better.
