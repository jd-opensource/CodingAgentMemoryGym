# OpenMLE-fast task

Task ID: `avocado-prices-2020@2`

Native metric: `AvocadoPriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (474 bytes)
- `data/sample_submission.csv` (73320 bytes); columns: ["date", "geography", "type", "average_price"]
- `data/test.csv` (46976 bytes); columns: ["date", "geography", "type"]
- `data/train.csv` (3380435 bytes); columns: ["date", "average_price", "total_volume", "4046", "4225", "4770", "total_bags", "small_bags", "large_bags", "xlarge_bags", "type", "year", "geography"]

## Public description

Avocado Price Forecasting Across Markets (2015–2020)

Files:
- train.csv: Historical data with targets and features.
- test.csv: Rows (date, geography, type) to predict.
- sample_submission.csv: Example with the correct columns and placeholder predictions.

Columns:
- date (YYYY-MM-DD), geography (string), type (conventional|organic)
- average_price (target, present in train.csv and sample_submission.csv)

Evaluation:
- Root Mean Squared Error (RMSE) on average_price.
