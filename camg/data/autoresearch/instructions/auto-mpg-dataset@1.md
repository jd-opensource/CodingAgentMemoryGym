# OpenMLE-fast task

Task ID: `auto-mpg-dataset@1`

Native metric: `AutoMpgRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1726 bytes)
- `data/sample_submission.csv` (2681 bytes); columns: ["Id", "mpg"]
- `data/test.csv` (5900 bytes); columns: ["Id", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model year", "origin", "car name"]
- `data/train.csv` (15141 bytes); columns: ["Id", "mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model year", "origin", "car name"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (119 lines)
test.csv (119 lines)
train.csv (281 lines)```

-> sample_submission.csv has 118 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 280.00 - 397.00, 0 nan values
mpg (float64) has range: 6.06 - 33.27, 0 nan values

-> test.csv has 118 rows and 9 columns.
Here is some information about the columns:
Id (int64) has range: 280.00 - 397.00, 0 nan values
acceleration (float64) has range: 11.30 - 24.80, 0 nan values
car name (object) has 109 unique values. Some example values: ['chevrolet citation', 'toyota corolla', 'pontiac phoenix', 'datsun 210']
cylinders (int64) has 5 unique values: [6, 4, 8, 5, 3]
displacement (float64) has range: 70.00 - 360.00, 0 nan values
horsepower (float64) has range: 48.00 - 155.00, 4 nan values
model year (int64) has 4 unique values: [79, 80, 81, 82]
origin (int64) has 3 unique values: [1, 2, 3]
weight (int64) has range: 1755.00 - 4360.00, 0 nan values

-> train.csv has 280 rows and 10 columns.
Here is some information about the columns:
Id (int64) has range: 0.00 - 279.00, 0 nan values
acceleration (float64) has range: 8.00 - 23.50, 0 nan values
car name (object) has 212 unique values. Some example values: ['ford pinto', 'ford maverick', 'amc matador', 'chevrolet impala']
cylinders (int64) has 5 unique values: [8, 4, 6, 3, 5]
displacement (float64) has range: 68.00 - 455.00, 0 nan values
horsepower (float64) has range: 46.00 - 230.00, 2 nan values
model year (int64) has 9 unique values: [70, 71, 72, 73, 74, 75, 76, 77, 78]
mpg (float64) has range: 9.00 - 43.10, 0 nan values
origin (int64) has 3 unique values: [1, 3, 2]
weight (int64) has range: 1613.00 - 5140.00, 0 nan values
