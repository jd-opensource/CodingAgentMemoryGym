# OpenMLE-fast task

Task ID: `bike-buyers@1`

Native metric: `BikeBuyersMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2215 bytes)
- `data/sample_submission.csv` (4820 bytes); columns: ["Purchased Bike"]
- `data/test.csv` (19359 bytes); columns: ["Marital Status", "Gender", "Income", "Children", "Education", "Occupation", "Home Owner", "Cars", "Commute Distance", "Region", "Age"]
- `data/train.csv` (66018 bytes); columns: ["Marital Status", "Gender", "Income", "Children", "Education", "Occupation", "Home Owner", "Cars", "Commute Distance", "Region", "Age", "Purchased Bike"]

## Public description

```
description.txt (35 lines)
sample_submission.csv (251 lines)
test.csv (251 lines)
train.csv (751 lines)```

-> sample_submission.csv has 250 rows and 1 columns.
Here is some information about the columns:
Purchased Bike (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 250 rows and 11 columns.
Here is some information about the columns:
Age (int64) has range: 26.00 - 74.00, 0 nan values
Cars (int64) has 5 unique values: [2, 1, 4, 3, 0]
Children (int64) has 6 unique values: [2, 4, 1, 5, 0, 3]
Commute Distance (object) has 5 unique values: ['5-10 Miles', '0-1 Miles', '10+ Miles', '2-5 Miles', '1-2 Miles']
Education (object) has 5 unique values: ['Partial College', 'Bachelors', 'High School', 'Graduate Degree', 'Partial High School']
Gender (object) has 2 unique values: ['Female', 'Male']
Home Owner (object) has 2 unique values: ['No', 'Yes']
Income (int64) has range: 10000.00 - 170000.00, 0 nan values
Marital Status (object) has 2 unique values: ['Single', 'Married']
Occupation (object) has 5 unique values: ['Clerical', 'Management', 'Professional', 'Manual', 'Skilled Manual']
Region (object) has 3 unique values: ['Pacific', 'North America', 'Europe']

-> train.csv has 750 rows and 12 columns.
Here is some information about the columns:
Age (float64) has range: 25.00 - 89.00, 7 nan values
Cars (float64) has 5 unique values: [0.0, 2.0, 1.0, 3.0, nan, 4.0]
Children (float64) has 6 unique values: [2.0, 3.0, 5.0, 0.0, 4.0, 1.0, nan]
Commute Distance (object) has 5 unique values: ['1-2 Miles', '5-10 Miles', '2-5 Miles', '0-1 Miles', '10+ Miles']
Education (object) has 5 unique values: ['Bachelors', 'High School', 'Partial College', 'Graduate Degree', 'Partial High School']
Gender (object) has 2 unique values: ['Male', 'Female', nan]
Home Owner (object) has 2 unique values: ['Yes', 'No', nan]
Income (float64) has range: 10000.00 - 170000.00, 5 nan values
Marital Status (object) has 2 unique values: ['Married', 'Single', nan]
Occupation (object) has 5 unique values: ['Professional', 'Skilled Manual', 'Management', 'Clerical', 'Manual']
Purchased Bike (object) has 2 unique values: ['Yes', 'No']
Region (object) has 3 unique values: ['Pacific', 'North America', 'Europe']
