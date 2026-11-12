# OpenMLE-fast task

Task ID: `store-data-analysis-using-ms-excel@2`

Native metric: `VrindaStoreForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3248 bytes)
- `data/sample_submission.csv` (26992 bytes); columns: ["series_id", "date", "orders"]
- `data/series_map.json` (20730 bytes)
- `data/test.csv` (35264 bytes); columns: ["series_id", "date", "channel", "category", "state"]
- `data/train.csv` (185240 bytes); columns: ["series_id", "date", "channel", "category", "state", "orders"]

## Public description

Title: Vrinda Store Daily Demand Forecasting (Channel × Category × State)

Problem statement
Predict daily order counts for each time series defined by the combination of Channel, Category, and ship-state. You are given historical daily aggregates (train.csv) and a set of future dates to forecast (test.csv). For every (series_id, date) pair in test.csv, forecast the number of orders (non-negative real values). The provided split uses a strict time-based cutoff: train contains the earlier dates; test contains the final 6 unique dates for all retained series.

Data description
- train.csv
  - series_id: Stable identifier for a series (Channel × Category × State)
  - date: Date in YYYY-MM-DD
  - channel: Sales channel
  - category: Product category
  - state: Shipping state (India)
  - orders: Target; number of unique orders for that series on that date (integer ≥ 0)
- test.csv
  - series_id, date, channel, category, state (same meaning as in train), without the target column
- sample_submission.csv
  - Example submission with the required columns: series_id, date, orders
  - Contains random but valid predictions to illustrate the expected format

How the data were prepared
- Order-line rows were aggregated by date and by (Channel, Category, ship-state) to compute:
  - orders = number of unique Order IDs (target)
  - Auxiliary counts (not used for evaluation): lines and revenue
- Only series with sufficient activity were retained to ensure meaningful training signal (≥ 28 distinct dates).
- A global time split is applied: the earliest dates form training; the last 6 dates form testing. All retained series appear in both train and test, and test covers the same 6 dates for every series. Missing observations in the raw log are treated as zero orders during aggregation.

Submission format
- CSV file with exactly the columns: series_id, date, orders
- Include one row for each (series_id, date) pair in test.csv
- orders must be finite numbers; non-negative values are required. Predictions need not be integers.

Evaluation
- Metric: sMAPE (symmetric mean absolute percentage error), averaged over all rows.
  - For true value y and prediction p: if y = 0 and p = 0 then sMAPE = 0; otherwise sMAPE = 2·|p − y| / (|y| + |p|).
  - The final score is the mean sMAPE across all test rows. Lower is better.
- Rationale: sMAPE is scale-free and symmetric, making it fair across heterogeneous series with different volumes.

Modeling notes and recommendations
- This is a multi-series time series forecasting task with short histories and intermittent demand.
- Useful features include calendar signals (day-of-week, week-of-month, month), lagged orders (e.g., 1, 7), and rolling statistics computed strictly from training data to avoid leakage.
- Global models that share information across series tend to perform well (e.g., gradient boosting/GLMs on lag features, temporal CNN/RNN/Transformer, ETS/Prophet-like baselines). Always ensure no forward-looking features are used.
- Determinism is encouraged (seed your pipelines) for reproducible validation.

Files provided
- train.csv: Training data with targets
- test.csv: Test data without targets
- sample_submission.csv: Template and example of valid predictions
