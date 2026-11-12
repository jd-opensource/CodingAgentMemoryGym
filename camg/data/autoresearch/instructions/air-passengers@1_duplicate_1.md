# OpenMLE-fast task

Task ID: `air-passengers@1_duplicate_1`

Native metric: `AirPassengersForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (807 bytes)
- `data/sample_submission.csv` (505 bytes); columns: ["Month", "Passengers"]
- `data/test.csv` (198 bytes); columns: ["Month"]
- `data/train.csv` (1457 bytes); columns: ["Month", "Passengers"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (25 lines)
test.csv (25 lines)
train.csv (121 lines)```

-> sample_submission.csv has 24 rows and 2 columns.
Here is some information about the columns:
Month (object) has 24 unique values. Some example values: ['1959-01', '1959-02', '1959-03', '1959-04']
Passengers (float64) has range: 310.00 - 506.50, 0 nan values

-> test.csv has 24 rows and 1 columns.
Here is some information about the columns:
Month (object) has 24 unique values. Some example values: ['1959-01', '1959-02', '1959-03', '1959-04']

-> train.csv has 120 rows and 2 columns.
Here is some information about the columns:
Month (object) has 120 unique values. Some example values: ['1949-01', '1949-02', '1949-03', '1949-04']
Passengers (int64) has range: 104.00 - 505.00, 0 nan values
