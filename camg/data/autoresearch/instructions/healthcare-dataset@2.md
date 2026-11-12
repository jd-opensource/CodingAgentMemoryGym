# OpenMLE-fast task

Task ID: `healthcare-dataset@2`

Native metric: `AdmissionUrgencyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2293 bytes)
- `data/sample_submission.csv` (215014 bytes); columns: ["row_id", "Admission Type"]
- `data/test.csv` (1121670 bytes); columns: ["row_id", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission", "Hospital", "Insurance Provider"]
- `data/train.csv` (3719577 bytes); columns: ["row_id", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission", "Hospital", "Insurance Provider", "Admission Type"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (13876 lines)
test.csv (13876 lines)
train.csv (41626 lines)```

-> sample_submission.csv has 13875 rows and 2 columns.
Here is some information about the columns:
Admission Type (object) has 4 unique values: ['Emergency', 'Urgent', 'Elective', 'Routine']
row_id (int64) has range: 100003.00 - 155496.00, 0 nan values

-> test.csv has 13875 rows and 8 columns.
Here is some information about the columns:
Age (int64) has range: 5.00 - 90.00, 0 nan values
Blood Type (object) has 8 unique values: ['O+', 'A+', 'B-', 'A-', 'B+', 'AB+', 'AB-', 'O-']
Date of Admission (object) has 1825 unique values. Some example values: ['2023-06-23', '2019-06-04', '2021-02-03', '2023-06-27']
Gender (object) has 2 unique values: ['Female', 'Male']
Hospital (object) has 4 unique values: ['UI Health (University of Illinois Hospital)', 'Northwestern Memorial Hospital', 'UChicago Medicine', 'Loyola University Medical Center']
Insurance Provider (object) has 5 unique values: ['Aetna', 'Cigna', 'UnitedHealthcare', 'Blue Cross', 'Medicare']
Medical Condition (object) has 8 unique values: ['Asthma', 'Heart Disease', 'Alzheimer’s', 'Obesity', 'Diabetes', 'Infections', 'Cancer', 'Flu']
row_id (int64) has range: 100003.00 - 155496.00, 0 nan values

-> train.csv has 41625 rows and 9 columns.
Here is some information about the columns:
Admission Type (object) has 4 unique values: ['Emergency', 'Elective', 'Routine', 'Urgent']
Age (int64) has range: 5.00 - 90.00, 0 nan values
Blood Type (object) has 8 unique values: ['AB+', 'B-', 'A+', 'O+', 'O-', 'AB-', 'B+', 'A-']
Date of Admission (object) has 1827 unique values. Some example values: ['2020-10-22', '2020-06-07', '2020-04-03', '2023-08-10']
Gender (object) has 2 unique values: ['Female', 'Male']
Hospital (object) has 4 unique values: ['Northwestern Memorial Hospital', 'UI Health (University of Illinois Hospital)', 'UChicago Medicine', 'Loyola University Medical Center']
Insurance Provider (object) has 5 unique values: ['Blue Cross', 'UnitedHealthcare', 'Medicare', 'Cigna', 'Aetna']
Medical Condition (object) has 8 unique values: ['Infections', 'Flu', 'Cancer', 'Alzheimer’s', 'Heart Disease', 'Asthma', 'Diabetes', 'Obesity']
row_id (int64) has range: 100000.00 - 155499.00, 0 nan values
