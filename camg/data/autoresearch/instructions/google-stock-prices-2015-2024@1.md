# OpenMLE-fast task

Task ID: `google-stock-prices-2015-2024@1`

Native metric: `GoogleStockRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1412 bytes)
- `data/sample_submission.csv` (28630 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]
- `data/test.csv` (5045 bytes); columns: ["Date"]
- `data/train.csv` (119287 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]

## Public description

```
description.txt (36 lines)
sample_submission.csv (253 lines)
test.csv (253 lines)
train.csv (2265 lines)```

-> sample_submission.csv has 252 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 135.16 - 143.99, 0 nan values
Date (object) has 252 unique values. Some example values: ['2024-01-02 16:00:00', '2024-01-03 16:00:00', '2024-01-04 16:00:00', '2024-01-05 16:00:00']
High (float64) has range: 138.24 - 145.77, 0 nan values
Low (float64) has range: 133.66 - 141.13, 0 nan values
Open (float64) has range: 136.03 - 145.07, 0 nan values
Volume (float64) has range: 11536451.48 - 31258911.07, 0 nan values

-> test.csv has 252 rows and 1 columns.
Here is some information about the columns:
Date (object) has 252 unique values. Some example values: ['2024-01-02 16:00:00', '2024-01-03 16:00:00', '2024-01-04 16:00:00', '2024-01-05 16:00:00']

-> train.csv has 2264 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 24.85 - 149.84, 0 nan values
Date (object) has 2264 unique values. Some example values: ['2023-12-29 16:00:00', '2015-01-02 16:00:00', '2015-01-05 16:00:00', '2015-01-06 16:00:00']
High (float64) has range: 25.01 - 151.55, 0 nan values
Low (float64) has range: 24.55 - 148.90, 0 nan values
Open (float64) has range: 24.96 - 151.25, 0 nan values
Volume (int64) has range: 465638.00 - 119455020.00, 0 nan values
