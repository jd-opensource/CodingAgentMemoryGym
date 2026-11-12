# OpenMLE-fast task

Task ID: `news-detection-fake-or-real-dataset@1`

Native metric: `NewsFakeRealMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (339 bytes)
- `data/sample_submission.csv` (25723 bytes); columns: ["id", "label"]
- `data/test.csv` (5237234 bytes); columns: ["id", "text"]
- `data/train.csv` (20698411 bytes); columns: ["id", "text", "label"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (1979 lines)
test.csv (1979 lines)
train.csv (7965 lines)```

-> sample_submission.csv has 1978 rows and 2 columns.
The columns are: id, label

-> test.csv has 1978 rows and 2 columns.
The columns are: id, text

-> train.csv has 7922 rows and 3 columns.
The columns are: id, text, label
