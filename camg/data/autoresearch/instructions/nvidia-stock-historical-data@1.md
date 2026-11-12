# OpenMLE-fast task

Task ID: `nvidia-stock-historical-data@1`

Native metric: `NvdaReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1550 bytes)
- `data/sample_submission.csv` (3787 bytes); columns: ["Date", "next_day_log_return"]
- `data/test.csv` (8144 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (516235 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "next_day_log_return"]

## Public description

```
description.txt (35 lines)
sample_submission.csv (118 lines)
test.csv (118 lines)
train.csv (6276 lines)```

-> sample_submission.csv has 117 rows and 2 columns.
Here is some information about the columns:
Date (object) has 117 unique values. Some example values: ['2023-12-29', '2024-01-02', '2024-01-03', '2024-01-04']
next_day_log_return (float64) has range: -0.09 - 0.10, 0 nan values

-> test.csv has 117 rows and 7 columns.
Here is some information about the columns:
Adj Close (float64) has range: 47.56 - 131.88, 0 nan values
Close (float64) has range: 47.57 - 131.88, 0 nan values
Date (object) has 117 unique values. Some example values: ['2023-12-29', '2024-01-02', '2024-01-03', '2024-01-04']
High (float64) has range: 48.18 - 133.73, 0 nan values
Low (float64) has range: 47.32 - 129.58, 0 nan values
Open (float64) has range: 47.49 - 132.99, 0 nan values
Volume (int64) has range: 222551200.00 - 1142269000.00, 0 nan values

-> train.csv has 6275 rows and 8 columns.
Here is some information about the columns:
Adj Close (float64) has range: 0.03 - 50.40, 0 nan values
Close (float64) has range: 0.03 - 50.41, 0 nan values
Date (object) has 6275 unique values. Some example values: ['2023-12-28', '1999-01-22', '1999-01-25', '2023-11-01']
High (float64) has range: 0.04 - 50.55, 0 nan values
Low (float64) has range: 0.03 - 49.41, 0 nan values
Open (float64) has range: 0.03 - 50.22, 0 nan values
Volume (int64) has range: 19680000.00 - 9230856000.00, 0 nan values
next_day_log_return (float64) has range: -0.43 - 0.35, 0 nan values
