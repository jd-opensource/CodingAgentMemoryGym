# OpenMLE-fast task

Task ID: `daily-potato-prices-and-trade-volume-q1-2025@1`

Native metric: `PotatoPriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (320 bytes)
- `data/sample_submission.csv` (1930 bytes); columns: ["row_id", "PredictedPrice"]
- `data/test.csv` (10906 bytes); columns: ["row_id", "date", "variety", "price_min", "price_max", "price_avg", "volume_tm"]
- `data/train.csv` (68324 bytes); columns: ["row_id", "date", "variety", "price_min", "price_max", "price_avg", "volume_tm", "target"]

## Public description

Daily Potato Prices – Next-Day Forecasting (Peru, Jan–May 2025)

Files:
- train.csv: training data with features and next-day target.
- test.csv: test data features (participants must predict next-day average price).
- sample_submission.csv: example submission format with column names ['row_id', 'PredictedPrice'].
