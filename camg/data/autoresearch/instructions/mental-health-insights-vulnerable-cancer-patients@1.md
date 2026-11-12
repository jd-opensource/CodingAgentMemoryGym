# OpenMLE-fast task

Task ID: `mental-health-insights-vulnerable-cancer-patients@1`

Native metric: `CancerEmotionIntensityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (349 bytes)
- `data/sample_submission.csv` (15501 bytes); columns: ["id", "intensity"]
- `data/test.csv` (2400736 bytes); columns: ["id", "posts"]
- `data/train.csv` (9924117 bytes); columns: ["id", "posts", "intensity"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (2080 lines)
test.csv (2080 lines)
train.csv (8313 lines)```

-> sample_submission.csv has 2079 rows and 2 columns.
The columns are: id, intensity

-> test.csv has 2079 rows and 2 columns.
The columns are: id, posts

-> train.csv has 8312 rows and 3 columns.
The columns are: id, posts, intensity
