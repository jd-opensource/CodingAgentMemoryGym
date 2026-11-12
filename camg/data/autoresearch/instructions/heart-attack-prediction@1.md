# OpenMLE-fast task

Task ID: `heart-attack-prediction@1`

Native metric: `HeartAttackRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1893 bytes)
- `data/sample_submission.csv` (4715 bytes); columns: ["id", "target"]
- `data/test.csv` (8000 bytes); columns: ["id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
- `data/train.csv` (36023 bytes); columns: ["id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]

## Public description

```
description.txt (59 lines)
sample_submission.csv (205 lines)
test.csv (205 lines)
train.csv (822 lines)```

-> sample_submission.csv has 204 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 3.00 - 1024.00, 0 nan values
target (float64) has range: 0.11 - 0.90, 0 nan values

-> test.csv has 204 rows and 14 columns.
Here is some information about the columns:
age (int64) has range: 35.00 - 71.00, 0 nan values
ca (int64) has 5 unique values: [1, 3, 0, 2, 4]
chol (int64) has range: 131.00 - 417.00, 0 nan values
cp (int64) has 4 unique values: [0, 2, 1, 3]
exang (int64) has 2 unique values: [0, 1]
fbs (int64) has 2 unique values: [0, 1]
id (int64) has range: 3.00 - 1024.00, 0 nan values
oldpeak (float64) has range: 0.00 - 4.40, 0 nan values
restecg (int64) has 3 unique values: [1, 2, 0]
sex (int64) has 2 unique values: [1, 0]
slope (int64) has 3 unique values: [2, 0, 1]
thal (int64) has 3 unique values: [3, 1, 2]
thalach (int64) has range: 71.00 - 195.00, 0 nan values
trestbps (int64) has range: 94.00 - 200.00, 0 nan values

-> train.csv has 821 rows and 15 columns.
Here is some information about the columns:
age (int64) has range: 29.00 - 77.00, 0 nan values
ca (int64) has 5 unique values: [2, 0, 3, 1, 4]
chol (int64) has range: 126.00 - 564.00, 0 nan values
cp (int64) has 4 unique values: [0, 1, 2, 3]
exang (int64) has 2 unique values: [0, 1]
fbs (int64) has 2 unique values: [0, 1]
id (int64) has range: 0.00 - 1023.00, 0 nan values
oldpeak (float64) has range: 0.00 - 6.20, 0 nan values
restecg (int64) has 3 unique values: [1, 0, 2]
sex (int64) has 2 unique values: [1, 0]
slope (int64) has 3 unique values: [2, 0, 1]
target (float64) has range: 0.10 - 0.90, 0 nan values
thal (int64) has 4 unique values: [3, 2, 0, 1]
thalach (int64) has range: 71.00 - 202.00, 0 nan values
trestbps (int64) has range: 94.00 - 200.00, 0 nan values
