# OpenMLE-fast task

Task ID: `apple-stock-data-from-2010-to-2024@1`

Native metric: `AppleReturnForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (89 bytes)
- `data/sample_submission.csv` (38536 bytes); columns: ["Id", "y1", "y5", "y10"]
- `data/test.csv` (41083 bytes); columns: ["Id", "Date", "Open Price", "High Price", "Low Price", "Close Price", "Volume"]
- `data/train.csv` (435785 bytes); columns: ["Id", "Date", "Open Price", "High Price", "Low Price", "Close Price", "Volume", "y1", "y5", "y10"]

## Public description

Files in this directory (relative paths):
- train.csv
- test.csv
- sample_submission.csv
