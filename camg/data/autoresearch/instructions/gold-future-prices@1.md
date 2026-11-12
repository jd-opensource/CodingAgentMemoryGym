# OpenMLE-fast task

Task ID: `gold-future-prices@1`

Native metric: `GoldDirectionLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1310 bytes)
- `data/sample_submission.csv` (4749 bytes); columns: ["Id", "Up"]
- `data/test.csv` (23216 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close"]
- `data/train.csv` (145529 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Up"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (528 lines)
test.csv (528 lines)
train.csv (3197 lines)```

-> sample_submission.csv has 527 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 3196.00 - 3722.00, 0 nan values
Up (float64) has 1 unique values: [0.5]

-> test.csv has 527 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 1630.90 - 2093.10, 0 nan values
Date (object) has 527 unique values. Some example values: ['2024-02-07', '2022-01-03', '2022-01-04', '2022-01-05']
High (float64) has range: 1634.20 - 2152.30, 0 nan values
Id (int64) has range: 3196.00 - 3722.00, 0 nan values
Low (float64) has range: 1621.10 - 2074.60, 0 nan values
Open (float64) has range: 1629.20 - 2094.40, 0 nan values

-> train.csv has 3196 rows and 7 columns.
Here is some information about the columns:
Close (float64) has range: 888.20 - 2069.40, 0 nan values
Date (object) has 3196 unique values. Some example values: ['2021-12-31', '2009-04-24', '2009-04-27', '2009-04-28']
High (float64) has range: 890.80 - 2089.20, 0 nan values
Id (int64) has range: 0.00 - 3195.00, 0 nan values
Low (float64) has range: 880.10 - 2049.00, 0 nan values
Open (float64) has range: 887.50 - 2076.40, 0 nan values
Up (int64) has 2 unique values: [0, 1]
