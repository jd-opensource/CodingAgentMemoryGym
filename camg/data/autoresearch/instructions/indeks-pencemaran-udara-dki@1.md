# OpenMLE-fast task

Task ID: `indeks-pencemaran-udara-dki@1`

Native metric: `JakartaAirQualityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2566 bytes)
- `data/sample_submission.csv` (1208 bytes); columns: ["id", "pm25_next"]
- `data/test.csv` (14750 bytes); columns: ["id", "pm10_lag1", "pm10_lag2", "pm10_lag3", "pm10_lag4", "pm10_lag5", "pm10_lag6", "pm10_lag7", "pm25_lag1", "pm25_lag2", "pm25_lag3", "pm25_lag4", "pm25_lag5", "pm25_lag6", "pm25_lag7", "so2_lag1", "so2_lag2", "so2_lag3", "so2_lag4", "so2_lag5", "so2_lag6", "so2_lag7", "co_lag1", "co_lag2", "co_lag3", "co_lag4", "co_lag5", "co_lag6", "co_lag7", "o3_lag1", "o3_lag2", "o3_lag3", "o3_lag4", "o3_lag5", "o3_lag6", "o3_lag7", "no2_lag1", "no2_lag2", "no2_lag3", "no2_lag4", "no2_lag5", "no2_lag6", "no2_lag7"]
- `data/train.csv` (60471 bytes); columns: ["id", "pm10_lag1", "pm10_lag2", "pm10_lag3", "pm10_lag4", "pm10_lag5", "pm10_lag6", "pm10_lag7", "pm25_lag1", "pm25_lag2", "pm25_lag3", "pm25_lag4", "pm25_lag5", "pm25_lag6", "pm25_lag7", "so2_lag1", "so2_lag2", "so2_lag3", "so2_lag4", "so2_lag5", "so2_lag6", "so2_lag7", "co_lag1", "co_lag2", "co_lag3", "co_lag4", "co_lag5", "co_lag6", "co_lag7", "o3_lag1", "o3_lag2", "o3_lag3", "o3_lag4", "o3_lag5", "o3_lag6", "o3_lag7", "no2_lag1", "no2_lag2", "no2_lag3", "no2_lag4", "no2_lag5", "no2_lag6", "no2_lag7", "pm25_next"]

## Public description

Title: Jakarta Air Quality: Next‑Day PM2.5 Forecasting (2021)

Background
- Jakarta’s daily air quality is tracked by pollutant-specific ISPU indices (PM10, PM2.5, SO2, CO, O3, NO2). Anticipating tomorrow’s PM2.5 index supports public advisories and mitigation.

Problem statement
- Given recent days of pollutant indices, predict the next day’s PM2.5 ISPU value.
- This is a time-series regression challenge that emphasizes leakage-free feature engineering and generalization to the future.

Data description
- You are provided with preprocessed tabular files with lagged features engineered from historical daily pollutant indices.
- Train file (train.csv):
  - id: the forecast date (YYYY-MM-DD) for which the target is defined.
  - Features: pollutant lag features of length 7 for each pollutant series (pm10_lag1..lag7, pm25_lag1..lag7, so2_lag1..lag7, co_lag1..lag7, o3_lag1..lag7, no2_lag1..lag7). Each lag k corresponds to the value k days before the forecast date.
  - Target: pm25_next — the PM2.5 ISPU value for the forecast date.
- Test file (test.csv):
  - id: the forecast date (YYYY-MM-DD) to predict.
  - Features: same set of lag features as in train.csv.
  - No target column is included.
- Sample submission (sample_submission.csv):
  - Columns: id, pm25_next. Contains randomly generated but valid numeric values as placeholders.

Notes
- Features are built only from historical days prior to the forecast date. Same-day derived indicators (e.g., max/critical/category) are excluded to avoid leakage and redundancy.
- Chronological splitting is applied: training covers the earlier period; testing covers the later hold-out period.

Evaluation
- Metric: Mean Absolute Error (MAE) on pm25_next over the test set.
- Definition: MAE = mean(|y_pred − y_true|) across all test rows.
- Rationale: MAE is robust to occasional spikes and directly reflects errors in ISPU units.

Rules and recommendations
- Use any ML/TS methods that respect temporal ordering (e.g., linear models with lag features, tree-based models, ARIMA/ETS with exogenous variables, simple RNNs). Do not leak future information into features.
- You may add additional features (e.g., calendar transforms from id) during modeling, but all features must be derived from information up to (and not including) the forecast date.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your task
- Fit a model on train.csv to predict pm25_next for each id in test.csv, and submit a CSV with columns: id, pm25_next. The leaderboard is ranked by MAE (lower is better).
