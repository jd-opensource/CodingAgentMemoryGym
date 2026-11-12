# OpenMLE-fast task

Task ID: `sf-salaries@1`

Native metric: `SFSalariesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1199 bytes)
- `data/sample_submission.csv` (970401 bytes); columns: ["Id", "TotalPayBenefits"]
- `data/test.csv` (1745713 bytes); columns: ["Id", "JobTitle", "Year", "Agency"]
- `data/train.csv` (6027235 bytes); columns: ["Id", "JobTitle", "Year", "Agency", "TotalPayBenefits"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (38123 lines)
test.csv (38123 lines)
train.csv (110529 lines)```

-> sample_submission.csv has 38122 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 110532.00 - 148653.00, 0 nan values
TotalPayBenefits (float64) has range: 183.76 - 323835.26, 0 nan values

-> test.csv has 38122 rows and 4 columns.
Here is some information about the columns:
Agency (object) has 1 unique values: ['San Francisco']
Id (int64) has range: 110532.00 - 148653.00, 0 nan values
JobTitle (object) has 997 unique values. Some example values: ['Transit Operator', 'Special Nurse', 'Registered Nurse', 'Public Svc Aide-Public Works']
Year (int64) has 1 unique values: [2014]

-> train.csv has 110528 rows and 5 columns.
Here is some information about the columns:
Agency (object) has 1 unique values: ['San Francisco']
Id (int64) has range: 1.00 - 110528.00, 0 nan values
JobTitle (object) has 2123 unique values. Some example values: ['Transit Operator', 'Special Nurse', 'Registered Nurse', 'TRANSIT OPERATOR']
TotalPayBenefits (float64) has range: 0.00 - 567595.43, 0 nan values
Year (int64) has 3 unique values: [2011, 2012, 2013]
