# OpenMLE-fast task

Task ID: `yulu-bike-sharing-data@1`

Native metric: `YuluBikeSharingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2951 bytes)
- `data/sample_submission.csv` (24853 bytes); columns: ["id", "count"]
- `data/test.csv` (121428 bytes); columns: ["id", "datetime", "season", "holiday", "workingday", "weather", "temp", "atemp", "humidity", "windspeed"]
- `data/train.csv` (509879 bytes); columns: ["id", "datetime", "season", "holiday", "workingday", "weather", "temp", "atemp", "humidity", "windspeed", "count"]

## Public description

Yulu Bike Sharing Demand Forecasting

Problem statement
Participants are challenged to predict the hourly number of bike rentals (count) for a shared micro‑mobility service using only information available at prediction time: datetime, calendar indicators, and weather‑related covariates. The task is a time-aware regression problem that mimics real forecasting: you must generalize from past hours to unseen future hours.

Data description
Final data files provided:
- train.csv: training rows with features and the target column count.
- test.csv: test rows with features only (no labels).
- sample_submission.csv: a valid-format example submission with random placeholder predictions.

Columns
- id: unique row identifier to align predictions with test rows.
- datetime: timestamp at hourly frequency (UTC-naive). You may parse/expand into rich calendar features (hour, weekday, month, year, week-of-year, day-of-year, weekend, holidays, etc.).
- season: categorical season indicator (1–4).
- holiday: binary indicator for public holiday.
- workingday: binary indicator for working day vs weekend/holiday.
- weather: categorical weather situation (1–4).
- temp: normalized temperature in Celsius.
- atemp: normalized “feels like” temperature in Celsius.
- humidity: relative humidity (0–100).
- windspeed: wind speed.
- count (train only): target variable, non‑negative integer representing hourly rentals.

Important notes
- Leakage prevention: casual and registered columns from the source are removed because count = casual + registered, and they are unknown at prediction time.
- The split is strictly chronological: the earlier 80% of hours are in train, and the latest 20% are in test. Do not use any information from the test period to engineer target or leakage‑prone features.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on count.
  - For predictions y_pred and ground truth y_true, RMSLE = sqrt(mean((log1p(max(y_true, 0)) − log1p(max(y_pred, 0)))^2)).
  - This metric emphasizes relative accuracy, is robust to right‑skew, and handles zero counts via log1p.

Submission format
- A single CSV with the following columns and no index column:
  - id: must match the ids in test.csv exactly.
  - count: your predicted non‑negative rental count for each id. Any negative predictions will be clipped to 0 for scoring.

Modeling guidance
- Recommended feature engineering includes extracting hour-of-day, day-of-week, month, year, holiday/weekend flags, and seasonality features from datetime.
- Consider treating season and weather as categorical variables; temperature, humidity, and windspeed as numeric.
- Tree‑based ensembles, gradient boosting, and regularized linear models are strong baselines; add interactions and non‑linearities to capture complex calendar × weather effects.

Ethical use and scope
- Use only the provided data. External data is not permitted for this competition.
