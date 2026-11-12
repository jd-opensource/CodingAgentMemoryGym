# OpenMLE-fast task

Task ID: `stock-prices-of-the-10-largest-fast-food-companies@1`

Native metric: `StockReturnPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3324 bytes)
- `data/sample_submission.csv` (66570 bytes); columns: ["row_id", "Target"]
- `data/test.csv` (239752 bytes); columns: ["row_id", "Ticker", "Date", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (9701112 bytes); columns: ["row_id", "Ticker", "Date", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Target"]

## Public description

Competition: Multi-Asset Next-Day Return Forecasting (Fast-Food Giants)

Problem statement
You are given daily stock market data for 10 large fast-food related tickers. Your task is to predict the next trading day’s log return for each ticker-date in the test set, using only historical information available up to that date. This is a multi-series time-series regression challenge that emphasizes robust modeling across assets with different volatility regimes and history lengths.

Target definition
For each ticker s and date t, the target is the next-day log return computed from adjusted close prices:
Target_t = ln(AdjClose_{t+1} / AdjClose_{t})
Targets are defined only when both t and t+1 exist for a given ticker.

Files provided
- train.csv: Historical rows with features and the target for supervised training. Columns include:
  - row_id, Ticker, Date, Open, High, Low, Close, Adj Close, Volume, Target
- test.csv: Rows for which you must predict the next-day log return. Same columns as train.csv except without Target.
- sample_submission.csv: A template for your predictions with the correct row_id set and a numeric Target column to fill.

Temporal split
- Training rows are strictly before 2024-01-01.
- Test rows span 2024-01-01 to 2024-09-19 (inclusive), for dates where the next trading day exists per ticker.

Rules and constraints
- Use only information available up to the timestamp in each test row when constructing features.
- You may engineer features from any of the provided columns (Open, High, Low, Close, Adj Close, Volume) and may leverage cross-asset features from other tickers so long as they are strictly historical relative to the prediction date.
- No external data is required; you may use it at your discretion if it does not create leakage beyond the specified date.

Evaluation metric
- For each ticker s, compute RMSE over its test rows: RMSE_s.
- Compute the standard deviation of training targets per ticker from train.csv: std_train_s.
- Normalize: nRMSE_s = RMSE_s / std_train_s.
- Final leaderboard score is the mean of nRMSE_s over all tickers present in the test set. Lower is better.
Rationale: RMSE measures magnitude accuracy on a continuous target, and per-ticker normalization ensures fairness across different volatility levels and price scales.

Recommended approach (non-exhaustive)
- Data processing: sort by date, remove duplicates, align calendars per ticker, and compute lagged features safely.
- Feature engineering: rolling statistics (means, stds, skewness), momentum/volatility indicators (returns, ATR, RSI, MACD), volume signals, and cross-asset features (e.g., lead/lag correlations using only past data).
- Models: linear models with regularization, tree-based models (GBM/Random Forest), or sequence models (RNN/Transformer) with careful time-ordering.
- Validation: consider a backtesting scheme (e.g., expanding window) within the training period to select hyperparameters without leakage.

Important notes
- The dataset includes multiple tickers spanning several decades with varying coverage; only the specified 2024 window is used for evaluation.
- The final row_id uniquely identifies each (Ticker, Date) pair and must match exactly with test.csv.
- Submissions must be a CSV with two columns: row_id and Target.

Good luck and happy modeling!
