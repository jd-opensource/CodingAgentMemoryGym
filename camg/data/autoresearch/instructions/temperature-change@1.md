# OpenMLE-fast task

Task ID: `temperature-change@1`

Native metric: `GlobalTempAnomalyMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2306 bytes)
- `data/sample_submission.csv` (359968 bytes); columns: ["id", "value"]
- `data/test.csv` (504778 bytes); columns: ["id", "country_code", "iso3", "months_code", "months", "year", "std_dev"]
- `data/train.csv` (7289148 bytes); columns: ["id", "country_code", "iso3", "months_code", "months", "year", "std_dev", "value"]

## Public description

Global Monthly Temperature Anomaly Forecasting (1961–2023)

Problem statement
- Predict monthly mean surface temperature anomaly (relative to 1951–1980) for each country and territory worldwide. Given historical country–month anomalies up to 2019, forecast the anomalies for 2020–2023 across all countries and months.

Data description
- train.csv: Panel time series of monthly anomalies for 1961–2019. Each row represents a country–month–year with columns:
  - id: Unique identifier combining country and month and year
  - country_code: FAO country code (numeric)
  - iso3: ISO3 country code
  - months_code: FAOSTAT month code (7001–7012)
  - months: Month name (January–December)
  - year: Calendar year (1961–2019)
  - std_dev: Baseline-method standard deviation (σ) of anomaly for the country–month
  - value: Target anomaly in °C
- test.csv: Same columns as train.csv except without the value column; spans 2020–2023. All ids correspond to rows in the hidden ground truth.
- sample_submission.csv: Example submission file with valid ids and randomly generated numeric predictions.

What you can use
- The panel structure enables ML models to learn global and country-specific trends, seasonality, and cross-country signals. Feature engineering ideas include lagged values, moving averages, month indicators, country fixed effects, trend features, and the provided std_dev.

Evaluation
- Weighted RMSE over all test rows. For each prediction, a weight is defined by the baseline-method standard deviation (σ) for the corresponding country–month:
  - weight = 1 / (σ^2).
  - Score = sqrt( sum_i weight_i * (pred_i − true_i)^2 / sum_i weight_i ).
- Rationale: Country–months differ in climatological variability; weighting by σ fairly balances influence across series and emphasizes accuracy where anomalies are more stable.

Files to submit
- A CSV with columns: id, value. The id must match those in test.csv. The value must be a finite numeric prediction in °C.

Notes
- Aggregated regions and roll-ups (e.g., Africa, Americas, World) are excluded; the task focuses on countries and territories.
- Only monthly frequency is included to keep the panel consistent and comparable.
- All ids in test.csv appear in the historical panel for the same country and month.
