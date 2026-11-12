# OpenMLE-fast task

Task ID: `temperature-and-ice-cream-sales@1`

Native metric: `IceCreamProfitMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (734 bytes)
- `data/sample_submission.csv` (760 bytes); columns: ["row_id", "Ice Cream Profits"]
- `data/test.csv` (515 bytes); columns: ["row_id", "Temperature"]
- `data/train.csv` (2537 bytes); columns: ["Temperature", "Ice Cream Profits"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (85 lines)
test.csv (85 lines)
train.csv (282 lines)```

-> sample_submission.csv has 84 rows and 2 columns.
Here is some information about the columns:
Ice Cream Profits (float64) has range: 18.82 - 85.13, 0 nan values
row_id (int64) has range: 0.00 - 83.00, 0 nan values

-> test.csv has 84 rows and 2 columns.
Here is some information about the columns:
Temperature (int64) has range: 39.00 - 101.00, 0 nan values
row_id (int64) has range: 0.00 - 83.00, 0 nan values

-> train.csv has 281 rows and 2 columns.
Here is some information about the columns:
Ice Cream Profits (float64) has range: 11.88 - 89.29, 0 nan values
Temperature (int64) has range: 40.00 - 99.00, 0 nan values
