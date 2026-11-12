# OpenMLE-fast task

Task ID: `framingham-heart-study@2`

Native metric: `FraminghamCHDRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2268 bytes)
- `data/sample_submission.csv` (11542 bytes); columns: ["Id", "TenYearCHD"]
- `data/test.csv` (53142 bytes); columns: ["Id", "male", "age", "education", "currentSmoker", "cigsPerDay", "BPMeds", "prevalentStroke", "prevalentHyp", "diabetes", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose"]
- `data/train.csv` (219536 bytes); columns: ["Id", "male", "age", "education", "currentSmoker", "cigsPerDay", "BPMeds", "prevalentStroke", "prevalentHyp", "diabetes", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose", "TenYearCHD"]

## Public description

```
description.txt (36 lines)
sample_submission.csv (849 lines)
test.csv (849 lines)
train.csv (3393 lines)```

-> sample_submission.csv has 848 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 1.00 - 4238.00, 0 nan values
TenYearCHD (float64) has range: 0.01 - 0.99, 0 nan values

-> test.csv has 848 rows and 16 columns.
Here is some information about the columns:
BMI (float64) has range: 15.96 - 45.79, 3 nan values
BPMeds (float64) has 2 unique values: [0.0, 1.0, nan]
Id (int64) has range: 1.00 - 4238.00, 0 nan values
age (int64) has range: 32.00 - 69.00, 0 nan values
cigsPerDay (float64) has range: 0.00 - 70.00, 7 nan values
currentSmoker (int64) has 2 unique values: [1, 0]
diaBP (float64) has range: 48.00 - 124.00, 0 nan values
diabetes (int64) has 2 unique values: [0, 1]
education (float64) has 4 unique values: [2.0, 1.0, 4.0, 3.0, nan]
glucose (float64) has range: 43.00 - 394.00, 91 nan values
heartRate (float64) has range: 48.00 - 120.00, 0 nan values
male (int64) has 2 unique values: [0, 1]
prevalentHyp (int64) has 2 unique values: [0, 1]
prevalentStroke (int64) has 2 unique values: [0, 1]
sysBP (float64) has range: 92.00 - 235.00, 0 nan values
totChol (float64) has range: 133.00 - 385.00, 12 nan values

-> train.csv has 3392 rows and 17 columns.
Here is some information about the columns:
BMI (float64) has range: 15.54 - 56.80, 16 nan values
BPMeds (float64) has 2 unique values: [0.0, 1.0, nan]
Id (int64) has range: 2.00 - 4240.00, 0 nan values
TenYearCHD (int64) has 2 unique values: [0, 1]
age (int64) has range: 33.00 - 70.00, 0 nan values
cigsPerDay (float64) has range: 0.00 - 60.00, 22 nan values
currentSmoker (int64) has 2 unique values: [1, 0]
diaBP (float64) has range: 51.00 - 142.50, 0 nan values
diabetes (int64) has 2 unique values: [0, 1]
education (float64) has 4 unique values: [2.0, 3.0, 1.0, 4.0, nan]
glucose (float64) has range: 40.00 - 394.00, 297 nan values
heartRate (float64) has range: 44.00 - 143.00, 1 nan values
male (int64) has 2 unique values: [0, 1]
prevalentHyp (int64) has 2 unique values: [0, 1]
prevalentStroke (int64) has 2 unique values: [0, 1]
sysBP (float64) has range: 83.50 - 295.00, 0 nan values
totChol (float64) has range: 107.00 - 696.00, 38 nan values
