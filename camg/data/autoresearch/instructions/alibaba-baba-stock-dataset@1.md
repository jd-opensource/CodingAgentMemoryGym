# OpenMLE-fast task

Task ID: `alibaba-baba-stock-dataset@1`

Native metric: `BabaReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (128 bytes)
- `data/sample_submission.csv` (2154 bytes); columns: ["row_id", "target"]
- `data/test.csv` (5985 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (96560 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "target"]

## Public description

Title: BABA Next-Day Adjusted Return Forecasting

Files provided to participants
- train.csv
- test.csv
- sample_submission.csv
