# OpenMLE-fast task

Task ID: `shopping-mall-customer-segmentation-data@1`

Native metric: `SpendingScoreRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1517 bytes)
- `data/sample_submission.csv` (126438 bytes); columns: ["id", "spending_score"]
- `data/test.csv` (170230 bytes); columns: ["id", "age", "gender", "annual_income"]
- `data/train.csv` (741862 bytes); columns: ["id", "age", "gender", "annual_income", "spending_score"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (3011 lines)
test.csv (3011 lines)
train.csv (12070 lines)```

-> sample_submission.csv has 3010 rows and 2 columns.
Here is some information about the columns:
id (object) has 3010 unique values. Some example values: ['5f388cbe-3373-4e16-b743-38f508f2249f', '7e211337-e92f-4140-8231-5c9ac7a2aa12', 'ebd23e4a-a9b2-4bb3-a855-e78508f4b6a0', 'cd68544f-d3c3-4cb8-9b2c-6ebfdfa5b326']
spending_score (float64) has 1 unique values: [50.0]

-> test.csv has 3010 rows and 4 columns.
Here is some information about the columns:
age (float64) has range: 18.00 - 90.00, 0 nan values
annual_income (float64) has range: 20089.00 - 199929.00, 0 nan values
gender (object) has 2 unique values: ['Male', 'Female']
id (object) has 3010 unique values. Some example values: ['5f388cbe-3373-4e16-b743-38f508f2249f', '7e211337-e92f-4140-8231-5c9ac7a2aa12', 'ebd23e4a-a9b2-4bb3-a855-e78508f4b6a0', 'cd68544f-d3c3-4cb8-9b2c-6ebfdfa5b326']

-> train.csv has 12069 rows and 5 columns.
Here is some information about the columns:
age (float64) has range: 18.00 - 90.00, 0 nan values
annual_income (float64) has range: 20022.00 - 199974.00, 0 nan values
gender (object) has 2 unique values: ['Male', 'Female']
id (object) has 12069 unique values. Some example values: ['b8b8f561-ebca-4401-8afe-544c906554ba', 'd410ea53-6661-42a9-ad3a-f554b05fd2a7', '1770b26f-493f-46b6-837f-4237fb5a314e', 'e81aa8eb-1767-4b77-87ce-1620dc732c5e']
spending_score (float64) has range: 1.00 - 100.00, 0 nan values
