# OpenMLE-fast task

Task ID: `auto-mpg-dataset@2`

Native metric: `AutoMpgOriginMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1434 bytes)
- `data/sample_submission.csv` (468 bytes); columns: ["id", "origin"]
- `data/test.csv` (2843 bytes); columns: ["id", "mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model year"]
- `data/train.csv` (11803 bytes); columns: ["id", "mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model year", "origin"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (81 lines)
test.csv (81 lines)
train.csv (319 lines)```

-> sample_submission.csv has 80 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 5.00 - 397.00, 0 nan values
origin (int64) has 3 unique values: [3, 1, 2]

-> test.csv has 80 rows and 8 columns.
Here is some information about the columns:
acceleration (float64) has range: 8.00 - 24.60, 0 nan values
cylinders (int64) has 5 unique values: [8, 4, 6, 3, 5]
displacement (float64) has range: 68.00 - 455.00, 0 nan values
horsepower (float64) has range: 49.00 - 225.00, 2 nan values
id (int64) has range: 5.00 - 397.00, 0 nan values
model year (int64) has range: 70.00 - 82.00, 0 nan values
mpg (float64) has range: 11.00 - 46.60, 0 nan values
weight (int64) has range: 1825.00 - 4746.00, 0 nan values

-> train.csv has 318 rows and 9 columns.
Here is some information about the columns:
acceleration (float64) has range: 8.50 - 24.80, 0 nan values
cylinders (int64) has 5 unique values: [8, 4, 6, 3, 5]
displacement (float64) has range: 70.00 - 455.00, 0 nan values
horsepower (float64) has range: 46.00 - 230.00, 4 nan values
id (int64) has range: 0.00 - 395.00, 0 nan values
model year (int64) has range: 70.00 - 82.00, 0 nan values
mpg (float64) has range: 9.00 - 44.60, 0 nan values
origin (int64) has 3 unique values: [1, 3, 2]
weight (int64) has range: 1613.00 - 5140.00, 0 nan values
