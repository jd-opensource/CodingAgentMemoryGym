# OpenMLE-fast task

Task ID: `samsung-stock-price-dataset@1`

Native metric: `SamsungReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1289 bytes)
- `data/sample_submission.csv` (8871 bytes); columns: ["row_id", "y"]
- `data/test.csv` (21772 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Adj Close", "Volume"]
- `data/train.csv` (448903 bytes); columns: ["Date", "Open", "High", "Low", "Adj Close", "Volume", "y"]

## Public description

Samsung Next-Day Log-Return Forecasting Challenge

Problem statement
- Predict the next trading day’s adjusted-close log return for Samsung Electronics using daily OHLCV data.
- For each day t in the dataset, the target is y_t = log(Adj Close_{t+1} / Adj Close_t). The last available date is excluded from training/testing.

Files provided (in public/)
- train.csv: rows with features and the target y for modeling.
- test.csv: rows with features only (no target), plus a row_id column for submission alignment.
- sample_submission.csv: example submission format with valid numeric predictions (two columns: row_id, y).

Features and target
- Features per row: Date, Open, High, Low, Adj Close, Volume.
- Target in train.csv: y, defined as the next-day adjusted-close log return.

Train/test split
- Chronological split to respect time order and prevent leakage.
- Train covers the earlier period; test covers the later period up to the penultimate trading day so that all test targets are well-defined.

Evaluation metric
- Mean Absolute Error (MAE) on log returns.
- MAE = mean over all test rows of |y_true − y_pred|.

Submission format
- A single CSV with two columns: row_id and y.
- row_id corresponds 1:1 to the rows in test.csv.
- y must be finite numeric values (no NaN/inf).
