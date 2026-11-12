# OpenMLE-fast task

Task ID: `mumbai-rainfall-data@1`

Native metric: `MumbaiRainfallQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2540 bytes)
- `data/sample_submission.csv` (4572 bytes); columns: ["row_id", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (2088 bytes); columns: ["row_id", "Year", "Month"]
- `data/train.csv` (34714 bytes); columns: ["row_id", "Year", "Month", "Rainfall"]

## Public description

Title: Mumbai Monsoon Quantile Forecasting

Problem statement
You are given more than a century of monthly rainfall observations for Mumbai. The task is to forecast the conditional distribution of monthly rainfall for held‑out future years by providing three quantiles per (Year, Month): q0.1, q0.5, q0.9. This is a probabilistic multi‑horizon time‑series forecasting problem with strong seasonality and heavy tails.

Files provided
- train.csv: Long-format historical data with columns [row_id, Year, Month, Rainfall]. Use these to train your models.
- test.csv: Target rows to predict with columns [row_id, Year, Month]. You must predict three quantiles for each row.
- sample_submission.csv: Example submission with the correct format and randomly generated but valid values.

Submission format
- A single CSV with columns: [row_id, q0.1, q0.5, q0.9].
- row_id matches the identifiers in test.csv (one per Year–Month), and must appear exactly once. No extra or missing rows are allowed.
- Predictions must be non‑negative in millimeters (mm). During evaluation, predictions will be clipped to [0, ∞) and coerced to be non‑decreasing across quantiles via cumulative maximum; however, you should aim to produce valid, monotone quantiles directly.

Evaluation metric
- Pinball loss averaged uniformly across all test rows and quantiles q ∈ {0.1, 0.5, 0.9}.
- For a true value y and a submitted quantile ŷ_q, the per‑row loss is: L_q(y, ŷ_q) = max(q·(y − ŷ_q), (q−1)·(y − ŷ_q)).
- The leaderboard score is the mean of L_q over all rows and the three quantiles. Lower is better.

Modeling guidance
- Reshape train.csv into a panel with each Year–Month as a row. Useful features often include: month indicators, lagged rainfall for the same calendar month (e.g., 1–5 year lags), rolling means/medians, and seasonal aggregates (e.g., monsoon total Jun–Sep in prior years). External covariates are not provided; models must rely on the historical series.
- Consider transformations (e.g., log1p) internally, but predictions must be in mm and non‑negative.
- Strictly treat this as a forecasting task: do not leak information from the test years into training or feature engineering windows.

Final data files
- train.csv
- test.csv
- sample_submission.csv

Notes
- The original dataset contains a "Total" column which is the yearly sum and will not appear in the competition files to avoid trivial leakage.
- The time split used to build train/test ensures that all calendar months appear in both sets.
