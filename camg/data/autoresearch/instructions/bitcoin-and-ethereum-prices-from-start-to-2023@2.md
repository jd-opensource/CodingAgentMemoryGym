# OpenMLE-fast task

Task ID: `bitcoin-and-ethereum-prices-from-start-to-2023@2`

Native metric: `CryptoVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2899 bytes)
- `data/sample_submission.csv` (5299 bytes); columns: ["row_id", "target"]
- `data/test.csv` (12388 bytes); columns: ["row_id", "date", "asset", "open", "high", "low", "close", "adj_close", "volume", "market_cap"]
- `data/train.csv` (752842 bytes); columns: ["row_id", "date", "asset", "open", "high", "low", "close", "adj_close", "volume", "market_cap", "target"]

## Public description

Title: One-week-ahead realized volatility forecasting for BTC and ETH

Problem statement
Predict the 5-day-ahead realized volatility for each asset (BTC and ETH) using only past daily OHLCV data. For each anchor date t, the target is the standard deviation of the next five daily log-returns r_{t+1..t+5}. You are given a harmonized daily panel with both assets; train rows include the target, while test rows hide it.

Files provided
- train.csv: Training rows with features and the target.
- test.csv: Test rows with the same features and a row_id to join predictions.
- sample_submission.csv: Example submission file with the correct schema.

Data description
Each row corresponds to a single asset-date pair. Columns in train.csv and test.csv:
- row_id: Unique identifier for the row, formatted as ASSET_YYYY-MM-DD (e.g., BTC_2024-11-05)
- date: UTC calendar date (YYYY-MM-DD)
- asset: One of {BTC, ETH}
- open, high, low, close: Daily OHLC prices (USD)
- adj_close: Adjusted close if available; otherwise equals close
- volume: Daily traded volume (unit is source-dependent but harmonized to numeric)
- market_cap: Market capitalization when available, else blank

Target (train.csv only):
- target: Natural logarithm of RV5, where RV5 is the population standard deviation (ddof=0) of the next five daily log-returns r_{t+1},...,r_{t+5}. A small epsilon is added internally when computing the log to avoid log(0).

Rules and expectations
- Use only non-leaky information: features must be functions of data available up to and including the anchor date t.
- You are encouraged to engineer features such as lagged returns, rolling volatility and ranges, momentum indicators, cross-asset lags, and calendar effects.
- Any ML approach is allowed (e.g., linear models, tree-based models, sequence models, volatility models) as long as it respects the non-leakage constraint.

Evaluation metric
Submissions are evaluated by mean absolute error (MAE) on log-volatility:
MAE = mean(|y_true - y_pred|), where y represents ln(RV5).
The final score averages across all assets and dates in the test set.

Submission format
- A CSV file with exactly two columns and no index:
  - row_id: Must exactly match the row_id values in test.csv
  - target: Your prediction for ln(RV5) for the corresponding row_id
- The number of rows must equal the number of rows in test.csv. No extra or missing rows are allowed.

Train/test time split
- Train covers the early history up to 2024-10-23 (inclusive).
- Test covers anchor dates from 2024-10-24 through 2025-01-08 (inclusive).
- All assets appear in both train and test ranges.

Tips
- Work in log-returns and log-volatility to stabilize variance and handle scale differences across assets.
- Cross-asset spillovers matter: lagged BTC signals can help ETH and vice versa.
- Expect regime changes and heavy tails; robust models and features tend to perform better.
