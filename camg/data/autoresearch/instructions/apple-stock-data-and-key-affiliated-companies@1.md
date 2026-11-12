# OpenMLE-fast task

Task ID: `apple-stock-data-and-key-affiliated-companies@1`

Native metric: `StockReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (687 bytes)
- `data/sample_submission.csv` (39445 bytes); columns: ["Date", "target"]
- `data/test.csv` (13370 bytes); columns: ["Date"]
- `data/test_features/asset_1.csv` (129565 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/test_features/asset_2.csv` (132813 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/test_features/asset_3.csv` (80450 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/test_features/asset_4.csv` (77333 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/test_features/asset_5.csv` (29567 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/test_features/asset_T.csv` (133356 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (85006 bytes); columns: ["Date", "target"]
- `data/train_features/asset_1.csv` (285053 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train_features/asset_2.csv` (290291 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train_features/asset_3.csv` (252207 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train_features/asset_4.csv` (171084 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train_features/asset_5.csv` (42 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train_features/asset_T.csv` (289107 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]

## Public description

Competition: Next-day return forecasting with multi-asset exogenous signals

Files (relative to this directory):
- train.csv
- test.csv
- sample_submission.csv
- train_features/asset_T.csv
- train_features/asset_1.csv
- train_features/asset_2.csv
- train_features/asset_3.csv
- train_features/asset_4.csv
- train_features/asset_5.csv
- test_features/asset_T.csv
- test_features/asset_1.csv
- test_features/asset_2.csv
- test_features/asset_3.csv
- test_features/asset_4.csv
- test_features/asset_5.csv

Submission format:
- CSV with two columns: Date,target
- Date values must exactly match test.csv and be unique

Evaluation:
- Root Mean Squared Error (RMSE) on target
- Lower is better
