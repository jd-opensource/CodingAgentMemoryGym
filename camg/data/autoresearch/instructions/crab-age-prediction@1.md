# OpenMLE-fast task

Task ID: `crab-age-prediction@1`

Native metric: `CrabAgePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1712 bytes)
- `data/sample_submission.csv` (21221 bytes); columns: ["id", "Age"]
- `data/test.csv` (55403 bytes); columns: ["id", "Sex", "Length", "Diameter", "Height", "Weight", "Shucked Weight", "Viscera Weight", "Shell Weight"]
- `data/train.csv` (229436 bytes); columns: ["id", "Sex", "Length", "Diameter", "Height", "Weight", "Shucked Weight", "Viscera Weight", "Shell Weight", "Age"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (778 lines)
test.csv (778 lines)
train.csv (3117 lines)```

-> sample_submission.csv has 777 rows and 2 columns.
Here is some information about the columns:
Age (float64) has range: 1.22 - 27.22, 0 nan values
id (object) has 777 unique values. Some example values: ['C0003891', 'C0000003', 'C0000007', 'C0000009']

-> test.csv has 777 rows and 9 columns.
Here is some information about the columns:
Diameter (float64) has range: 0.24 - 1.56, 0 nan values
Height (float64) has range: 0.00 - 1.29, 0 nan values
Length (float64) has range: 0.33 - 1.93, 0 nan values
Sex (object) has 3 unique values: ['I', 'F', 'M']
Shell Weight (float64) has range: 0.10 - 25.09, 0 nan values
Shucked Weight (float64) has range: 0.14 - 33.92, 0 nan values
Viscera Weight (float64) has range: 0.13 - 15.99, 0 nan values
Weight (float64) has range: 0.30 - 72.29, 0 nan values
id (object) has 777 unique values. Some example values: ['C0003891', 'C0000003', 'C0000007', 'C0000009']

-> train.csv has 3116 rows and 10 columns.
Here is some information about the columns:
Age (int64) has range: 1.00 - 29.00, 0 nan values
Diameter (float64) has range: 0.14 - 1.62, 0 nan values
Height (float64) has range: 0.00 - 2.83, 0 nan values
Length (float64) has range: 0.19 - 2.04, 0 nan values
Sex (object) has 3 unique values: ['F', 'M', 'I']
Shell Weight (float64) has range: 0.04 - 28.49, 0 nan values
Shucked Weight (float64) has range: 0.03 - 42.18, 0 nan values
Viscera Weight (float64) has range: 0.01 - 21.55, 0 nan values
Weight (float64) has range: 0.06 - 80.10, 0 nan values
id (object) has 3116 unique values. Some example values: ['C0003893', 'C0000001', 'C0000002', 'C0000004']
