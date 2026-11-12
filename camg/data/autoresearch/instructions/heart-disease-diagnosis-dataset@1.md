# OpenMLE-fast task

Task ID: `heart-disease-diagnosis-dataset@1`

Native metric: `HeartDiseaseCostMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2017 bytes)
- `data/sample_submission.csv` (412 bytes); columns: ["id", "heart_disease"]
- `data/test.csv` (3239 bytes); columns: ["id", "age", "sex", "chest_pain_type", "resting_blood_pressure", "serum_cholestoral", "fasting_blood_sugar", "resting_ecg", "max_heart_rate", "exercise_induced_angina", "oldpeak", "st_segment", "major_vessels", "thal"]
- `data/train.csv` (7178 bytes); columns: ["age", "sex", "chest_pain_type", "resting_blood_pressure", "serum_cholestoral", "fasting_blood_sugar", "resting_ecg", "max_heart_rate", "exercise_induced_angina", "oldpeak", "st_segment", "major_vessels", "thal", "heart_disease"]

## Public description

```
description.txt (30 lines)
sample_submission.csv (82 lines)
test.csv (82 lines)
train.csv (190 lines)```

-> sample_submission.csv has 81 rows and 2 columns.
Here is some information about the columns:
heart_disease (int64) has 2 unique values: [1, 2]
id (int64) has range: 0.00 - 80.00, 0 nan values

-> test.csv has 81 rows and 14 columns.
Here is some information about the columns:
age (int64) has range: 29.00 - 70.00, 0 nan values
chest_pain_type (int64) has 4 unique values: [4, 3, 1, 2]
exercise_induced_angina (int64) has 2 unique values: [0, 1]
fasting_blood_sugar (int64) has 2 unique values: [0, 1]
id (int64) has range: 0.00 - 80.00, 0 nan values
major_vessels (int64) has 4 unique values: [3, 1, 2, 0]
max_heart_rate (int64) has range: 88.00 - 202.00, 0 nan values
oldpeak (float64) has range: 0.00 - 6.20, 0 nan values
resting_blood_pressure (int64) has range: 94.00 - 192.00, 0 nan values
resting_ecg (int64) has 2 unique values: [2, 0]
serum_cholestoral (int64) has range: 164.00 - 409.00, 0 nan values
sex (int64) has 2 unique values: [1, 0]
st_segment (int64) has 3 unique values: [2, 1, 3]
thal (int64) has 3 unique values: [3, 6, 7]

-> train.csv has 189 rows and 14 columns.
Here is some information about the columns:
age (int64) has range: 34.00 - 77.00, 0 nan values
chest_pain_type (int64) has 4 unique values: [3, 2, 4, 1]
exercise_induced_angina (int64) has 2 unique values: [0, 1]
fasting_blood_sugar (int64) has 2 unique values: [0, 1]
heart_disease (int64) has 2 unique values: [1, 2]
major_vessels (int64) has 4 unique values: [0, 1, 2, 3]
max_heart_rate (int64) has range: 71.00 - 192.00, 0 nan values
oldpeak (float64) has range: 0.00 - 5.60, 0 nan values
resting_blood_pressure (int64) has range: 100.00 - 200.00, 0 nan values
resting_ecg (int64) has 3 unique values: [2, 0, 1]
serum_cholestoral (int64) has range: 126.00 - 564.00, 0 nan values
sex (int64) has 2 unique values: [0, 1]
st_segment (int64) has 3 unique values: [2, 1, 3]
thal (int64) has 3 unique values: [7, 3, 6]
