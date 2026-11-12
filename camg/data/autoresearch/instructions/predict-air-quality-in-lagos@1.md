# OpenMLE-fast task

Task ID: `predict-air-quality-in-lagos@1`

Native metric: `LagosAirQualityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2422 bytes)
- `data/sample_submission.csv` (875 bytes); columns: ["date", "pm25"]
- `data/test.csv` (335 bytes); columns: ["date"]
- `data/train.csv` (8996 bytes); columns: ["date", "pm25"]

## Public description

Predict Lagos Daily PM2.5 (µg/m³) from historical observations.

Problem statement
Participants must forecast daily PM2.5 concentrations for a held-out, chronologically later period in Lagos. You are given historical observations with dates. Use time-aware modeling to predict the PM2.5 value for each date listed in the test set.

Files
- train.csv: Historical data with columns:
  - date: ISO format YYYY-MM-DD (unique, sorted)
  - pm25: target value (numeric)
- test.csv: Future dates to predict with columns:
  - date: ISO format YYYY-MM-DD
- sample_submission.csv: Example submission file with columns:
  - date
  - pm25: placeholder numeric predictions

Target
- pm25: Daily average fine particulate matter concentration (PM2.5) in µg/m³.

Task details and guidance
- This is a univariate time-series regression/forecasting task. Respect temporal order; do not train on any data from or after the test period.
- The series has irregular sampling with missing calendar days. You may reindex to daily frequency and create lags/rolling statistics, but avoid leakage by using only information available up to each prediction date.
- Suggested features (optional): calendar features (month, day-of-week, day-of-year), lagged pm25 (1, 2, 7, 14, 28), rolling mean/std/max over 7–30 days, seasonal lags (e.g., 365 if reindexed), weekend/holiday flags derived only from the date.
- Typical modeling approaches include tree-based regressors with engineered features, state-space/ETS/ARIMA-type models, gradient boosting, or sequence models. Use time-aware validation (e.g., rolling-origin/expanding window) to mimic the leaderboard split.
- External data is not allowed. All features must be computed from the provided training data and/or the date field.

Evaluation
- Metric: Mean Absolute Error (MAE) on pm25.
  - MAE = mean(|y_true − y_pred|)
  - Lower is better.
  - Rationale: MAE is robust and directly interpretable in µg/m³, balancing everyday accuracy with sensitivity to harmful spikes.

Submission format
- CSV with two columns: date, pm25
- Must contain exactly the same dates as in test.csv, with no duplicates or missing entries.
- pm25 must be finite numeric values (no NaN/inf).

Notes
- The data include sharp peaks and very low values; model them carefully and consider robust features/losses.
- Ensure your pipeline is strictly time-aware to avoid leakage from the future into training features.
