# OpenMLE-fast task

Task ID: `concrete-compressive-strength@1`

Native metric: `ConcreteCompressiveStrengthMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1575 bytes)
- `data/sample_submission.csv` (4484 bytes); columns: ["Id", "strength"]
- `data/test.csv` (9608 bytes); columns: ["Id", "cement", "blast_furnace_slag", "fly_ash", "water", "superplasticizer", "coarse_aggregate", "fine_aggregate", "age"]
- `data/train.csv` (44666 bytes); columns: ["cement", "blast_furnace_slag", "fly_ash", "water", "superplasticizer", "coarse_aggregate", "fine_aggregate", "age", "strength"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (207 lines)
test.csv (207 lines)
train.csv (825 lines)```

-> sample_submission.csv has 206 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 0.00 - 205.00, 0 nan values
strength (float64) has range: 0.00 - 79.99, 0 nan values

-> test.csv has 206 rows and 9 columns.
Here is some information about the columns:
Id (int64) has range: 0.00 - 205.00, 0 nan values
age (int64) has range: 3.00 - 365.00, 0 nan values
blast_furnace_slag (float64) has range: 0.00 - 290.20, 0 nan values
cement (float64) has range: 102.00 - 540.00, 0 nan values
coarse_aggregate (float64) has range: 801.00 - 1145.00, 0 nan values
fine_aggregate (float64) has range: 605.00 - 942.00, 0 nan values
fly_ash (float64) has range: 0.00 - 195.00, 0 nan values
superplasticizer (float64) has range: 0.00 - 28.20, 0 nan values
water (float64) has range: 140.75 - 247.00, 0 nan values

-> train.csv has 824 rows and 9 columns.
Here is some information about the columns:
age (int64) has range: 1.00 - 365.00, 0 nan values
blast_furnace_slag (float64) has range: 0.00 - 359.40, 0 nan values
cement (float64) has range: 108.30 - 540.00, 0 nan values
coarse_aggregate (float64) has range: 801.00 - 1125.00, 0 nan values
fine_aggregate (float64) has range: 594.00 - 992.60, 0 nan values
fly_ash (float64) has range: 0.00 - 200.10, 0 nan values
strength (float64) has range: 2.33 - 80.20, 0 nan values
superplasticizer (float64) has range: 0.00 - 32.20, 0 nan values
water (float64) has range: 121.75 - 246.90, 0 nan values
