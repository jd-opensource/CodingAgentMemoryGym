# OpenMLE-fast task

Task ID: `top-10-cryptocurrencies-historical-dataset@1`

Native metric: `CryptoReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2450 bytes)
- `data/sample_submission.csv` (284476 bytes); columns: ["row_id", "target"]
- `data/test.csv` (736917 bytes); columns: ["row_id", "coin_id", "Date", "Open", "High", "Low", "Close", "Volume"]
- `data/train.csv` (13993165 bytes); columns: ["coin_id", "Date", "Open", "High", "Low", "Close", "Volume", "target"]

## Public description

Title: Multi-Asset Crypto 1-Day Ahead Log-Return Forecasting

Problem statement
- Given daily OHLCV history up to day t for each cryptocurrency, predict the next day’s Close log return for that asset. Models should generalize across coins and regimes.

Data description
- Provided files: train.csv, test.csv, sample_submission.csv.
- Each row represents one coin on one date, with OHLCV features from day t.
- Columns in train.csv and test.csv:
  - coin_id: Obfuscated identifier for the cryptocurrency (one coin per identifier).
  - Date: ISO date string for the observation (YYYY-MM-DD).
  - Open, High, Low, Close, Volume: Daily OHLCV features for day t.
- train.csv includes an additional column:
  - target: next-day log return y = ln(Close_{t+1} / Close_{t}) using the natural logarithm.
- test.csv has the same feature columns but does not include the target.

Submission format
- Submit a CSV with exactly two columns in this order:
  - row_id: Identifier corresponding to each row in test.csv.
  - target: Your predicted next-day log return for that row (numeric, finite).
- A sample_submission.csv is provided to illustrate the required format.

Evaluation metric
- Macro-averaged mean absolute error (MAE) on log returns across coins.
  - For each coin c, compute MAE_c = mean over that coin’s test rows of |prediction − target|.
  - Final score = average of MAE_c across all coins present in the test set.
- Rationale:
  - Log returns are scale-invariant, enabling fair comparison across assets with different price levels.
  - Macro-averaging ensures each asset contributes equally, avoiding dominance by sample count or volatility.
  - MAE is robust to outliers common in crypto markets.

Train/test split
- Chronological split per coin:
  - Train contains all labeled rows up to each coin’s test window.
  - Test contains the last 60 labeled rows per coin (targets withheld).
- All coins in test also appear in train.

Notes and recommendations
- coin_id is obfuscated to prevent leakage from asset names; do not attempt to infer labels from names.
- Feature engineering is encouraged (e.g., returns, ranges, moving averages, volatility estimates, volume patterns, candlestick signals).
- Handle non-stationarity and regime shifts carefully; robust preprocessing and modeling (e.g., normalization per coin, time-aware features) can help.
- External data is not required; solutions should be based on the provided OHLCV fields.
