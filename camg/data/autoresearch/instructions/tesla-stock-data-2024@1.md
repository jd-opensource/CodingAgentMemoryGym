# OpenMLE-fast task

Task ID: `tesla-stock-data-2024@1`

Native metric: `TSLAReturnForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2677 bytes)
- `data/sample_submission.csv` (8303 bytes); columns: ["row_id", "target"]
- `data/test.csv` (21750 bytes); columns: ["row_id", "date", "open", "high", "low", "close", "adj_close", "volume"]
- `data/train.csv` (388831 bytes); columns: ["row_id", "date", "open", "high", "low", "close", "adj_close", "volume", "target"]

## Public description

Competition: TSLA Next-Day Log Return Forecast

Problem statement
Participants are provided with daily OHLCV data for Tesla (TSLA). For each trading day t in the test set, predict the next trading day’s adjusted close log return, defined as:
  target = log(AdjClose[t+1] / AdjClose[t])
Only information available up to and including day t should be used to form predictions. This is a single-asset, one‑step‑ahead time‑series regression task.

Files provided
- train.csv: Historical daily data with columns [row_id, date, open, high, low, close, adj_close, volume, target]. The target is the next‑day adjusted close log return for each row.
- test.csv: Same schema as train.csv but without the target column.
- sample_submission.csv: A valid example submission with columns [row_id, target].

Important notes
- date is provided in ISO format (YYYY-MM-DD). All rows are sorted by date ascending and represent unique trading days.
- The task is strictly one‑day‑ahead forecasting; do not use any future information beyond day t when constructing features.
- You may engineer any features based on the provided columns and date, as long as they are computed using data up to and including day t.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on the predicted next‑day log returns.
  RMSE = sqrt(mean((y_true - y_pred)^2))
- Lower is better. RMSE is robust and scale‑compatible for log returns, and penalizes large errors on volatile days.

Train/test split
- Time-based split. The train set contains rows up to the end of 2023. The test set contains rows from 2024 only, ending before the last available day to ensure every test row has a valid next‑day target.
- Exact boundaries used by prepare.py:
  • Train rows: dates <= 2023-12-29
  • Test rows: 2024-01-02 through 2024-12-06 (inclusive)

Submission format
- A CSV file with exactly two columns and a header: [row_id, target]
- row_id must match the IDs in test.csv. Order does not matter, but there must be a one‑to‑one match with no duplicates or missing IDs.
- target must be a real-valued prediction for the next‑day adjusted close log return. Avoid NaN/Inf values.

Modeling guidance (optional)
- Baselines: last‑return models, linear models on lagged OHLCV/technical features, tree ensembles, or sequence models.
- Feature ideas: rolling means/volatility of prices and ranges, RSI/MACD/ATR-like indicators, volume z‑scores, day‑of‑week/month effects, regime/volatility state features. Ensure no look‑ahead when computing features.

Deliverables summary
- Use train.csv to train your model.
- Predict target for every row in test.csv.
- Submit a CSV with [row_id, target].
