# OpenMLE-fast task

Task ID: `city-typeseda-and-model@2`

Native metric: `CityPM25ForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (492 bytes)
- `data/sample_submission.csv` (201215 bytes); columns: ["row_id", "Target_PM2.5_24h"]
- `data/test.csv` (688368 bytes); columns: ["row_id", "Date", "City", "CO", "NO2", "SO2", "O3", "PM2.5", "PM10", "Type"]
- `data/train.csv` (3728266 bytes); columns: ["row_id", "Date", "City", "CO", "NO2", "SO2", "O3", "PM2.5", "PM10", "Type", "Target_PM2.5_24h"]

## Public description

City Air Quality: 24-hour-ahead PM2.5 Forecasting

Files provided (under public/):
- train.csv: row_id, Date, City, CO, NO2, SO2, O3, PM2.5, PM10, Type, Target_PM2.5_24h
- test.csv: row_id, Date, City, CO, NO2, SO2, O3, PM2.5, PM10, Type
- sample_submission.csv: row_id, Target_PM2.5_24h

Submission format:
- CSV with exactly two columns: row_id, Target_PM2.5_24h, covering all row_id from test.csv.

Evaluation:
- RMSE between predictions and ground truth on the test set. Lower is better.
