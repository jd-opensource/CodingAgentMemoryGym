# OpenMLE-fast task

Task ID: `2d-datasets@1`

Native metric: `TwoDClusterClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (964 bytes)
- `data/sample_submission.csv` (7028 bytes); columns: ["id", "label"]
- `data/test.csv` (6773 bytes); columns: ["id", "x", "y"]
- `data/train.csv` (49995 bytes); columns: ["id", "x", "y", "label"]

## Public description

```
description.txt (32 lines)
sample_submission.csv (473 lines)
test.csv (473 lines)
train.csv (1932 lines)```

-> sample_submission.csv has 472 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 471.00, 0 nan values
label (object) has 23 unique values. Some example values: ['Aggregation_5', 'Aggregation_4', 'Flame_2', 'Flame_1']

-> test.csv has 472 rows and 3 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 471.00, 0 nan values
x (float64) has range: 0.65 - 42.25, 0 nan values
y (float64) has range: 2.40 - 31.10, 0 nan values

-> train.csv has 1931 rows and 4 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 1930.00, 0 nan values
label (object) has 23 unique values. Some example values: ['Jain_1', 'Aggregation_4', 'Aggregation_2', 'Compound_5']
x (float64) has range: 0.50 - 42.90, 0 nan values
y (float64) has range: 1.95 - 31.75, 0 nan values
