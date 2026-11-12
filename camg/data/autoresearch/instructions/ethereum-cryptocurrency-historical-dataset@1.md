# OpenMLE-fast task

Task ID: `ethereum-cryptocurrency-historical-dataset@1`

Native metric: `EthereumLogRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (660 bytes)
- `data/sample_submission.csv` (10604 bytes); columns: ["NextDate", "PredictedLogPrice"]
- `data/test.csv` (25023 bytes); columns: ["RefDate", "NextDate", "Price", "Open", "High", "Low", "Vol", "ChangePct"]
- `data/train.csv` (160805 bytes); columns: ["RefDate", "NextDate", "Price", "Open", "High", "Low", "Vol", "ChangePct", "NextClose"]

## Public description

ETH Next-Day Close Forecasting Challenge

Problem statement
- Task: Using daily OHLCV information up to day t, predict the next day close (Price at t+1).

Data description
- Files in this directory:
  - train.csv: columns [RefDate, NextDate, Price, Open, High, Low, Vol, ChangePct, NextClose]
  - test.csv: columns [RefDate, NextDate, Price, Open, High, Low, Vol, ChangePct]
  - sample_submission.csv: columns [NextDate, PredictedLogPrice]

Evaluation
- RMSE on log-price: compare PredictedLogPrice with ln(NextClose) for the same NextDate.

Submission format
- CSV with columns [NextDate, PredictedLogPrice]; include each NextDate from test.csv exactly once.
