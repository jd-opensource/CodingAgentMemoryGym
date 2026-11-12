# OpenMLE-fast task

Task ID: `ataque-cardaco@1`

Native metric: `AMITriageRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1302 bytes)
- `data/sample_submission.csv` (9290 bytes); columns: ["Id", "Result"]
- `data/test.csv` (9943 bytes); columns: ["Age", "Gender", "Heart rate", "Systolic blood pressure", "Diastolic blood pressure", "Blood sugar", "Id"]
- `data/train.csv` (21050 bytes); columns: ["Age", "Gender", "Heart rate", "Systolic blood pressure", "Diastolic blood pressure", "Blood sugar", "Result"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (397 lines)
test.csv (397 lines)
train.csv (924 lines)```

-> sample_submission.csv has 396 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 2.00 - 1319.00, 0 nan values
Result (float64) has range: 0.01 - 0.99, 0 nan values

-> test.csv has 396 rows and 7 columns.
Here is some information about the columns:
Age (int64) has range: 20.00 - 103.00, 0 nan values
Blood sugar (float64) has range: 35.00 - 431.00, 0 nan values
Diastolic blood pressure (int64) has range: 42.00 - 118.00, 0 nan values
Gender (int64) has 2 unique values: [1, 0]
Heart rate (int64) has range: 40.00 - 1111.00, 0 nan values
Id (int64) has range: 2.00 - 1319.00, 0 nan values
Systolic blood pressure (int64) has range: 42.00 - 223.00, 0 nan values

-> train.csv has 923 rows and 7 columns.
Here is some information about the columns:
Age (int64) has range: 14.00 - 103.00, 0 nan values
Blood sugar (float64) has range: 60.00 - 541.00, 0 nan values
Diastolic blood pressure (int64) has range: 38.00 - 154.00, 0 nan values
Gender (int64) has 2 unique values: [1, 0]
Heart rate (int64) has range: 20.00 - 1111.00, 0 nan values
Result (int64) has 2 unique values: [0, 1]
Systolic blood pressure (int64) has range: 65.00 - 223.00, 0 nan values
