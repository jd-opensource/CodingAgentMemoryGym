# OpenMLE-fast task

Task ID: `rainfall-timeseries-data@1`

Native metric: `RainfallForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3099 bytes)
- `data/sample_submission.csv` (924 bytes); columns: ["row_id", "Precipitation"]
- `data/test.csv` (16697 bytes); columns: ["row_id", "Month", "month_sin", "month_cos", "Year", "t_index", "Precipitation_lag1", "Precipitation_lag10", "Precipitation_lag11", "Precipitation_lag12", "Precipitation_lag2", "Precipitation_lag3", "Precipitation_lag4", "Precipitation_lag5", "Precipitation_lag6", "Precipitation_lag7", "Precipitation_lag8", "Precipitation_lag9", "Relative_Humidity_lag1", "Relative_Humidity_lag10", "Relative_Humidity_lag11", "Relative_Humidity_lag12", "Relative_Humidity_lag2", "Relative_Humidity_lag3", "Relative_Humidity_lag4", "Relative_Humidity_lag5", "Relative_Humidity_lag6", "Relative_Humidity_lag7", "Relative_Humidity_lag8", "Relative_Humidity_lag9", "Specific_Humidity_lag1", "Specific_Humidity_lag10", "Specific_Humidity_lag11", "Specific_Humidity_lag12", "Specific_Humidity_lag2", "Specific_Humidity_lag3", "Specific_Humidity_lag4", "Specific_Humidity_lag5", "Specific_Humidity_lag6", "Specific_Humidity_lag7", "Specific_Humidity_lag8", "Specific_Humidity_lag9", "Temperature_lag1", "Temperature_lag10", "Temperature_lag11", "Temperature_lag12", "Temperature_lag2", "Temperature_lag3", "Temperature_lag4", "Temperature_lag5", "Temperature_lag6", "Temperature_lag7", "Temperature_lag8", "Temperature_lag9"]
- `data/train.csv` (63909 bytes); columns: ["Month", "month_sin", "month_cos", "Year", "t_index", "Precipitation_lag1", "Precipitation_lag10", "Precipitation_lag11", "Precipitation_lag12", "Precipitation_lag2", "Precipitation_lag3", "Precipitation_lag4", "Precipitation_lag5", "Precipitation_lag6", "Precipitation_lag7", "Precipitation_lag8", "Precipitation_lag9", "Relative_Humidity_lag1", "Relative_Humidity_lag10", "Relative_Humidity_lag11", "Relative_Humidity_lag12", "Relative_Humidity_lag2", "Relative_Humidity_lag3", "Relative_Humidity_lag4", "Relative_Humidity_lag5", "Relative_Humidity_lag6", "Relative_Humidity_lag7", "Relative_Humidity_lag8", "Relative_Humidity_lag9", "Specific_Humidity_lag1", "Specific_Humidity_lag10", "Specific_Humidity_lag11", "Specific_Humidity_lag12", "Specific_Humidity_lag2", "Specific_Humidity_lag3", "Specific_Humidity_lag4", "Specific_Humidity_lag5", "Specific_Humidity_lag6", "Specific_Humidity_lag7", "Specific_Humidity_lag8", "Specific_Humidity_lag9", "Temperature_lag1", "Temperature_lag10", "Temperature_lag11", "Temperature_lag12", "Temperature_lag2", "Temperature_lag3", "Temperature_lag4", "Temperature_lag5", "Temperature_lag6", "Temperature_lag7", "Temperature_lag8", "Temperature_lag9", "Precipitation"]

## Public description

Competition: Monsoon Rainfall Forecasting (Monthly, 1–12 month horizon)

Problem Statement
You are given a single-location monthly time series from Mumbai, India. Using only information available up to the previous month, predict the monthly precipitation total (in mm) for future months. The task is a univariate target regression with exogenous history: you may model seasonality and use lagged meteorological variables, but same-month meteorology must not be used to avoid future information leakage.

Files
- train.csv: Training set with engineered features and target.
- test.csv: Test set with engineered features (no target).
- sample_submission.csv: A valid-format sample with random but plausible predictions.

Data Description
Each row represents one calendar month. Columns include:
- row_id (test.csv and sample_submission.csv only): Integer ID linking test rows to predictions.
- Precipitation: Target (mm) in train.csv only; withheld in test.csv.
- Month, month_sin, month_cos, Year, t_index: Seasonal/time features.
- Lag features: For each of Precipitation, Specific Humidity, Relative Humidity, Temperature, the dataset provides 12 months of lagged values: e.g., Precipitation_lag1..lag12, Specific_Humidity_lag1..lag12, Relative_Humidity_lag1..lag12, Temperature_lag1..lag12.

Important: The public features deliberately exclude same-month meteorology to ensure a leakage-free forecasting setup. All predictive information about meteorology comes through lags of up to 12 months.

Train/Test Split
- Temporal split without shuffling to respect causality.
- Train: 2000-01 to 2016-12 (with the first 12 months dropped to ensure all lag features are available).
- Test: 2017-01 to 2020-12.

Target
- Precipitation (mm) per month.

Evaluation Metric
- Root Mean Squared Logarithmic Error (RMSLE) on Precipitation.
- Definition: RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2)).
- Rationale: Robust to zeros and heavy-tailed monsoon spikes; rewards accurate relative error across wet and dry months.

Rules and Guidance
- Use any modeling approach (classical, ML, or deep learning) that respects the no-leakage constraint.
- You may perform additional feature engineering, e.g., longer/shorter lags, rolling statistics, or holiday/seasonal encodings. Just ensure that features for month t are derived strictly from months < t.
- The provided train/test CSVs are leakage-safe and can be used directly. If you rebuild features from the raw monthly file, be cautious to avoid using same-month covariates for test-time predictions.

Submission Format
- CSV with columns: row_id, Precipitation.
- row_id must match the provided IDs in test.csv exactly (0..N-1 without gaps).
- Precipitation predictions must be numeric and non-negative.

Baseline Ideas
- Seasonal ARIMA/SARIMAX on log1p(Precipitation) with seasonal period 12.
- Gradient-boosted trees or random forests using the provided lag features and seasonal encodings.
- Sequence models (e.g., 1D CNNs, LSTMs, or Transformers) trained on the lagged feature windows.

Final Files
- train.csv
- test.csv
- sample_submission.csv
