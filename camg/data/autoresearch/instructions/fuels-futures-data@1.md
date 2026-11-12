# OpenMLE-fast task

Task ID: `fuels-futures-data@1`

Native metric: `FuelReturnRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2599 bytes)
- `data/sample_submission.csv` (68989 bytes); columns: ["row_id", "target"]
- `data/test.csv` (232084 bytes); columns: ["row_id", "ticker", "date", "commodity", "open", "high", "low", "close", "volume"]
- `data/train.csv` (3834498 bytes); columns: ["row_id", "ticker", "date", "commodity", "open", "high", "low", "close", "volume", "target"]

## Public description

Title: Energy Futures One-Day-Ahead Return Forecasting

Problem statement
- Given historical daily OHLCV data for five energy futures (crude oil, Brent crude, natural gas, heating oil, RBOB gasoline), predict the next trading day close-to-close log return for each (ticker, date) in the test set.
- For each row keyed by (ticker, date) in the test set, predict y = ln(close_{t+1} / close_t), where close_t is the close price on the given date and close_{t+1} is the close price on that ticker’s next trading day.
- This is a multi-asset, panel time-series regression task. You may engineer any features using information up to and including the row’s date t only.

Files
- train.csv: Historical rows with target available for training. Columns: row_id, ticker, date, commodity, open, high, low, close, volume, target.
- test.csv: Rows to predict. Columns: row_id, ticker, date, commodity, open, high, low, close, volume. The target column is not included.
- sample_submission.csv: Submission template with the required format and a random but valid target for every row in test.csv. Columns: row_id, target.

Target definition
- For each ticker and date t, define the next-day log return as: target = ln(close_{t+1} / close_t).
- Only trading days within the dataset are considered. The last day per ticker (with no next trading day) is excluded.

Train/test split
- Strict chronological split, applied per ticker across the full panel.
- Train: all rows whose next trading day date is on or before 2022-12-31.
- Test: all rows whose next trading day date is on or after 2023-01-01 (up to the dataset’s end).
- The split ensures no leakage from the future. Rows are uniquely identified by row_id = "{ticker}_{YYYY-MM-DD}".

Evaluation
- Metric: Root Mean Squared Error (RMSE) on the target across all rows in test.csv.
- Every row in test.csv carries equal weight. Lower RMSE is better.
- Submission format: a CSV with exactly two columns named row_id and target. The row_id values must exactly match those in test.csv.

Notes and recommendations
- You may engineer features such as rolling statistics of returns/price/volume, technical indicators (RSI, MACD, ATR), realized/high-low volatility estimators, z-scores, seasonalities (day-of-week/month), and contemporaneous cross-asset features from the same date t. Ensure that no information from t+1 or later is used when constructing features for date t.
- Non-stationarity and regime changes are expected. Methods such as regularization, tree-based models, gradient boosting, temporal CNN/RNN/Transformers, and ensembling can be effective.
