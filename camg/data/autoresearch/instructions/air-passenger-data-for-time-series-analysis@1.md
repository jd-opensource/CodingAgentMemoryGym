# OpenMLE-fast task

Task ID: `air-passenger-data-for-time-series-analysis@1`

Native metric: `AirPassengerForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1434 bytes)
- `data/sample_submission.csv` (973 bytes); columns: ["Month", "Passengers"]
- `data/test.csv` (294 bytes); columns: ["Month"]
- `data/train.csv` (1313 bytes); columns: ["Month", "Passengers"]

## Public description

Title: Monthly Air Passenger Forecasting (1958–1960)

Problem statement
- You are given monthly counts of international airline passengers from Jan 1949 through Dec 1957.
- Your task is to forecast the monthly passenger counts for Jan 1958 through Dec 1960 (36 months ahead).

Data description (paths are relative to this public directory)
- train.csv: Two columns — Month and Passengers. Contains 108 consecutive months from 1949-01 to 1957-12.
- test.csv: One column — Month. Contains 36 consecutive months from 1958-01 to 1960-12.
- sample_submission.csv: Two columns — Month and Passengers. A valid example of the expected submission format.

Important properties
- Month is a monthly timestamp (YYYY-MM) and is strictly sequential with no gaps or duplicates.
- Passengers are strictly positive counts; you may predict integers or floats.
- The series exhibits an increasing trend and strong month-of-year seasonality.

Submission format
- Submit a CSV with exactly two columns: Month and Passengers.
- The Month values must exactly match those in test.csv (same set, same order, formatted YYYY-MM).
- The Passengers column must be numeric, finite, and non-missing.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) over the 36 test months.
- Definition: RMSLE = sqrt(mean((log1p(y_true) - log1p(max(y_pred, 0)))^2)).

Files provided in this public directory
- train.csv
- test.csv
- sample_submission.csv
