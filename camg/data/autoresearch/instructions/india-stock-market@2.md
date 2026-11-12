# OpenMLE-fast task

Task ID: `india-stock-market@2`

Native metric: `IndiaNSEReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3277 bytes)
- `data/sample_submission.csv` (822448 bytes); columns: ["row_id", "target"]
- `data/test.csv` (1569840 bytes); columns: ["row_id", "Date", "Index", "Open", "High", "Low", "Close", "Volume", "breadth_mean_change", "breadth_median_change", "breadth_std_change", "breadth_advancers_ratio", "breadth_decliners_ratio", "breadth_total_volume", "breadth_num_stocks"]
- `data/train.csv` (7376634 bytes); columns: ["row_id", "Date", "Index", "Open", "High", "Low", "Close", "Volume", "breadth_mean_change", "breadth_median_change", "breadth_std_change", "breadth_advancers_ratio", "breadth_decliners_ratio", "breadth_total_volume", "breadth_num_stocks", "target"]

## Public description

India NSE Multi-Index Next-Day Return Forecasting

Problem statement
Build a model that predicts the next trading day’s close-to-close percent return for multiple NSE equity indices. For each index and trading day t, the target is y = Close_{t+1}/Close_t - 1. This is a panel time-series regression problem spanning broad and sector indices across many years and regimes.

Files provided
- train.csv: Per-index, per-day rows with input features and the target column.
- test.csv: Same schema as train.csv but without the target column; these are the rows you must predict.
- sample_submission.csv: A correctly formatted example submission file with random predictions.

Data schema (per row)
- row_id: Unique identifier for the row (string).
- Date: Trading date in ISO format (YYYY-MM-DD).
- Index: Index name (string).
- Open, High, Low, Close, Volume: Index OHLCV for day t.
- Breadth features derived from stock-level data for day t (shared across indices for that date):
  - breadth_mean_change: Equal-weighted average daily stock return (fraction; e.g., 0.0123 for 1.23%).
  - breadth_median_change: Cross-sectional median stock return (fraction).
  - breadth_std_change: Cross-sectional standard deviation of stock returns (fraction).
  - breadth_advancers_ratio: Fraction of stocks with positive daily return.
  - breadth_decliners_ratio: Fraction of stocks with negative daily return.
  - breadth_total_volume: Total traded volume over all stocks.
  - breadth_num_stocks: Number of stocks with available data on the date.
- target (train only): Next-day percent return for the index (fraction): Close_{t+1}/Close_t - 1.

Notes
- The index universe comprises non-leveraged NSE equity indices (broad and sectoral). Synthetic leveraged/inverse indices, pre-open series, volatility indices, and government securities indices are excluded for comparability.
- Some breadth features may be missing on certain dates; handle missing values robustly in your pipeline.
- All features correspond to information available up to and including date t; the target refers to t+1.

Evaluation
Submissions are evaluated using Mean Absolute Error (MAE) over all rows in the test set:
MAE = mean_i |y_i - yhat_i|
This choice is scale-free (returns) and robust to outliers relative to MSE.

Submission format
- CSV with exactly two columns and no header changes: row_id, target
- The row_id values must match those in test.csv in the same order.
- The target must be a finite numeric value (fractional return).

Train/Test split
- Deterministic chronological split: the earliest 80% of all index–date rows are in train, and the latest 20% are in test.
- Every index appearing in test also appears at least once in train.

What you can build
- Feature-engineered pipelines on OHLCV and breadth: momentum/trend, rolling stats, volatility estimators (e.g., Parkinson, close-to-close), turnover, calendar effects, cross-index context.
- Machine learning models: linear/multitask regression, tree ensembles, gradient boosting, quantile regression.
- Deep temporal models: temporal CNNs/RNNs/Transformers with panel embeddings and regularization.

Objective
Upload predictions for every row in test.csv using the specified submission format. Your goal is to minimize MAE on next-day returns.
