# OpenMLE-fast task

Task ID: `heart-disease-statlog@1`

Native metric: `HeartDiseaseStatlogMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1854 bytes)
- `data/sample_submission.csv` (623 bytes); columns: ["id", "target"]
- `data/test.csv` (3199 bytes); columns: ["id", "age", "trestbps", "chol", "thalach", "oldpeak", "sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
- `data/train.csv` (7749 bytes); columns: ["id", "age", "trestbps", "chol", "thalach", "oldpeak", "sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal", "target"]

## Public description

```
description.txt (32 lines)
sample_submission.csv (82 lines)
test.csv (82 lines)
train.csv (190 lines)```

-> sample_submission.csv has 81 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 268.00, 0 nan values
target (float64) has 1 unique values: [0.5]

-> test.csv has 81 rows and 14 columns.
Here is some information about the columns:
age (int64) has range: 29.00 - 77.00, 0 nan values
ca (int64) has 4 unique values: [3, 2, 0, 1]
chol (int64) has range: 126.00 - 354.00, 0 nan values
cp (int64) has 4 unique values: [3, 2, 0, 1]
exang (int64) has 2 unique values: [0, 1]
fbs (int64) has 2 unique values: [0, 1]
id (int64) has range: 0.00 - 268.00, 0 nan values
oldpeak (float64) has range: 0.00 - 6.20, 0 nan values
restecg (int64) has 2 unique values: [2, 0]
sex (int64) has 2 unique values: [1, 0]
slope (int64) has 3 unique values: [1, 0, 2]
thal (int64) has 3 unique values: [1, 3, 2]
thalach (int64) has range: 88.00 - 202.00, 0 nan values
trestbps (int64) has range: 100.00 - 192.00, 0 nan values

-> train.csv has 189 rows and 15 columns.
Here is some information about the columns:
age (int64) has range: 34.00 - 76.00, 0 nan values
ca (int64) has 4 unique values: [0, 1, 3, 2]
chol (int64) has range: 141.00 - 564.00, 0 nan values
cp (int64) has 4 unique values: [2, 1, 3, 0]
exang (int64) has 2 unique values: [0, 1]
fbs (int64) has 2 unique values: [0, 1]
id (int64) has range: 1.00 - 269.00, 0 nan values
oldpeak (float64) has range: 0.00 - 4.20, 0 nan values
restecg (int64) has 3 unique values: [2, 0, 1]
sex (int64) has 2 unique values: [0, 1]
slope (int64) has 3 unique values: [1, 0, 2]
target (int64) has 2 unique values: [0, 1]
thal (int64) has 3 unique values: [3, 1, 2]
thalach (int64) has range: 71.00 - 194.00, 0 nan values
trestbps (int64) has range: 94.00 - 200.00, 0 nan values
