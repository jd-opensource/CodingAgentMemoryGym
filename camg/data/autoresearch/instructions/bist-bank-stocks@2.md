# OpenMLE-fast task

Task ID: `bist-bank-stocks@2`

Native metric: `BistBankStocksMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3026 bytes)
- `data/sample_submission.csv` (67497 bytes); columns: ["row_id", "log_range_next_day"]
- `data/test.csv` (124053 bytes); columns: ["date", "stock_name", "open", "high", "low", "close", "volume", "daily_return", "adj_close", "row_id"]
- `data/train.csv` (884628 bytes); columns: ["date", "stock_name", "open", "high", "low", "close", "volume", "daily_return", "adj_close", "log_range_next_day"]

## Public description

BIST Bank Stocks: Next‑Day Intraday Range Forecasting

Problem statement
Given daily OHLCV data for 9 Turkish banking stocks, predict the next trading day’s intraday log‑range for each stock/date. For a record at day t, the target is log(high_{t+1} / low_{t+1}) computed from the next trading day (t+1) of the same stock. This target is a scale‑invariant proxy for realized volatility and is widely used in risk management and short‑horizon trading.

Public files
- train.csv: Features observed at day t and the target log_range_next_day computed from day t+1. Columns:
  - date (YYYY‑MM‑DD)
  - stock_name (categorical: 9 bank tickers as names)
  - open, high, low, close (floats)
  - volume (float)
  - daily_return (float; as provided in the source data)
  - adj_close (float)
  - log_range_next_day (float target) = ln(high_{t+1} / low_{t+1}). Non‑negative.
- test.csv: Same feature columns as train.csv but without the target, plus a unique row_id column that identifies each required prediction. These rows correspond to day t values strictly after the training period; all of them have a valid next trading day (t+1) for evaluation.
- sample_submission.csv: A template file with the columns required for submission and randomized yet valid target values.

Train/test split (already applied in provided CSVs)
- Time‑based split aligned with realistic deployment.
- Training rows use features from dates up to 2024‑12‑31 where the next trading day exists on or before 2024‑12‑31.
- Test rows use features from dates on or after 2025‑01‑02 where the next trading day exists.
- The very last date per stock (which lacks a next trading day) is never included.

Target definition (precise)
For each stock and day t, the target is:
  log_range_next_day = ln(high_{t+1} / low_{t+1})
where high_{t+1} and low_{t+1} are the high and low of the next available trading day for the same stock. This quantity is always >= 0.

Submission format
- File must contain exactly these columns, in any order:
  - row_id
  - log_range_next_day
- Each row_id in test.csv must appear exactly once in the submission. Do not add or remove rows.

Evaluation
- Primary metric: Mean Absolute Error (MAE) between your predictions and the ground truth log_range_next_day over all test rows.
- Ties are broken by smaller MAE to higher precision.

Modeling notes and leakage control
- Use only information available at day t to predict day t+1 (as the provided features do). You may engineer additional features from the provided columns (e.g., log(high/low), absolute daily_return, rolling statistics, candlesticks, volume/turnover metrics, cross‑sectional aggregates across the 9 stocks), but ensure they are computed without using day t+1 or later.
- The stock_name and date columns are included to enable time‑series processing and cross‑sectional features; they can be used as features (e.g., via encoding) or for grouping/sorting.

Deliverables (public directory)
- train.csv
- test.csv
- sample_submission.csv
