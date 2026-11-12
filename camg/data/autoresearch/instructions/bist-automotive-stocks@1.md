# OpenMLE-fast task

Task ID: `bist-automotive-stocks@1`

Native metric: `AutomotiveStocksNextDayReturnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3670 bytes)
- `data/sample_submission.csv` (43638 bytes); columns: ["date", "stock_name", "y"]
- `data/test.csv` (68767 bytes); columns: ["date", "stock_name", "open", "high", "low", "close", "adj_close", "volume", "daily_return"]
- `data/train.csv` (785566 bytes); columns: ["date", "stock_name", "open", "high", "low", "close", "adj_close", "volume", "daily_return", "y"]

## Public description

Competition: BIST Auto Stocks — Cross-Sectional Next‑Day Return Forecasting

Problem statement
You are given aligned daily OHLCV data for eight Turkish automotive stocks listed on Borsa Istanbul (BIST). For each stock and trading day t, your task is to predict the next trading day’s adjusted close-to-close log return y_t = ln(adj_close_{t+1} / adj_close_{t}) using only information available up to and including day t. Models should generalize across both time and the eight-stock cross-section.

Data description
- Train file: train.csv — per-date, per-stock rows with input features and the target label.
- Test file: test.csv — per-date, per-stock rows with input features only. The rows correspond to dates where the next-day label exists and the cross-section is complete for all eight stocks.
- Sample submission: sample_submission.csv — template containing the required prediction keys and a valid example of y values.

Columns
All files use the following columns (train includes the label y):
- date: trading date in YYYY-MM-DD format
- stock_name: stock identifier (one of eight automotive companies)
- open, high, low, close: daily price fields
- adj_close: adjusted closing price (target is computed from this)
- volume: total traded volume for the day
- daily_return: provided daily return; may be used as a feature
- y (train only): next-day log return ln(adj_close_{t+1} / adj_close_{t}) computed per stock and date t

Train/test split
- Train covers 2020-07-13 through 2024-12-31 (inclusive) for all eight stocks, restricted to dates where adj_close values at t and t+1 are available for all stocks.
- Test covers 2025-01-01 through 2025-07-10 (inclusive) under the same completeness rule.

Important notes
- The target is derived from adjusted prices to avoid distortions from corporate actions.
- The final date per stock is excluded from supervision because its t+1 label is unavailable.
- All test dates have a complete eight-stock cross-section to ensure fair evaluation.

Submission format
Submit a single CSV with columns exactly: [date, stock_name, y]
- date: in YYYY-MM-DD format
- stock_name: stock identifier string
- y: your predicted next-day log return (float), can be any real number
The submission must contain the same rows, in the same order, as the test file’s [date, stock_name] pairs.

Evaluation metric
We evaluate using the mean Spearman rank correlation (Information Coefficient, IC) computed cross-sectionally per test date and then averaged across all test dates:
1) For each test date D, compute Spearman correlation between your predictions and the true y across the eight stocks on that date.
2) Average these daily IC values across all test dates to obtain the final score.
Edge cases are handled conservatively: if all predictions for a given date are equal (constant), the correlation for that date is set to 0 to keep the metric well-defined.

Modeling guidance
- Respect time order: features for date t must be computed using data up to and including t.
- Feature engineering ideas: momentum and returns at multiple lags; rolling volatility; high–low range and true range measures; moving averages and deviations; volume statistics; same-date cross-sectional z-scores; calendar features.
- Avoid leakage: ensure that any rolling features and cross-sectional normalizations use only information from t and earlier, or same-day cross-sectional information.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your goal is to maximize the mean daily Spearman IC on the test set by building robust models that capture signals in the OHLCV data across both time and the eight-stock cross-section.
