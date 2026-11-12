# OpenMLE-fast task

Task ID: `student-lifestyle-dataset@1`

Native metric: `StudentLifestyleRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1368 bytes)
- `data/sample_submission.csv` (8899 bytes); columns: ["row_id", "GPA"]
- `data/test.csv` (9632 bytes); columns: ["row_id", "Study_Hours_Per_Day", "Extracurricular_Hours_Per_Day", "Sleep_Hours_Per_Day", "Social_Hours_Per_Day", "Physical_Activity_Hours_Per_Day"]
- `data/train.csv` (46891 bytes); columns: ["row_id", "Study_Hours_Per_Day", "Extracurricular_Hours_Per_Day", "Sleep_Hours_Per_Day", "Social_Hours_Per_Day", "Physical_Activity_Hours_Per_Day", "GPA"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (401 lines)
test.csv (401 lines)
train.csv (1601 lines)```

-> sample_submission.csv has 400 rows and 2 columns.
Here is some information about the columns:
GPA (float64) has range: 2.24 - 3.79, 0 nan values
row_id (int64) has range: 0.00 - 399.00, 0 nan values

-> test.csv has 400 rows and 6 columns.
Here is some information about the columns:
Extracurricular_Hours_Per_Day (float64) has range: 0.00 - 4.00, 0 nan values
Physical_Activity_Hours_Per_Day (float64) has range: 0.10 - 11.20, 0 nan values
Sleep_Hours_Per_Day (float64) has range: 5.00 - 10.00, 0 nan values
Social_Hours_Per_Day (float64) has range: 0.00 - 6.00, 0 nan values
Study_Hours_Per_Day (float64) has range: 5.00 - 10.00, 0 nan values
row_id (int64) has range: 0.00 - 399.00, 0 nan values

-> train.csv has 1600 rows and 7 columns.
Here is some information about the columns:
Extracurricular_Hours_Per_Day (float64) has range: 0.00 - 4.00, 0 nan values
GPA (float64) has range: 2.24 - 4.00, 0 nan values
Physical_Activity_Hours_Per_Day (float64) has range: 0.00 - 13.00, 0 nan values
Sleep_Hours_Per_Day (float64) has range: 5.00 - 10.00, 0 nan values
Social_Hours_Per_Day (float64) has range: 0.00 - 6.00, 0 nan values
Study_Hours_Per_Day (float64) has range: 5.00 - 10.00, 0 nan values
row_id (int64) has range: 0.00 - 1599.00, 0 nan values
