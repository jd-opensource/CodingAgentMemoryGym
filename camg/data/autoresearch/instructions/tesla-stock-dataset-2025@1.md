# OpenMLE-fast task

Task ID: `tesla-stock-dataset-2025@1`

Native metric: `TeslaReturnQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2679 bytes)
- `data/sample_submission.csv` (48984 bytes); columns: ["Id", "q10", "q50", "q90"]
- `data/test.csv` (81601 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (388598 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "next_day_log_return"]

## Public description

Title: Probabilistic Next‑Day TSLA Return Forecasting (Quantile Regression)

Problem
- Predict the conditional distribution of Tesla’s next-day adjusted close log return from daily OHLCV history.

Task
- For each row in test.csv (a trading day t), predict three quantiles of the next day’s adjusted close log return r_{t+1} = ln(AdjClose_{t+1} / AdjClose_t).
- Submit the 0.1, 0.5, and 0.9 quantiles for each Id in the test set.

Files provided
- train.csv: Daily OHLCV with the target next_day_log_return for model training.
- test.csv: Daily OHLCV for evaluation dates; no targets. Contains an Id column.
- sample_submission.csv: Example submission with valid quantile ordering.

Data schema
- Shared feature columns in train.csv and test.csv:
  - Date: Trading date (YYYY-MM-DD), strictly increasing within each file.
  - Open, High, Low, Close, Adj Close: Daily prices.
  - Volume: Daily traded volume.
- Additional columns:
  - test.csv: Id (unique integer identifier)
  - train.csv: next_day_log_return = ln(AdjClose_{t+1} / AdjClose_t)

Submission format
- CSV with columns: Id, q10, q50, q90.
- Quantile monotonicity must hold per row: q10 ≤ q50 ≤ q90.
- Ids must exactly match those in test.csv in the same order and with no duplicates or missing rows.

Evaluation metric
- Pinball (quantile) loss averaged over q ∈ {0.1, 0.5, 0.9} and all test rows.
  - For true return y and predicted quantile ŷ_q: L_q(y, ŷ_q) = max(q·(y−ŷ_q), (q−1)·(y−ŷ_q)).
  - Final score = mean of L_q across all rows and the three quantiles. Lower is better.

Train/test split
- Strict chronological split: approximately the last 20% of dates are used as test; the earlier ~80% are used as train.
- Data is ordered by Date without shuffling. All feature engineering must use only information available up to and including day t to forecast r_{t+1}.

Modeling guidance (optional)
- Any ML approach capable of probabilistic or quantile prediction is allowed (e.g., gradient boosting with quantile loss, linear models with pinball loss, quantile forests, sequence models).
- Useful features include lagged OHLCV values, moving averages and volatility, price ranges (High−Low, High−Close), momentum/RSI, ATR, volume changes, and calendar effects. Fit scalers/transforms only on the training period.

Rules
- No leakage: Use information from dates ≤ t only to predict r_{t+1} for date t.
- Submissions violating quantile ordering or Id alignment will be rejected.

Deliverables
- train.csv
- test.csv
- sample_submission.csv

Build well-calibrated probabilistic forecasts that handle non-stationarity, regime shifts, and volatility clustering in TSLA returns. Good luck!
