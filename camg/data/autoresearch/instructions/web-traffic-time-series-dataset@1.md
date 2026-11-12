# OpenMLE-fast task

Task ID: `web-traffic-time-series-dataset@1`

Native metric: `WebTrafficForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1293 bytes)
- `data/sample_submission.csv` (12993 bytes); columns: ["Timestamp", "TrafficCount"]
- `data/test.csv` (8798 bytes); columns: ["Timestamp"]
- `data/train.csv` (80885 bytes); columns: ["Timestamp", "TrafficCount"]

## Public description

Web Traffic 14-Day Hourly Forecast Challenge

Problem statement
Given historical web traffic (total number of web requests) for a single website, forecast the traffic for each timestamp in the final 14-day horizon. This is a univariate time-series forecasting task with strong daily/weekly seasonality, occasional gaps, spikes, and moderate trend changes.

What you are given
- train.csv: Historical data prior to the 14-day test horizon. Columns: Timestamp, TrafficCount.
- test.csv: The timestamps to forecast during the last 14 days of the series. Column: Timestamp.
- sample_submission.csv: Example submission file with the correct structure and placeholder predictions.

Your task
- Learn from train.csv and predict TrafficCount for every row in test.csv.
- Submit a CSV with exactly two columns and this order: Timestamp, TrafficCount.
- The number of rows and the Timestamp values must exactly match test.csv.

Evaluation
- Metric: SMAPE (Symmetric Mean Absolute Percentage Error), reported in percent. Lower is better.
  SMAPE = 100 * mean( |y_pred - y_true| / (|y_pred| + |y_true|) ), with the per-row term defined as 0 when both are 0.

Rules
- Do not include extra columns, NaN/Inf values, or missing rows.
- Do not use external data; forecasts must be derived from train.csv only.
