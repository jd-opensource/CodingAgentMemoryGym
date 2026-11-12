# OpenMLE-fast task

Task ID: `500-person-gender-height-weight-bodymassindex@1`

Native metric: `BodyWeightRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (908 bytes)
- `data/sample_submission.csv` (2604 bytes); columns: ["row_id", "Weight"]
- `data/test.csv` (1923 bytes); columns: ["row_id", "Gender", "Height"]
- `data/train.csv` (9855 bytes); columns: ["row_id", "Gender", "Height", "Weight"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (101 lines)
test.csv (101 lines)
train.csv (401 lines)```

-> sample_submission.csv has 100 rows and 2 columns.
Here is some information about the columns:
Weight (float64) has range: 102.49 - 108.02, 0 nan values
row_id (int64) has range: 100007.00 - 100499.00, 0 nan values

-> test.csv has 100 rows and 3 columns.
Here is some information about the columns:
Gender (object) has 2 unique values: ['Male', 'Female']
Height (float64) has range: 140.00 - 199.00, 0 nan values
row_id (int64) has range: 100007.00 - 100499.00, 0 nan values

-> train.csv has 400 rows and 4 columns.
Here is some information about the columns:
Gender (object) has 2 unique values: ['Male', 'Female']
Height (float64) has range: 140.00 - 199.00, 0 nan values
Weight (float64) has range: 50.00 - 160.00, 0 nan values
row_id (int64) has range: 100000.00 - 100497.00, 0 nan values
