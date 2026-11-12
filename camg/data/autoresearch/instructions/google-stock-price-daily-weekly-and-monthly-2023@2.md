# OpenMLE-fast task

Task ID: `google-stock-price-daily-weekly-and-monthly-2023@2`

Native metric: `GoogleStockRangeForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (774 bytes)
- `data/sample_submission.csv` (21401 bytes); columns: ["id", "y"]
- `data/test.csv` (42061 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose"]
- `data/test_daily.csv` (33306 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose"]
- `data/test_monthly.csv` (1708 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose"]
- `data/test_weekly.csv` (7135 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose"]
- `data/train.csv` (210267 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose", "y"]
- `data/train_daily.csv` (166982 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose", "y"]
- `data/train_monthly.csv` (8175 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose", "y"]
- `data/train_weekly.csv` (35202 bytes); columns: ["id", "Date", "Open", "High", "Low", "Close", "Volume", "AdjClose", "y"]

## Public description

Competition: Multi-Frequency Next-Period Realized Range Forecasting for GOOGL

Files provided (under this public directory):
- train.csv, test.csv
- train_daily.csv, test_daily.csv
- train_weekly.csv, test_weekly.csv
- train_monthly.csv, test_monthly.csv
- sample_submission.csv

Columns:
- id: unique identifier (prefix indicates frequency: daily_, weekly_, monthly_)
- Date, Open, High, Low, Close, Volume, AdjClose
- y (only in train*.csv): next period realized log-range = log(High_{t+1}/Low_{t+1})

Train/test split:
- 80/20 chronological split on the aligned series for each frequency.

Submission format:
- CSV with two columns: id,y covering all rows in test.csv.

Evaluation:
- Mean Absolute Error (MAE) per frequency, averaged equally across daily/weekly/monthly.
