# OpenMLE-fast task

Task ID: `simulated-sales-data-with-timeseries-features@2`

Native metric: `SalesQuantilePinballMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2894 bytes)
- `data/sample_submission.csv` (1998 bytes); columns: ["Date", "q0.10", "q0.50", "q0.90"]
- `data/test.csv` (335 bytes); columns: ["Date"]
- `data/train.csv` (9802 bytes); columns: ["Date", "Sales"]

## Public description

Weekend-Seasonality Sales Forecast (Probabilistic Quantiles)

Problem statement
Participants must forecast calibrated uncertainty for daily sales over the final 30 days of the dataset by predicting multiple quantiles of the sales distribution for each target date. You will submit three quantiles per day: 0.10, 0.50, and 0.90.

Data description
- train.csv: Historical daily records with two columns: Date, Sales. This file contains all days up to and including 2022-08-31.
- test.csv: Target dates (30 rows; 2022-09-01 to 2022-09-30) with a single column: Date. No labels are provided here.
- sample_submission.csv: Example submission with columns: Date, q0.10, q0.50, q0.90.

Raw data characteristics
- Single-store daily sales with a clear weekly seasonality (weekend uplift) and a slow upward trend.
- Clean, continuous daily frequency; no missing dates.

What you need to do
- Parse dates, sort chronologically, and build features using past data only. Example ideas:
  - Time features: day of week/weekend, month, seasonal indicators.
  - Lag features: 1, 2, 7, 14, 21, 28; rolling means/medians/stds over 7/14/28 days; seasonal differences (e.g., y[t]-y[t-7]).
  - Point forecasters combined with residual modeling, quantile regression (GBDTs, QRNNs), distributional regression (e.g., NGBoost), bootstrapping, or Bayesian approaches.
- Use rolling-origin (time-based) validation on the training period to tune models and assess calibration and sharpness.

Submission format
- CSV with columns: Date, q0.10, q0.50, q0.90.
- Dates must exactly match those in test.csv and appear once each.
- Quantiles must be numeric, finite, and non-decreasing per row: q0.10 <= q0.50 <= q0.90.

Evaluation
- Metric: Mean Pinball Loss averaged across all target dates and requested quantiles τ ∈ {0.10, 0.50, 0.90}.
- For a single observation y with predicted quantile q_τ, the pinball loss is:
  L_τ(y, q) = max(τ · (y − q), (τ − 1) · (y − q)).
- The competition score is the mean of L_τ over all days and all three quantiles. Lower is better.

Files provided to participants
- train.csv
- test.csv
- sample_submission.csv

Rules and recommendations
- Do not use future information beyond each forecasting date when constructing features.
- No external data is required. If you use any, ensure it would have been available historically.
- Ensure numeric stability in your pipeline (no NaN/Inf in predictions).
- Keep quantiles coherent (non-crossing). Consider techniques such as constrained regression, monotonic post-processing, or joint distributional models.

Notes
- The original export contained a leftmost row-index column; it has been removed in the provided train/test files to avoid leakage or spurious correlations.
- This is a single time series; careful regularization and cross-validation are recommended to avoid overfitting while capturing weekly seasonality and trend.
