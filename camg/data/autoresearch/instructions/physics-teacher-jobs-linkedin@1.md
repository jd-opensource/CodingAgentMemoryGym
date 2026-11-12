# OpenMLE-fast task

Task ID: `physics-teacher-jobs-linkedin@1`

Native metric: `PhysicsTeacherSectorClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (573 bytes)
- `data/sample_submission.csv` (5318 bytes); columns: ["id", "sector"]
- `data/test.csv` (419606 bytes); columns: ["id", "title", "description", "location", "publishedAt", "companyName", "applicationsCount", "contractType", "experienceLevel", "workType", "salary"]
- `data/train.csv` (2365355 bytes); columns: ["id", "title", "description", "location", "publishedAt", "companyName", "applicationsCount", "contractType", "experienceLevel", "workType", "salary", "sector"]

## Public description

```
description.txt (60 lines)
sample_submission.csv (129 lines)
test.csv (129 lines)
train.csv (631 lines)```

-> sample_submission.csv has 128 rows and 2 columns.
The columns are: id, sector

-> test.csv has 128 rows and 11 columns.
The columns are: id, title, description, location, publishedAt, companyName, applicationsCount, contractType, experienceLevel, workType, salary

-> train.csv has 630 rows and 12 columns.
The columns are: id, title, description, location, publishedAt, companyName, applicationsCount, contractType, experienceLevel, workType, salary, sector
