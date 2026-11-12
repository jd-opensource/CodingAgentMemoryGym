# OpenMLE-fast task

Task ID: `orders-csv@1`

Native metric: `DailyRevenueForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (851 bytes)
- `data/sample_submission.csv` (5483 bytes); columns: ["date", "daily_total_sales"]
- `data/test.csv` (4009 bytes); columns: ["date"]
- `data/train.csv` (21957 bytes); columns: ["date", "daily_total_sales"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (365 lines)
test.csv (365 lines)
train.csv (1095 lines)```

-> sample_submission.csv has 364 rows and 2 columns.
Here is some information about the columns:
daily_total_sales (float64) has 1 unique values: [0.0]
date (object) has 364 unique values. Some example values: ['2017-12-30', '2017-01-01', '2017-01-02', '2017-01-03']

-> test.csv has 364 rows and 1 columns.
Here is some information about the columns:
date (object) has 364 unique values. Some example values: ['2017-12-30', '2017-01-01', '2017-01-02', '2017-01-03']

-> train.csv has 1094 rows and 2 columns.
Here is some information about the columns:
daily_total_sales (float64) has range: 0.00 - 28106.72, 0 nan values
date (object) has 1094 unique values. Some example values: ['2016-12-31', '2014-01-03', '2014-01-04', '2014-01-05']
