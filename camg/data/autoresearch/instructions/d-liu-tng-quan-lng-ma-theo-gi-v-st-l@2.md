# OpenMLE-fast task

Task ID: `d-liu-tng-quan-lng-ma-theo-gi-v-st-l@2`

Native metric: `LandslideEarlyWarningMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1101 bytes)
- `data/sample_submission.csv` (175450 bytes); columns: ["id", "target"]
- `data/test.csv` (412315 bytes); columns: ["id", "date", "hour", "rainfall_mm"]
- `data/train.csv` (1781545 bytes); columns: ["id", "date", "hour", "rainfall_mm", "target"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (17545 lines)
test.csv (17545 lines)
train.csv (70129 lines)```

-> sample_submission.csv has 17544 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 70128.00 - 87671.00, 0 nan values
target (float64) has 1 unique values: [0.5]

-> test.csv has 17544 rows and 4 columns.
Here is some information about the columns:
date (object) has 731 unique values. Some example values: ['2017-12-31', '2016-01-01', '2016-01-02', '2016-01-03']
hour (int64) has range: 1.00 - 24.00, 0 nan values
id (int64) has range: 70128.00 - 87671.00, 0 nan values
rainfall_mm (float64) has range: 0.00 - 80.10, 822 nan values

-> train.csv has 70128 rows and 5 columns.
Here is some information about the columns:
date (object) has 2922 unique values. Some example values: ['2015-12-31', '2008-01-01', '2008-01-02', '2008-01-03']
hour (int64) has range: 1.00 - 24.00, 0 nan values
id (int64) has range: 0.00 - 70127.00, 0 nan values
rainfall_mm (float64) has range: 0.00 - 107.00, 1725 nan values
target (int64) has 2 unique values: [0, 1]
