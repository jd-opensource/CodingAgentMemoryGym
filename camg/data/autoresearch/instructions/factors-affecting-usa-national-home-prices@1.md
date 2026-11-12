# OpenMLE-fast task

Task ID: `factors-affecting-usa-national-home-prices@1`

Native metric: `HomePriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (537 bytes)
- `data/sample_submission.csv` (1379 bytes); columns: ["row_id", "target"]
- `data/test.csv` (4140 bytes); columns: ["row_id", "date", "mortgage_rate", "cpi", "unemployment", "fed_funds", "gdp", "population_growth"]
- `data/train.csv` (26521 bytes); columns: ["row_id", "date", "mortgage_rate", "cpi", "unemployment", "fed_funds", "gdp", "population_growth", "target"]

## Public description

# Macro-Driven U.S. Home Price Forecasting (3-Month Ahead)

Files in this folder (public/):
- train.csv: Training data with row_id, date, features, and target.
- test.csv: Test data with row_id, date, and features only.
- sample_submission.csv: Example submission file with columns row_id and target (positive values).

Submission format:
- CSV with columns: row_id, target.
- Provide exactly one row per row_id present in test.csv. Values must be strictly positive.

Evaluation:
- Root Mean Squared Error on logarithms of the HPI level.
