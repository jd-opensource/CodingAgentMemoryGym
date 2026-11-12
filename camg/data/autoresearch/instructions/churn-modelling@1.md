# OpenMLE-fast task

Task ID: `churn-modelling@1`

Native metric: `BankChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2162 bytes)
- `data/sample_submission.csv` (56494 bytes); columns: ["CustomerId", "Exited"]
- `data/test.csv` (132663 bytes); columns: ["RowNumber", "CustomerId", "Surname", "CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
- `data/train.csv` (545944 bytes); columns: ["RowNumber", "CustomerId", "Surname", "CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]

## Public description

```
description.txt (35 lines)
sample_submission.csv (2001 lines)
test.csv (2001 lines)
train.csv (8001 lines)```

-> sample_submission.csv has 2000 rows and 2 columns.
Here is some information about the columns:
CustomerId (int64) has range: 15565779.00 - 15815645.00, 0 nan values
Exited (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 2000 rows and 13 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 85.00, 0 nan values
Balance (float64) has range: 0.00 - 250898.09, 0 nan values
CreditScore (int64) has range: 365.00 - 850.00, 0 nan values
CustomerId (int64) has range: 15565779.00 - 15815645.00, 0 nan values
EstimatedSalary (float64) has range: 90.07 - 199929.17, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Geography (object) has 3 unique values: ['Germany', 'Spain', 'France']
HasCrCard (int64) has 2 unique values: [1, 0]
IsActiveMember (int64) has 2 unique values: [1, 0]
NumOfProducts (int64) has 4 unique values: [1, 2, 4, 3]
RowNumber (int64) has range: 10.00 - 9998.00, 0 nan values
Surname (object) has 1153 unique values. Some example values: ['Wei', 'Thompson', 'Hughes', 'McGregor']
Tenure (int64) has range: 0.00 - 10.00, 0 nan values

-> train.csv has 8000 rows and 14 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 92.00, 0 nan values
Balance (float64) has range: 0.00 - 238387.56, 0 nan values
CreditScore (int64) has range: 350.00 - 850.00, 0 nan values
CustomerId (int64) has range: 15565701.00 - 15815690.00, 0 nan values
EstimatedSalary (float64) has range: 11.58 - 199992.48, 0 nan values
Exited (int64) has 2 unique values: [0, 1]
Gender (object) has 2 unique values: ['Male', 'Female']
Geography (object) has 3 unique values: ['France', 'Germany', 'Spain']
HasCrCard (int64) has 2 unique values: [0, 1]
IsActiveMember (int64) has 2 unique values: [0, 1]
NumOfProducts (int64) has 4 unique values: [2, 1, 3, 4]
RowNumber (int64) has range: 1.00 - 10000.00, 0 nan values
Surname (object) has 2615 unique values. Some example values: ['Smith', 'Scott', 'Martin', 'Chu']
Tenure (int64) has range: 0.00 - 10.00, 0 nan values
