# OpenMLE-fast task

Task ID: `stock-prices-vn30-indexvietnam@2`

Native metric: `Vn30RangeForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3192 bytes)
- `data/sample_submission.csv` (263642 bytes); columns: ["row_id", "y"]
- `data/test.csv` (473259 bytes); columns: ["row_id", "asset_id", "date", "open", "high", "low", "close", "volume"]
- `data/train.csv` (5193767 bytes); columns: ["row_id", "asset_id", "date", "open", "high", "low", "close", "volume", "y"]

## Public description

VN30 Next-Day Intraday Range Forecasting Challenge

Problem statement
You are given daily OHLCV (Open, High, Low, Close, Volume) data for 30 large-cap Vietnamese equities that are (or were) constituents of the VN30 index. For each asset and trading day d, your task is to predict the next trading day’s intraday volatility, defined as the log range between the next day’s High and Low prices:

  y_{t,d} = ln(High_{t,d+1}) − ln(Low_{t,d+1})

This target is strictly positive and scale-invariant, making it comparable across assets and time.

Data description
The competition files contain panel daily OHLCV for multiple assets and a supervised learning setup with targets only in the training set:
- train.csv: Training samples with columns
  - row_id: Unique identifier for each sample ("Axx-YYYY-MM-DD")
  - asset_id: De-identified asset code (e.g., A00, A01, ...)
  - date: Trading date in ISO format (YYYY-MM-DD) for which features (Open, High, Low, Close, Volume) are observed
  - open, high, low, close, volume: Daily OHLCV features for day d
  - y: Target value, the next-day log range ln(High_{d+1}) − ln(Low_{d+1})

- test.csv: Test samples with the same columns as train.csv except that y is not provided. You must predict y for each row in test.csv.

- sample_submission.csv: A sample file showing the required submission format. It contains two columns:
  - row_id: Matches the row_id in test.csv
  - y: Your prediction of the next-day log range for that row

Data split
The split preserves time order to avoid leakage:
- Training set covers earlier dates.
- Test set covers later dates up to the end of the dataset for each asset.
Only rows with an available next trading day are included (the final day per asset is excluded because the target cannot be computed).

Evaluation
Submissions are evaluated using Mean Absolute Error (MAE) over all test rows:

  MAE = mean(|y_pred − y_true|)

MAE is robust to heavy tails, appropriate for positive log-range values, and comparable across assets.

Rules and notes
- Use any features derived from the provided OHLCV and calendar information, but do not use any future information beyond day d to predict y_{d}.
- The panel is unbalanced (assets have different listing histories), and markets are non-stationary. Strong solutions typically benefit from careful feature engineering (e.g., realized ranges, volatility clustering, gaps, rolling statistics), and robust models (e.g., tree-based methods or sequence models).
- The identities of the original tickers are anonymized via asset_id to reduce the risk of external leakage.

Submission format
- File: a CSV with two columns: row_id, y
- The set of row_id values must exactly match those in test.csv.
- y must be finite real numbers. Predictions outside a reasonable range are allowed but will affect the MAE.

Tips
- Baselines: Moving averages of recent realized ranges (e.g., ln(High/Low)) and rolling volatility proxies can be strong starting points.
- Handle missing values and numeric stability carefully (e.g., logs). Validate your pipeline to avoid leakage from the future.

Final files
- train.csv
- test.csv
- sample_submission.csv

Good luck and happy modeling!
