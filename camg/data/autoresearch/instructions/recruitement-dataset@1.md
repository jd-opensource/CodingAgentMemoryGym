# OpenMLE-fast task

Task ID: `recruitement-dataset@1`

Native metric: `ResumeJobMatchMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (407 bytes)
- `data/sample_submission.csv` (48349 bytes); columns: ["id", "best_match"]
- `data/test.csv` (1933659 bytes); columns: ["id", "resume", "job_role", "job_description"]
- `data/train.csv` (7749008 bytes); columns: ["id", "resume", "job_role", "job_description", "best_match"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (2001 lines)
test.csv (2001 lines)
train.csv (8001 lines)```

-> sample_submission.csv has 2000 rows and 2 columns.
The columns are: id, best_match

-> test.csv has 2000 rows and 4 columns.
The columns are: id, resume, job_role, job_description

-> train.csv has 8000 rows and 5 columns.
The columns are: id, resume, job_role, job_description, best_match
