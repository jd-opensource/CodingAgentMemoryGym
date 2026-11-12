# OpenMLE-fast task

Task ID: `wild-blueberry-yield-prediction-dataset@1`

Native metric: `WildBlueberryYieldMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2664 bytes)
- `data/sample_submission.csv` (4885 bytes); columns: ["Id", "yield"]
- `data/test.csv` (13892 bytes); columns: ["Id", "clonesize", "honeybee", "bumbles", "andrena", "osmia", "MaxOfUpperTRange", "MinOfUpperTRange", "AverageOfUpperTRange", "MaxOfLowerTRange", "MinOfLowerTRange", "AverageOfLowerTRange", "RainingDays", "AverageRainingDays"]
- `data/train.csv` (48267 bytes); columns: ["Id", "clonesize", "honeybee", "bumbles", "andrena", "osmia", "MaxOfUpperTRange", "MinOfUpperTRange", "AverageOfUpperTRange", "MaxOfLowerTRange", "MinOfLowerTRange", "AverageOfLowerTRange", "RainingDays", "AverageRainingDays", "yield"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (195 lines)
test.csv (195 lines)
train.csv (584 lines)```

-> sample_submission.csv has 194 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 200000.00 - 200193.00, 0 nan values
yield (float64) has range: 1660.95 - 8966.05, 0 nan values

-> test.csv has 194 rows and 14 columns.
Here is some information about the columns:
AverageOfLowerTRange (float64) has 4 unique values: [55.9, 41.2, 45.8, 50.8]
AverageOfUpperTRange (float64) has 4 unique values: [79.0, 58.2, 64.7, 71.9]
AverageRainingDays (float64) has 5 unique values: [0.26, 0.39, 0.1, 0.56, 0.06]
Id (int64) has range: 200000.00 - 200193.00, 0 nan values
MaxOfLowerTRange (float64) has 4 unique values: [68.2, 50.2, 55.8, 62.0]
MaxOfUpperTRange (float64) has 4 unique values: [94.6, 69.7, 77.4, 86.0]
MinOfLowerTRange (float64) has 4 unique values: [33.0, 24.3, 27.0, 30.0]
MinOfUpperTRange (float64) has 4 unique values: [57.2, 42.1, 46.8, 52.0]
RainingDays (float64) has 5 unique values: [16.0, 24.0, 1.0, 34.0, 3.77]
andrena (float64) has 9 unique values: [0.63, 0.25, 0.5, 0.75, 0.38, 0.0, 0.409, 0.229, 0.234]
bumbles (float64) has 6 unique values: [0.25, 0.38, 0.585, 0.117, 0.065, 0.293]
clonesize (float64) has 6 unique values: [12.5, 25.0, 37.5, 20.0, 10.0, 40.0]
honeybee (float64) has 6 unique values: [0.25, 0.5, 0.0, 0.75, 0.537, 6.64]
osmia (float64) has 8 unique values: [0.75, 0.5, 0.63, 0.25, 0.0, 0.38, 0.058, 0.033]

-> train.csv has 583 rows and 15 columns.
Here is some information about the columns:
AverageOfLowerTRange (float64) has 5 unique values: [55.9, 45.8, 50.8, 41.2, 45.3]
AverageOfUpperTRange (float64) has 5 unique values: [79.0, 64.7, 71.9, 58.2, 65.6]
AverageRainingDays (float64) has 5 unique values: [0.26, 0.39, 0.56, 0.1, 0.06]
Id (int64) has range: 100000.00 - 100582.00, 0 nan values
MaxOfLowerTRange (float64) has 5 unique values: [68.2, 55.8, 62.0, 50.2, 66.0]
MaxOfUpperTRange (float64) has 5 unique values: [94.6, 77.4, 86.0, 69.7, 89.0]
MinOfLowerTRange (float64) has 5 unique values: [33.0, 27.0, 30.0, 24.3, 28.0]
MinOfUpperTRange (float64) has 5 unique values: [57.2, 46.8, 52.0, 42.1, 39.0]
RainingDays (float64) has 5 unique values: [16.0, 24.0, 34.0, 1.0, 3.77]
andrena (float64) has range: 0.00 - 0.75, 0 nan values
bumbles (float64) has 7 unique values: [0.25, 0.38, 0.117, 0.042, 0.058, 0.0, 0.202]
clonesize (float64) has 4 unique values: [25.0, 12.5, 20.0, 37.5]
honeybee (float64) has 7 unique values: [0.5, 0.25, 0.537, 0.0, 0.75, 18.43, 6.64]
osmia (float64) has range: 0.00 - 0.75, 0 nan values
yield (float64) has range: 1637.70 - 8969.40, 0 nan values
