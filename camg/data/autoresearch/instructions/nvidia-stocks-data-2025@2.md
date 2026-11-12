# OpenMLE-fast task

Task ID: `nvidia-stocks-data-2025@2`

Native metric: `NVDAIntradayRangeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3009 bytes)
- `data/sample_submission.csv` (8846 bytes); columns: ["Date", "target_log_range_next_day"]
- `data/test.csv` (22396 bytes); columns: ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
- `data/train.csv` (629380 bytes); columns: ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume", "target_log_range_next_day"]

## Public description

Title: NVDA Next-Day Intraday Range Forecasting

Problem Statement
You are given NVIDIA (NVDA) daily OHLCV data. For each trading day t, use information available up to and including day t to predict the next trading day’s realized intraday volatility, defined as the natural log of the High/Low price ratio on day t+1:
  target_log_range_next_day = ln(High_{t+1} / Low_{t+1})

This is a univariate, time-ordered regression problem with strong volatility clustering and regime shifts across 1999–2025. Effective solutions will combine careful data processing, feature engineering, and robust modeling.

Files Provided
- train.csv: Daily OHLCV features and the target column target_log_range_next_day.
- test.csv: Daily OHLCV features for which you must predict target_log_range_next_day.
- sample_submission.csv: Example submission showing the required format.

Columns
All provided CSVs use these columns (in this order):
- Date: Trading date (YYYY-MM-DD)
- Adj Close: Adjusted closing price after corporate actions
- Close: Closing stock price
- High: Highest price of the day
- Low: Lowest price of the day
- Open: Opening stock price
- Volume: Number of shares traded
- target_log_range_next_day: Prediction target (present only in train.csv and in your submission; not present in test.csv)

Task and Constraints
- Use only information available up to and including each day t to build features and train models. The target uses day t+1 High and Low.
- The data spans 1999 through early 2025 and is strictly ordered by Date. Treat it as a time series; do not shuffle across time.
- Avoid leakage: do not fit transformations (e.g., scalers) on train+test jointly, and compute rolling features using only past data.
- You may engineer any features from the provided columns (e.g., ranges, returns, gaps, ATR-like indicators, volume/momentum features), and you may use any ML methods.

Evaluation Metric
Submissions are evaluated using Mean Absolute Error (MAE) on target_log_range_next_day. MAE is robust and symmetric, and the log-range target normalizes price level changes across time.

Submission Format
Your submission must be a CSV with exactly these columns and ordering:
- Date
- target_log_range_next_day

Additional requirements:
- Date values must match test.csv exactly and be strictly increasing with no duplicates.
- target_log_range_next_day values must be non-negative, finite real numbers.

Train/Test Split
- Train set: all rows whose next-day label date is before 2024-01-01.
- Test set: all rows whose feature Date is on/after 2024-01-01.
This creates a strictly out-of-sample evaluation window in 2024–2025 while preserving a large training history.

Starter Tips
- Baselines: rolling medians/means of recent log-ranges; HAR-style features based on multiple horizons; gradient boosting or sequence models.
- Be careful with rolling window warm-ups and missing values.
- Use time-series cross-validation (e.g., expanding window) for model selection.

Good luck and happy modeling!
