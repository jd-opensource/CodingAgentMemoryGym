# OpenMLE-fast task

Task ID: `climate-change-indicators@1`

Native metric: `ClimateAnomalyForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1236 bytes)
- `data/sample_submission.csv` (86528 bytes); columns: ["Country", "ISO3", "Year", "Anomaly"]
- `data/test.csv` (46358 bytes); columns: ["Country", "ISO3", "Year"]
- `data/train.csv` (290066 bytes); columns: ["Country", "ISO3", "Year", "Anomaly"]

## Public description

Title: Global Panel Forecasting of Country-Level Surface Temperature Anomalies (2013–2022)

Problem Statement
Build a model that, for each country, forecasts annual surface temperature anomaly for 2013–2022 using only historical anomalies up to and including 2012.

Data Description
Participants are provided time-series training data and an identifier-only test horizon:
- train.csv: Long-format panel time series containing rows for years 1961–2012 across all countries. Columns: Country, ISO3, Year, Anomaly.
- test.csv: Identifier rows for the forecast horizon (2013–2022) for countries with complete targets. Columns: Country, ISO3, Year.
- sample_submission.csv: A properly formatted example submission containing all test identifiers and a placeholder Anomaly column with plausible numeric values.

Evaluation
Submissions must predict an Anomaly value for every row in test.csv. The leaderboard metric is macro-averaged RMSE computed per country (ISO3) across its test years and then averaged across countries.

Submission Format
- CSV with columns: Country, ISO3, Year, Anomaly.
- Every (ISO3, Year) pair in test.csv must appear exactly once. No extra or missing rows.
- The Anomaly column must be finite numeric values.
