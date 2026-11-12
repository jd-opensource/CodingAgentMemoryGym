# OpenMLE-fast task

Task ID: `pima-indians-diabetes-database@1`

Native metric: `PimaIndiansDiabetesMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1406 bytes)
- `data/sample_submission.csv` (4456 bytes); columns: ["Outcome"]
- `data/test.csv` (6601 bytes); columns: ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
- `data/train.csv` (16316 bytes); columns: ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]

## Public description

```
description.txt (33 lines)
sample_submission.csv (232 lines)
test.csv (232 lines)
train.csv (538 lines)```

-> sample_submission.csv has 231 rows and 1 columns.
Here is some information about the columns:
Outcome (float64) has range: 0.01 - 0.99, 0 nan values

-> test.csv has 231 rows and 8 columns.
Here is some information about the columns:
Age (int64) has range: 21.00 - 69.00, 0 nan values
BMI (float64) has range: 0.00 - 59.40, 0 nan values
BloodPressure (int64) has range: 0.00 - 110.00, 0 nan values
DiabetesPedigreeFunction (float64) has range: 0.08 - 2.42, 0 nan values
Glucose (int64) has range: 0.00 - 199.00, 0 nan values
Insulin (int64) has range: 0.00 - 846.00, 0 nan values
Pregnancies (int64) has range: 0.00 - 15.00, 0 nan values
SkinThickness (int64) has range: 0.00 - 99.00, 0 nan values

-> train.csv has 537 rows and 9 columns.
Here is some information about the columns:
Age (int64) has range: 21.00 - 81.00, 0 nan values
BMI (float64) has range: 0.00 - 67.10, 0 nan values
BloodPressure (int64) has range: 0.00 - 122.00, 0 nan values
DiabetesPedigreeFunction (float64) has range: 0.08 - 2.33, 0 nan values
Glucose (int64) has range: 0.00 - 198.00, 0 nan values
Insulin (int64) has range: 0.00 - 744.00, 0 nan values
Outcome (int64) has 2 unique values: [1, 0]
Pregnancies (int64) has range: 0.00 - 17.00, 0 nan values
SkinThickness (int64) has range: 0.00 - 60.00, 0 nan values
