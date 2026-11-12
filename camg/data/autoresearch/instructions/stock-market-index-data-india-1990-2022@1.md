# OpenMLE-fast task

Task ID: `stock-market-index-data-india-1990-2022@1`

Native metric: `StockReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2340 bytes)
- `data/sample_submission.csv` (302312 bytes); columns: ["row_id", "next_return_pct"]
- `data/test.csv` (997328 bytes); columns: ["row_id", "index_id", "Date", "open", "high", "low", "close", "pe", "pb", "div_yield", "vix_close", "gold_inr"]
- `data/train.csv` (7882303 bytes); columns: ["row_id", "index_id", "Date", "open", "high", "low", "close", "pe", "pb", "div_yield", "vix_close", "gold_inr", "next_return_pct"]

## Public description

Competition: Multi-Index Next-Day Returns Forecasting for Indian NSE Indices (1990–2022)

Problem statement
Participants must forecast the next trading day’s close-to-close percentage return for multiple Indian stock market indices. For each index and date in the test set, predict the next day’s return using only information available up to the current day. Predictions are evaluated jointly across all indices.

Data provided (under public/)
- public/train.csv
  - Columns: row_id, index_id, Date, open, high, low, close, pe, pb, div_yield, vix_close, gold_inr, next_return_pct
  - Date is the trading day (YYYY-MM-DD). The target next_return_pct is the close-to-close return for the following trading day, in percent.
- public/test.csv
  - Columns: row_id, index_id, Date, open, high, low, close, pe, pb, div_yield, vix_close, gold_inr
  - Date is the trading day (YYYY-MM-DD). Each row_id corresponds to a required prediction for the next day’s return.
- public/sample_submission.csv
  - Columns: row_id, next_return_pct
  - row_id directly maps to rows in test.csv.

Notes on features and construction
- The dataset spans decades of daily OHLC for multiple NSE indices and includes index valuation ratios (P/E, P/B, Dividend Yield), plus daily VIX and INR-denominated gold prices as exogenous signals.
- Features are aligned by trading day per index; valuation, VIX, and gold series are joined using backward (as-of) merging to prevent lookahead bias. Missing values have been forward/backward filled within index and then filled with global median if necessary.
- The target next_return_pct equals 100 * (Close_{t+1} / Close_{t} − 1). There is no label in test.csv.
- row_id is a unique identifier for each prediction instance; it must be preserved in submissions.

Evaluation metric
- Metric: RMSE of next_return_pct over all test rows.
- For each test row: error = prediction − truth; score = sqrt(mean(error^2)). Lower is better.

Submission format
- A single CSV file with columns: row_id, next_return_pct.
- The row_ids must match those provided in test.csv; extra or missing rows will lead to an invalid submission.
- next_return_pct must be numeric and finite values expressed in percent.

Deliverables
- Submit predictions for all row_id entries in the test set as a CSV following the required two-column format.
