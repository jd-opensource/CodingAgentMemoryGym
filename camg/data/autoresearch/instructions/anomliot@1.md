# OpenMLE-fast task

Task ID: `anomliot@1`

Native metric: `AnoMLIoTMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1153 bytes)
- `data/sample_submission.csv` (59977 bytes); columns: ["id", "is_anomaly"]
- `data/test.csv` (60677 bytes); columns: ["Time", "Temperature", "Humidity", "Light", "Loudness"]
- `data/train.csv` (150581 bytes); columns: ["Time", "Temperature", "Humidity", "Light", "Loudness", "is_anomaly"]

## Public description

```
description.txt (36 lines)
sample_submission.csv (1969 lines)
test.csv (1969 lines)
train.csv (4591 lines)```

-> sample_submission.csv has 1968 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1623827206.00 - 1623846876.00, 0 nan values
is_anomaly (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 1968 rows and 5 columns.
Here is some information about the columns:
Humidity (float64) has range: 1.94 - 67.44, 0 nan values
Light (int64) has range: 626.00 - 675.00, 0 nan values
Loudness (int64) has range: 40.00 - 362.00, 0 nan values
Temperature (float64) has range: 22.75 - 72.28, 0 nan values
Time (int64) has range: 1623827206.00 - 1623846876.00, 0 nan values

-> train.csv has 4590 rows and 6 columns.
Here is some information about the columns:
Humidity (float64) has range: 28.38 - 71.81, 0 nan values
Light (int64) has range: 625.00 - 646.00, 0 nan values
Loudness (int64) has range: 31.00 - 498.00, 0 nan values
Temperature (float64) has range: 22.19 - 38.16, 0 nan values
Time (int64) has range: 1623781306.00 - 1623827196.00, 0 nan values
is_anomaly (int64) has 2 unique values: [1, 0]
