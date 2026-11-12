# OpenMLE-fast task

Task ID: `bitcoin-and-ethereum-prices-from-start-to-2023@1`

Native metric: `CryptoNextDayCloseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3229 bytes)
- `data/sample_submission.csv` (4177 bytes); columns: ["row_id", "target_next_close"]
- `data/test.csv` (12388 bytes); columns: ["row_id", "date", "asset", "open", "high", "low", "close", "adj_close", "volume", "market_cap"]
- `data/train.csv` (705090 bytes); columns: ["row_id", "date", "asset", "open", "high", "low", "close", "adj_close", "volume", "market_cap", "target_next_close"]

## Public description

Competition: Dual‑Crypto Next‑Day Close Forecasting (BTC + ETH)

Problem statement
- Given only the past daily OHLCV information for Bitcoin (BTC) and Ethereum (ETH), predict the next‑day Close price for each asset.
- You are provided with a unified panel dataset of daily candles for both assets. Train rows contain the candle for day t and the target value of the Close on day t+1 for the same asset. Test rows contain the candle for day t; you must predict the Close on day t+1.

Files
- train.csv: panel of BTC and ETH daily records with target_next_close provided.
- test.csv: panel of BTC and ETH daily records for which you must predict target_next_close.
- sample_submission.csv: shows the required submission format.

Columns (train/test)
- row_id: unique identifier of a (date, asset) row in test and train.
- date: UTC date (YYYY‑MM‑DD) of the candle (day t).
- asset: one of {BTC, ETH}.
- open, high, low, close: OHLC prices for day t (float).
- adj_close: Adjusted Close (equals Close for crypto; provided for consistency) (float).
- volume: trading volume for day t (float; may be 0 or missing on some days).
- market_cap: market capitalization for day t where available (float; may be missing).
- target_next_close: ONLY IN train.csv. The Close on the next calendar day (t+1) for the same asset (float).

Target to predict
- For every row in test.csv, predict target_next_close (the Close on day t+1 for the same asset).

Train/test split
- Train rows cover the earliest available history up to 2024‑10‑27 (inclusive as day t). Their target_next_close corresponds to 2024‑10‑28 or earlier.
- Test rows cover 2024‑10‑28 through 2025‑01‑12 (inclusive as day t). These rows require predicting the Close for 2024‑10‑29 through 2025‑01‑13 (inclusive).
- The train and test sets are strictly disjoint by row_id and by target date to avoid leakage.

Evaluation
- The competition metric is SMAPE (Symmetric Mean Absolute Percentage Error) on target_next_close, averaged over all assets and all test rows:
  SMAPE(y_true, y_pred) = mean( 2 * |y_pred − y_true| / (|y_true| + |y_pred|) ).
- SMAPE is scale‑free and treats BTC and ETH fairly despite different price levels. Predictions must be finite real numbers.

What you can use
- All columns in train.csv and test.csv.
- Any data processing, feature engineering, and modeling techniques, including cross‑asset features (e.g., BTC lags to predict ETH), rolling statistics, and sequence models. Ensure you avoid look‑ahead: only use information from dates strictly prior to the target date.

Submission format
- A CSV with the following columns and no header/column changes:
  - row_id
  - target_next_close
- row_id must exactly match the values provided in test.csv. One prediction per row_id. Values must be finite numbers.

Notes
- Prices and volumes come from multiple high‑quality public sources and were standardized into the canonical schema above. Missing market_cap values may occur; use them as you see fit (including creating missingness indicators).
- Dates are calendar days in UTC; not all calendar days are present for both assets in earlier years. Only rows with a known target_next_close are included in train.
