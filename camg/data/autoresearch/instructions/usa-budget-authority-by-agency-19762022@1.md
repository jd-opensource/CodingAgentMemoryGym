# OpenMLE-fast task

Task ID: `usa-budget-authority-by-agency-19762022@1`

Native metric: `BudgetAuthorityForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (515 bytes)
- `data/sample_submission.csv` (3988 bytes); columns: ["series_id", "year", "value"]
- `data/test.csv` (1415 bytes); columns: ["series_id", "year"]
- `data/train.csv` (15860 bytes); columns: ["series_id", "year", "value"]

## Public description

Competition: Multi-Agency Budget Forecasting (1976–2016)

Objective
Predict annual budget authority values for multiple anonymized federal agencies.

Files
- train.csv: Historical data (1976–2011). Columns: series_id, year, value.
- test.csv: Forecast keys (2012–2016). Columns: series_id, year.
- sample_submission.csv: Example submission with valid schema. Columns: series_id, year, value.

Submission format
Provide predictions for every row in test.csv with the same keys and a non-negative value column.
