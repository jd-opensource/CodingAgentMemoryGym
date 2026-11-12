# OpenMLE-fast task

Task ID: `student-scores@2`

Native metric: `StudentCareerAspirationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2232 bytes)
- `data/sample_submission.csv` (11392 bytes); columns: ["row_id", "career_aspiration"]
- `data/test.csv` (30526 bytes); columns: ["row_id", "gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "math_score", "history_score", "physics_score", "chemistry_score", "biology_score", "english_score", "geography_score"]
- `data/train.csv` (78685 bytes); columns: ["gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "math_score", "history_score", "physics_score", "chemistry_score", "biology_score", "english_score", "geography_score", "career_aspiration"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (602 lines)
test.csv (602 lines)
train.csv (1400 lines)```

-> sample_submission.csv has 601 rows and 2 columns.
Here is some information about the columns:
career_aspiration (object) has 17 unique values. Some example values: ['Accountant', 'Banker', 'Writer', 'Construction Engineer']
row_id (int64) has range: 100000.00 - 100600.00, 0 nan values

-> test.csv has 601 rows and 13 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
biology_score (int64) has range: 30.00 - 100.00, 0 nan values
chemistry_score (int64) has range: 50.00 - 100.00, 0 nan values
english_score (int64) has range: 50.00 - 99.00, 0 nan values
extracurricular_activities (bool) is 20.80% True, 79.20% False
gender (object) has 2 unique values: ['male', 'female']
geography_score (int64) has range: 60.00 - 100.00, 0 nan values
history_score (int64) has range: 50.00 - 100.00, 0 nan values
math_score (int64) has range: 40.00 - 100.00, 0 nan values
part_time_job (bool) is 14.31% True, 85.69% False
physics_score (int64) has range: 50.00 - 100.00, 0 nan values
row_id (int64) has range: 100000.00 - 100600.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 49.00, 0 nan values

-> train.csv has 1399 rows and 13 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
biology_score (int64) has range: 30.00 - 100.00, 0 nan values
career_aspiration (object) has 17 unique values. Some example values: ['Software Engineer', 'Business Owner', 'Unknown', 'Banker']
chemistry_score (int64) has range: 50.00 - 100.00, 0 nan values
english_score (int64) has range: 50.00 - 99.00, 0 nan values
extracurricular_activities (bool) is 20.23% True, 79.77% False
gender (object) has 2 unique values: ['female', 'male']
geography_score (int64) has range: 60.00 - 100.00, 0 nan values
history_score (int64) has range: 50.00 - 100.00, 0 nan values
math_score (int64) has range: 40.00 - 100.00, 0 nan values
part_time_job (bool) is 16.44% True, 83.56% False
physics_score (int64) has range: 50.00 - 100.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 50.00, 0 nan values
