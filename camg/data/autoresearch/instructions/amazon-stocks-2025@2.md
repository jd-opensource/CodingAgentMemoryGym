# OpenMLE-fast task

Task ID: `amazon-stocks-2025@2`

Native metric: `AmazonVolatilityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2291 bytes)
- `data/sample_submission.csv` (43129 bytes); columns: ["row_id", "y"]
- `data/test.csv` (139806 bytes); columns: ["row_id", "date", "open", "high", "low", "close", "volume", "stock_splits"]
- `data/train.csv` (737591 bytes); columns: ["row_id", "date", "open", "high", "low", "close", "volume", "stock_splits", "y"]

## Public description

AMZN 5-Day Realized Volatility Forecasting (Range-Based)

Problem statement
Predict the next 5-trading-day realized volatility for Amazon (AMZN) using only information available up to the prediction day. For each evaluation date t, submit a point forecast of the log realized volatility over days t+1..t+5.

Provided files
- train.csv: Historical rows with features and the target y.
- test.csv: Evaluation rows with the same features but without y.
- sample_submission.csv: Submission template with required columns and example values.

Data schema
Each row represents a trading day (date t).
- row_id: Unique identifier, e.g., AMZN_20191231
- date: Trading date in YYYY-MM-DD
- open, high, low, close: Daily prices (float)
- volume: Daily traded shares (float)
- stock_splits: Split ratio on date t (float; usually 0.0)
- y (train only): Target defined below

Target definition (y)
- Parkinson daily variance: v_d = [ln(High_d / Low_d)]^2 / (4 ln 2)
- 5-day realized volatility at day t: sigma_{t,5} = sqrt( sum_{k=1..5} v_{t+k} )
- Target: y_t = log( sigma_{t,5} )
Targets exist only where the five future trading days are available. Do not try to recompute y for test.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on y.
- Submission format: CSV with exactly two columns [row_id, y]. The row_id values must match those in test.csv.

Rules and guidance
- No lookahead: Use only information up to and including day t when constructing features. Do not use data from t+1..t+5.
- Feature engineering is encouraged (e.g., rolling ranges/ATR, returns, volatility clustering features, volume/price interactions, calendar effects, split flags).
- Numeric stability matters; outliers and regime shifts are present across the full history.

Split
- Chronological split to emulate real forecasting.
- Train dates: 1997-05-15 .. 2019-12-31
- Test dates: 2020-01-02 .. 2025-02-13
All test rows have five subsequent trading days in the underlying history to define the (hidden) targets.

Notes
- Dividends are always 0 in this dataset and are not included.
- All numeric fields are floats; there are no missing values in the provided files.

Deliverable
- Upload a submission.csv with columns [row_id, y]. Any real number is allowed for y. The leaderboard uses RMSE on the hidden test targets.
