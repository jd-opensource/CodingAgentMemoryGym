# OpenMLE-fast task

Task ID: `absenteeism-dataset@1`

Native metric: `AbsenteeismRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2319 bytes)
- `data/sample_submission.csv` (22115 bytes); columns: ["EmployeeNumber", "AbsentHours"]
- `data/test.csv` (214736 bytes); columns: ["EmployeeNumber", "Gender", "City", "JobTitle", "DepartmentName", "StoreLocation", "Division", "Age", "LengthService", "BusinessUnit"]
- `data/train.csv` (565741 bytes); columns: ["EmployeeNumber", "Gender", "City", "JobTitle", "DepartmentName", "StoreLocation", "Division", "Age", "LengthService", "AbsentHours", "BusinessUnit"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (2493 lines)
test.csv (2493 lines)
train.csv (5845 lines)```

-> sample_submission.csv has 2492 rows and 2 columns.
Here is some information about the columns:
AbsentHours (float64) has 1 unique values: [0.0]
EmployeeNumber (int64) has range: 1.00 - 8335.00, 0 nan values

-> test.csv has 2492 rows and 10 columns.
Here is some information about the columns:
Age (float64) has range: 3.50 - 77.00, 0 nan values
BusinessUnit (object) has 2 unique values: ['Stores', 'HeadOffice']
City (object) has 226 unique values. Some example values: ['Vancouver', 'Victoria', 'New Westminster', 'Burnaby']
DepartmentName (object) has 20 unique values. Some example values: ['Customer Service', 'Bakery', 'Dairy', 'Meats']
Division (object) has 5 unique values: ['Stores', 'FinanceAndAccounting', 'HumanResources', 'InfoTech', 'Executive']
EmployeeNumber (int64) has range: 1.00 - 8335.00, 0 nan values
Gender (object) has 2 unique values: ['F', 'M']
JobTitle (object) has 25 unique values. Some example values: ['Cashier', 'Dairy Person', 'Baker', 'Meat Cutter']
LengthService (float64) has range: 0.05 - 43.74, 0 nan values
StoreLocation (object) has 39 unique values. Some example values: ['Vancouver', 'Victoria', 'New Westminster', 'Nanaimo']

-> train.csv has 5844 rows and 11 columns.
Here is some information about the columns:
AbsentHours (float64) has range: 0.00 - 272.53, 0 nan values
Age (float64) has range: 8.12 - 77.94, 0 nan values
BusinessUnit (object) has 2 unique values: ['Stores', 'HeadOffice']
City (object) has 243 unique values. Some example values: ['Vancouver', 'Victoria', 'New Westminster', 'Burnaby']
DepartmentName (object) has 21 unique values. Some example values: ['Customer Service', 'Meats', 'Dairy', 'Bakery']
Division (object) has 6 unique values: ['Stores', 'FinanceAndAccounting', 'HumanResources', 'InfoTech', 'Executive', 'Legal']
EmployeeNumber (int64) has range: 2.00 - 8336.00, 0 nan values
Gender (object) has 2 unique values: ['M', 'F']
JobTitle (object) has 47 unique values. Some example values: ['Cashier', 'Dairy Person', 'Meat Cutter', 'Baker']
LengthService (float64) has range: 0.01 - 39.45, 0 nan values
StoreLocation (object) has 40 unique values. Some example values: ['Vancouver', 'Victoria', 'Nanaimo', 'New Westminster']
