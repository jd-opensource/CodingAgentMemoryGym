# OpenMLE-fast task

Task ID: `diabetes-classification-dataset@1`

Native metric: `DiabetesClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1562 bytes)
- `data/sample_submission.csv` (24749 bytes); columns: ["Id", "Diagnosis"]
- `data/test.csv` (43393 bytes); columns: ["Id", "Age", "Gender", "BMI", "Chol", "TG", "HDL", "LDL", "Cr", "BUN"]
- `data/train.csv` (180432 bytes); columns: ["Id", "Age", "Gender", "BMI", "Chol", "TG", "HDL", "LDL", "Cr", "BUN", "Diagnosis"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (1028 lines)
test.csv (1028 lines)
train.csv (4106 lines)```

-> sample_submission.csv has 1027 rows and 2 columns.
Here is some information about the columns:
Diagnosis (float64) has range: 0.00 - 1.00, 0 nan values
Id (int64) has range: 1.00 - 5130.00, 0 nan values

-> test.csv has 1027 rows and 10 columns.
Here is some information about the columns:
Age (int64) has range: 20.00 - 91.00, 0 nan values
BMI (int64) has range: 16.00 - 39.00, 0 nan values
BUN (float64) has range: 2.00 - 38.90, 0 nan values
Chol (float64) has range: 2.00 - 9.70, 0 nan values
Cr (float64) has range: 4.86 - 800.00, 0 nan values
Gender (object) has 2 unique values: ['M', 'F']
HDL (float64) has range: 0.00 - 9.90, 0 nan values
Id (int64) has range: 1.00 - 5130.00, 0 nan values
LDL (float64) has range: 0.60 - 5.60, 0 nan values
TG (float64) has range: 0.00 - 13.80, 0 nan values

-> train.csv has 4105 rows and 11 columns.
Here is some information about the columns:
Age (int64) has range: 23.00 - 93.00, 0 nan values
BMI (int64) has range: 15.00 - 47.00, 0 nan values
BUN (float64) has range: 0.50 - 26.40, 0 nan values
Chol (float64) has range: 0.00 - 11.65, 0 nan values
Cr (float64) has range: 4.86 - 800.00, 0 nan values
Diagnosis (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['F', 'M']
HDL (float64) has range: 0.00 - 6.60, 0 nan values
Id (int64) has range: 0.00 - 5131.00, 0 nan values
LDL (float64) has range: 0.30 - 9.90, 0 nan values
TG (float64) has range: 0.00 - 32.64, 0 nan values
