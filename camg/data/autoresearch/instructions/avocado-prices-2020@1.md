# OpenMLE-fast task

Task ID: `avocado-prices-2020@1`

Native metric: `AvocadoForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (645 bytes)
- `data/sample_submission.csv` (1192552 bytes); columns: ["geography", "type", "date", "target", "value"]
- `data/test.csv` (831507 bytes); columns: ["geography", "type", "date", "target"]
- `data/test_data.csv` (831507 bytes); columns: ["geography", "type", "date", "target"]
- `data/train.csv` (3141160 bytes); columns: ["date", "geography", "type", "average_price", "total_volume", "4046", "4225", "4770", "total_bags", "small_bags", "large_bags", "xlarge_bags"]

## Public description

Avocado Demand Decomposition Forecasting (2015–2020)

Files in this directory:
- train.csv: Historical weekly data with features and targets.
- test.csv: Forecasting template in long format with columns [geography, type, date, target].
- test_data.csv: Same as test.csv, provided for convenience.
- sample_submission.csv: Example submission matching the required schema [geography, type, date, target, value].

Submission format
Submit a CSV with columns: geography, type, date, target, value. One row per required forecast.

Evaluation
Submissions are evaluated with RMSLE between predicted 'value' and ground-truth values (lower is better).
