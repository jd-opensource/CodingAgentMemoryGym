# OpenMLE-fast task

Task ID: `gold-future-prices@2`

Native metric: `GoldVolatilityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1339 bytes)
- `data/sample_submission.csv` (13706 bytes); columns: ["Id", "target"]
- `data/test.csv` (23260 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close"]
- `data/train.csv` (205924 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "target"]

## Public description

```
description.txt (63 lines)
sample_submission.csv (529 lines)
test.csv (529 lines)
train.csv (3196 lines)```

-> sample_submission.csv has 528 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 3195.00 - 3722.00, 0 nan values
target (float64) has range: 0.00 - 0.02, 0 nan values

-> test.csv has 528 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 1630.90 - 2093.10, 0 nan values
Date (object) has 528 unique values. Some example values: ['02/07/2024', '12/31/2021', '01/03/2022', '01/04/2022']
High (float64) has range: 1634.20 - 2152.30, 0 nan values
Id (int64) has range: 3195.00 - 3722.00, 0 nan values
Low (float64) has range: 1621.10 - 2074.60, 0 nan values
Open (float64) has range: 1629.20 - 2094.40, 0 nan values

-> train.csv has 3195 rows and 7 columns.
Here is some information about the columns:
Close (float64) has range: 888.20 - 2069.40, 0 nan values
Date (object) has 3195 unique values. Some example values: ['12/30/2021', '04/24/2009', '04/27/2009', '04/28/2009']
High (float64) has range: 890.80 - 2089.20, 0 nan values
Id (int64) has range: 0.00 - 3194.00, 0 nan values
Low (float64) has range: 880.10 - 2049.00, 0 nan values
Open (float64) has range: 887.50 - 2076.40, 0 nan values
target (float64) has range: 0.00 - 0.06, 0 nan values
