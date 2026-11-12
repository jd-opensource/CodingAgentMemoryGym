# OpenMLE-fast task

Task ID: `netflix-stock-data-2025@1`

Native metric: `NFLXLogReturnForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (182 bytes)
- `data/sample_submission.csv` (8767 bytes); columns: ["row_id", "target_5d_log_return"]
- `data/test.csv` (37353 bytes); columns: ["row_id", "date", "open", "high", "low", "close", "adj_close", "volume"]
- `data/train.csv` (698471 bytes); columns: ["date", "open", "high", "low", "close", "adj_close", "volume", "target_5d_log_return"]

## Public description

Title: NFLX 5-Day Cumulative Log-Return Forecasting

Files provided
- train.csv
- test.csv
- sample_submission.csv

Submission format
- CSV with columns: row_id,target_5d_log_return
