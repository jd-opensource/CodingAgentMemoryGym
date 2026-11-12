# OpenMLE-fast task

Task ID: `obesity-levels@2`

Native metric: `ObesityBMIMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2342 bytes)
- `data/sample_submission.csv` (9699 bytes); columns: ["id", "bmi"]
- `data/test.csv` (42876 bytes); columns: ["id", "Age", "Gender", "family_history_with_overweight", "FAVC", "FCVC", "NCP", "CAEC", "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS"]
- `data/train.csv` (202005 bytes); columns: ["id", "Age", "Gender", "family_history_with_overweight", "FAVC", "FCVC", "NCP", "CAEC", "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS", "bmi"]

## Public description

```
description.txt (56 lines)
sample_submission.csv (424 lines)
test.csv (424 lines)
train.csv (1689 lines)```

-> sample_submission.csv has 423 rows and 2 columns.
Here is some information about the columns:
bmi (float64) has range: 15.48 - 48.75, 0 nan values
id (int64) has range: 0.00 - 2110.00, 0 nan values

-> test.csv has 423 rows and 15 columns.
Here is some information about the columns:
Age (float64) has range: 16.00 - 55.25, 0 nan values
CAEC (object) has 4 unique values: ['Sometimes', 'Frequently', 'Always', 'no']
CALC (object) has 3 unique values: ['no', 'Sometimes', 'Frequently']
CH2O (float64) has range: 1.00 - 3.00, 0 nan values
FAF (float64) has range: 0.00 - 3.00, 0 nan values
FAVC (object) has 2 unique values: ['no', 'yes']
FCVC (float64) has range: 1.00 - 3.00, 0 nan values
Gender (object) has 2 unique values: ['Female', 'Male']
MTRANS (object) has 5 unique values: ['Public_Transportation', 'Walking', 'Motorbike', 'Automobile', 'Bike']
NCP (float64) has range: 1.00 - 4.00, 0 nan values
SCC (object) has 2 unique values: ['no', 'yes']
SMOKE (object) has 2 unique values: ['no', 'yes']
TUE (float64) has range: 0.00 - 2.00, 0 nan values
family_history_with_overweight (object) has 2 unique values: ['yes', 'no']
id (int64) has range: 0.00 - 2110.00, 0 nan values

-> train.csv has 1688 rows and 16 columns.
Here is some information about the columns:
Age (float64) has range: 14.00 - 61.00, 0 nan values
CAEC (object) has 4 unique values: ['Sometimes', 'Frequently', 'Always', 'no']
CALC (object) has 4 unique values: ['Frequently', 'Sometimes', 'no', 'Always']
CH2O (float64) has range: 1.00 - 3.00, 0 nan values
FAF (float64) has range: 0.00 - 3.00, 0 nan values
FAVC (object) has 2 unique values: ['no', 'yes']
FCVC (float64) has range: 1.00 - 3.00, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
MTRANS (object) has 5 unique values: ['Public_Transportation', 'Automobile', 'Walking', 'Bike', 'Motorbike']
NCP (float64) has range: 1.00 - 4.00, 0 nan values
SCC (object) has 2 unique values: ['no', 'yes']
SMOKE (object) has 2 unique values: ['no', 'yes']
TUE (float64) has range: 0.00 - 2.00, 0 nan values
bmi (float64) has range: 13.00 - 50.01, 0 nan values
family_history_with_overweight (object) has 2 unique values: ['yes', 'no']
id (int64) has range: 2.00 - 2109.00, 0 nan values
