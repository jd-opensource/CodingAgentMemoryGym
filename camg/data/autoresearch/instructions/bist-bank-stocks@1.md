# OpenMLE-fast task

Task ID: `bist-bank-stocks@1`

Native metric: `NextAdjReturnMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3355 bytes)
- `data/sample_submission.csv` (44836 bytes); columns: ["row_id", "next_adj_return"]
- `data/test.csv` (100743 bytes); columns: ["row_id", "date", "stock_name", "open", "high", "low", "close", "volume", "daily_return", "adj_close"]
- `data/train.csv` (1071280 bytes); columns: ["row_id", "date", "stock_name", "open", "high", "low", "close", "volume", "daily_return", "adj_close", "next_adj_return"]

## Public description

Cross-Stock Next-Day Adjusted Return Forecasting (BIST Banks)

Problem statement
Predict the next trading day’s adjusted close percentage return for Turkish banking stocks using only information available at day t. Each row represents one stock on trading day t; your target is the one-step-ahead adjusted return r_{t+1} in percentage points for the same stock.

Target definition
next_adj_return = 100 * (adj_close_{t+1} / adj_close_t - 1)
The target is computed from adjusted close prices to remove dividend/split effects.

Files provided
- train.csv: Feature rows at day t with the target next_adj_return.
- test.csv: Same schema as train.csv but without next_adj_return. You must predict it for every row.
- sample_submission.csv: Example submission with valid formatting.

Columns
- row_id: Unique identifier (e.g., Akbank_20200708). Treat as a string.
- date: Trading date t in YYYY-MM-DD.
- stock_name: Stock identifier (UTF-8 string; some names include Turkish characters).
- open, high, low, close: OHLC prices at day t.
- volume: Trading volume at day t.
- daily_return: Provided close-to-close daily return at day t (can be used as a feature).
- adj_close: Adjusted close price at day t.
- next_adj_return: Target in percentage points (present only in train.csv).

Train/test split
- Strictly time-based split.
  - Train: all rows with date <= 2024-12-31
  - Test: all rows with date >= 2025-01-02
- Rows are included only if a valid next trading day exists for the same stock (label availability). The very last available day per stock is excluded from both train and test.
- All nine banking stocks are present in both train and test.

Task scope and constraints
- Use only information available up to and including day t to predict r_{t+1}.
- You may derive features from historical data (lags, rolling statistics, volatility/volume indicators, candlestick features, cross-stock signals, calendar effects, etc.).
- Avoid leakage: do not use any information from t+1 or later to construct features for day t. Rolling features must be computed using past values only.
- You may train a single global model across stocks or per-stock models. Feature scaling can be global or per-stock.

Submission format
- A CSV with exactly two columns and the same number of rows as test.csv:
  - row_id
  - next_adj_return
- Row order does not matter, but row_id values must match test.csv exactly and be unique.
- Predictions must be finite numeric values (percentage points). Use UTF-8 encoding.

Evaluation
- Metric: Mean Absolute Error (MAE) over next_adj_return on all test rows.
  MAE = mean(|y_true − y_pred|)
- Rationale: MAE is robust to heavy-tailed errors and treats each stock/day equally. Using percentage returns ensures scale invariance across different price levels.

Modeling notes
- The series exhibit co-movement and regime changes. Consider cross-sectional features (e.g., same-day signals from other banks), rolling volatility/volume, price-based technicals, or simple baselines like persistence and moving averages.
- Non-trading gaps are handled implicitly: r_{t+1} uses the next observed trading day per stock.
- Some daily_return values in early rows may be missing; this is normal and these rows remain usable as features as long as adj_close exists.

Good luck and have fun building robust, leakage-free forecasting pipelines!
