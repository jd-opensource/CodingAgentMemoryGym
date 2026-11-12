# OpenMLE-fast task

Task ID: `student-scores@1`

Native metric: `StudentScoresMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4121 bytes)
- `data/sample_submission.csv` (49732 bytes); columns: ["row_id", "math_score", "history_score", "physics_score", "chemistry_score", "biology_score", "english_score", "geography_score"]
- `data/test.csv` (15847 bytes); columns: ["row_id", "gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "career_aspiration"]
- `data/test_features.csv` (15847 bytes); columns: ["row_id", "gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "career_aspiration"]
- `data/train.csv` (97003 bytes); columns: ["row_id", "gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "career_aspiration", "math_score", "history_score", "physics_score", "chemistry_score", "biology_score", "english_score", "geography_score"]
- `data/train_features.csv` (63023 bytes); columns: ["row_id", "gender", "part_time_job", "absence_days", "extracurricular_activities", "weekly_self_study_hours", "career_aspiration"]
- `data/train_labels.csv` (41086 bytes); columns: ["row_id", "math_score", "history_score", "physics_score", "chemistry_score", "biology_score", "english_score", "geography_score"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (402 lines)
test.csv (402 lines)
test_features.csv (402 lines)
train.csv (1600 lines)
train_features.csv (1600 lines)
train_labels.csv (1600 lines)```

-> sample_submission.csv has 401 rows and 8 columns.
Here is some information about the columns:
biology_score (float64) has range: 39.71 - 100.00, 0 nan values
chemistry_score (float64) has range: 42.47 - 100.00, 0 nan values
english_score (float64) has range: 45.19 - 100.00, 0 nan values
geography_score (float64) has range: 49.73 - 100.00, 0 nan values
history_score (float64) has range: 46.05 - 100.00, 0 nan values
math_score (float64) has range: 40.95 - 100.00, 0 nan values
physics_score (float64) has range: 44.91 - 100.00, 0 nan values
row_id (int64) has range: 6.00 - 1992.00, 0 nan values

-> test.csv has 401 rows and 7 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
career_aspiration (object) has 17 unique values. Some example values: ['Software Engineer', 'Business Owner', 'Unknown', 'Banker']
extracurricular_activities (bool) is 22.94% True, 77.06% False
gender (object) has 2 unique values: ['male', 'female']
part_time_job (bool) is 13.97% True, 86.03% False
row_id (int64) has range: 6.00 - 1992.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 50.00, 0 nan values

-> test_features.csv has 401 rows and 7 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
career_aspiration (object) has 17 unique values. Some example values: ['Software Engineer', 'Business Owner', 'Unknown', 'Banker']
extracurricular_activities (bool) is 22.94% True, 77.06% False
gender (object) has 2 unique values: ['male', 'female']
part_time_job (bool) is 13.97% True, 86.03% False
row_id (int64) has range: 6.00 - 1992.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 50.00, 0 nan values

-> train.csv has 1599 rows and 14 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
biology_score (int64) has range: 30.00 - 100.00, 0 nan values
career_aspiration (object) has 17 unique values. Some example values: ['Software Engineer', 'Business Owner', 'Unknown', 'Banker']
chemistry_score (int64) has range: 50.00 - 100.00, 0 nan values
english_score (int64) has range: 50.00 - 99.00, 0 nan values
extracurricular_activities (bool) is 19.76% True, 80.24% False
gender (object) has 2 unique values: ['female', 'male']
geography_score (int64) has range: 60.00 - 100.00, 0 nan values
history_score (int64) has range: 50.00 - 100.00, 0 nan values
math_score (int64) has range: 40.00 - 100.00, 0 nan values
part_time_job (bool) is 16.26% True, 83.74% False
physics_score (int64) has range: 50.00 - 100.00, 0 nan values
row_id (int64) has range: 0.00 - 1999.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 50.00, 0 nan values

-> train_features.csv has 1599 rows and 7 columns.
Here is some information about the columns:
absence_days (int64) has range: 0.00 - 10.00, 0 nan values
career_aspiration (object) has 17 unique values. Some example values: ['Software Engineer', 'Business Owner', 'Unknown', 'Banker']
extracurricular_activities (bool) is 19.76% True, 80.24% False
gender (object) has 2 unique values: ['female', 'male']
part_time_job (bool) is 16.26% True, 83.74% False
row_id (int64) has range: 0.00 - 1999.00, 0 nan values
weekly_self_study_hours (int64) has range: 0.00 - 50.00, 0 nan values

-> train_labels.csv has 1599 rows and 8 columns.
Here is some information about the columns:
biology_score (int64) has range: 30.00 - 100.00, 0 nan values
chemistry_score (int64) has range: 50.00 - 100.00, 0 nan values
english_score (int64) has range: 50.00 - 99.00, 0 nan values
geography_score (int64) has range: 60.00 - 100.00, 0 nan values
history_score (int64) has range: 50.00 - 100.00, 0 nan values
math_score (int64) has range: 40.00 - 100.00, 0 nan values
physics_score (int64) has range: 50.00 - 100.00, 0 nan values
row_id (int64) has range: 0.00 - 1999.00, 0 nan values
