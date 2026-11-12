# OpenMLE-fast task

Task ID: `2020-2025-apple-stock-dataset@1`

Native metric: `AppleLogReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1422 bytes)
- `data/sample_submission.csv` (3786 bytes); columns: ["Date", "next_log_return"]
- `data/test.csv` (23526 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]
- `data/train.csv` (116352 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume", "next_log_return"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (252 lines)
test.csv (252 lines)
train.csv (1004 lines)```

-> sample_submission.csv has 251 rows and 2 columns.
Here is some information about the columns:
Date (object) has 251 unique values. Some example values: ['2024-05-30', '2024-05-31', '2024-06-03', '2024-06-04']
next_log_return (float64) has 1 unique values: [0.0]

-> test.csv has 251 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 172.19 - 258.40, 0 nan values
Date (object) has 251 unique values. Some example values: ['2024-05-30', '2024-05-31', '2024-06-03', '2024-06-04']
High (float64) has range: 190.09 - 259.47, 0 nan values
Low (float64) has range: 168.99 - 257.01, 0 nan values
Open (float64) has range: 171.72 - 257.57, 0 nan values
Volume (int64) has range: 23234700.00 - 318679900.00, 0 nan values

-> train.csv has 1003 rows and 7 columns.
Here is some information about the columns:
Close (float64) has range: 78.33 - 196.67, 0 nan values
Date (object) has 1003 unique values. Some example values: ['2024-05-29', '2020-06-04', '2020-06-05', '2020-06-08']
High (float64) has range: 79.13 - 198.17, 0 nan values
Low (float64) has range: 77.96 - 195.57, 0 nan values
Open (float64) has range: 78.58 - 196.58, 0 nan values
Volume (int64) has range: 24048300.00 - 374336800.00, 0 nan values
next_log_return (float64) has range: -0.08 - 0.10, 0 nan values
