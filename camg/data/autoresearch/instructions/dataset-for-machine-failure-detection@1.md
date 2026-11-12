# OpenMLE-fast task

Task ID: `dataset-for-machine-failure-detection@1`

Native metric: `MachineFailureRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1105 bytes)
- `data/sample_submission.csv` (4839 bytes); columns: ["Failure_Risk"]
- `data/test.csv` (13364 bytes); columns: ["Temperature", "Vibration", "Power_Usage", "Humidity", "Machine_Type"]
- `data/train.csv` (41495 bytes); columns: ["Temperature", "Vibration", "Power_Usage", "Humidity", "Machine_Type", "Failure_Risk"]

## Public description

```
description.txt (35 lines)
sample_submission.csv (251 lines)
test.csv (251 lines)
train.csv (751 lines)```

-> sample_submission.csv has 250 rows and 1 columns.
Here is some information about the columns:
Failure_Risk (float64) has range: 0.01 - 0.99, 0 nan values

-> test.csv has 250 rows and 5 columns.
Here is some information about the columns:
Humidity (float64) has range: 17.53 - 41.60, 0 nan values
Machine_Type (object) has 3 unique values: ['Lathe', 'Mill', 'Drill']
Power_Usage (float64) has range: 4.02 - 15.97, 0 nan values
Temperature (float64) has range: 37.59 - 95.73, 0 nan values
Vibration (float64) has range: 35.64 - 62.90, 0 nan values

-> train.csv has 750 rows and 6 columns.
Here is some information about the columns:
Failure_Risk (int64) has 2 unique values: [0, 1]
Humidity (float64) has range: 15.35 - 46.22, 0 nan values
Machine_Type (object) has 3 unique values: ['Lathe', 'Mill', 'Drill']
Power_Usage (float64) has range: 3.96 - 17.85, 0 nan values
Temperature (float64) has range: 43.49 - 108.53, 0 nan values
Vibration (float64) has range: 35.30 - 65.97, 0 nan values
