# OpenMLE-fast task

Task ID: `obesity-or-cvd-risk-classifyregressorcluster@1`

Native metric: `ObesityRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2779 bytes)
- `data/sample_submission.csv` (11510 bytes); columns: ["Id", "NObeyesdad"]
- `data/test.csv` (44942 bytes); columns: ["Id", "Gender", "Age", "family_history_with_overweight", "FAVC", "FCVC", "NCP", "CAEC", "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS"]
- `data/train.csv` (209516 bytes); columns: ["Id", "Gender", "Age", "family_history_with_overweight", "FAVC", "FCVC", "NCP", "CAEC", "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS", "NObeyesdad"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (424 lines)
test.csv (424 lines)
train.csv (1689 lines)```

-> sample_submission.csv has 423 rows and 2 columns.
Here is some information about the columns:
Id (object) has 423 unique values. Some example values: ['ID_001397', 'ID_000573', 'ID_000371', 'ID_001003']
NObeyesdad (object) has 7 unique values: ['Obesity_Type_I', 'Normal_Weight', 'Obesity_Type_III', 'Obesity_Type_II', 'Insufficient_Weight', 'Overweight_Level_I', 'Overweight_Level_II']

-> test.csv has 423 rows and 15 columns.
Here is some information about the columns:
Age (float64) has range: 14.00 - 55.00, 0 nan values
CAEC (object) has 4 unique values: ['Sometimes', 'Frequently', 'no', 'Always']
CALC (object) has 3 unique values: ['Sometimes', 'no', 'Frequently']
CH2O (float64) has range: 1.00 - 3.00, 0 nan values
FAF (float64) has range: 0.00 - 3.00, 0 nan values
FAVC (object) has 2 unique values: ['yes', 'no']
FCVC (float64) has range: 1.00 - 3.00, 0 nan values
Gender (object) has 2 unique values: ['Female', 'Male']
Id (object) has 423 unique values. Some example values: ['ID_001397', 'ID_000573', 'ID_000371', 'ID_001003']
MTRANS (object) has 5 unique values: ['Public_Transportation', 'Automobile', 'Walking', 'Motorbike', 'Bike']
NCP (float64) has range: 1.00 - 4.00, 0 nan values
SCC (object) has 2 unique values: ['no', 'yes']
SMOKE (object) has 2 unique values: ['no', 'yes']
TUE (float64) has range: 0.00 - 2.00, 0 nan values
family_history_with_overweight (object) has 2 unique values: ['no', 'yes']

-> train.csv has 1688 rows and 16 columns.
Here is some information about the columns:
Age (float64) has range: 15.00 - 61.00, 0 nan values
CAEC (object) has 4 unique values: ['Frequently', 'Sometimes', 'Always', 'no']
CALC (object) has 4 unique values: ['Frequently', 'no', 'Sometimes', 'Always']
CH2O (float64) has range: 1.00 - 3.00, 0 nan values
FAF (float64) has range: 0.00 - 3.00, 0 nan values
FAVC (object) has 2 unique values: ['yes', 'no']
FCVC (float64) has range: 1.00 - 3.00, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Id (object) has 1688 unique values. Some example values: ['ID_000479', 'ID_000460', 'ID_000427', 'ID_000327']
MTRANS (object) has 5 unique values: ['Public_Transportation', 'Automobile', 'Walking', 'Bike', 'Motorbike']
NCP (float64) has range: 1.00 - 4.00, 0 nan values
NObeyesdad (object) has 7 unique values: ['Overweight_Level_I', 'Normal_Weight', 'Overweight_Level_II', 'Insufficient_Weight', 'Obesity_Type_II', 'Obesity_Type_III', 'Obesity_Type_I']
SCC (object) has 2 unique values: ['no', 'yes']
SMOKE (object) has 2 unique values: ['no', 'yes']
TUE (float64) has range: 0.00 - 2.00, 0 nan values
family_history_with_overweight (object) has 2 unique values: ['yes', 'no']
