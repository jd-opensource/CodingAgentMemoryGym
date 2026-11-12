# OpenMLE-fast task

Task ID: `student-final-grade-prediction-multi-lin-reg@1`

Native metric: `StudentFinalGradeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4397 bytes)
- `data/sample_submission.csv` (1701 bytes); columns: ["row_id", "G3"]
- `data/test.csv` (8383 bytes); columns: ["row_id", "school", "sex", "age", "address", "famsize", "Parrent_status", "Mother_edu", "Father_edu", "Mother_job", "Father_job", "reason_to_chose_school", "guardian", "traveltime", "weekly_studytime", "failures", "extra_edu_supp", "family_edu_supp", "extra_paid_class", "extra_curr_activities", "nursery", "Interested_in_higher_edu", "internet_access", "romantic_relationship", "Family_quality_reln", "freetime_after_school", "goout_with_friends", "workday_alcohol_consum", "weekend_alcohol_consum", "health_status", "absences"]
- `data/train.csv` (33337 bytes); columns: ["row_id", "school", "sex", "age", "address", "famsize", "Parrent_status", "Mother_edu", "Father_edu", "Mother_job", "Father_job", "reason_to_chose_school", "guardian", "traveltime", "weekly_studytime", "failures", "extra_edu_supp", "family_edu_supp", "extra_paid_class", "extra_curr_activities", "nursery", "Interested_in_higher_edu", "internet_access", "romantic_relationship", "Family_quality_reln", "freetime_after_school", "goout_with_friends", "workday_alcohol_consum", "weekend_alcohol_consum", "health_status", "absences", "G3"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (80 lines)
test.csv (80 lines)
train.csv (317 lines)```

-> sample_submission.csv has 79 rows and 2 columns.
Here is some information about the columns:
G3 (float64) has range: 0.38 - 19.77, 0 nan values
row_id (int64) has range: 0.00 - 78.00, 0 nan values

-> test.csv has 79 rows and 31 columns.
Here is some information about the columns:
Family_quality_reln (int64) has 5 unique values: [4, 5, 3, 2, 1]
Father_edu (int64) has 4 unique values: [3, 2, 1, 4]
Father_job (object) has 5 unique values: ['services', 'other', 'at_home', 'teacher', 'health']
Interested_in_higher_edu (object) has 2 unique values: ['no', 'yes']
Mother_edu (int64) has 5 unique values: [1, 3, 2, 0, 4]
Mother_job (object) has 5 unique values: ['at_home', 'services', 'other', 'health', 'teacher']
Parrent_status (object) has 2 unique values: ['T', 'A']
absences (int64) has range: 0.00 - 54.00, 0 nan values
address (object) has 2 unique values: ['U', 'R']
age (int64) has 7 unique values: [18, 16, 19, 17, 15, 22, 20]
extra_curr_activities (object) has 2 unique values: ['no', 'yes']
extra_edu_supp (object) has 2 unique values: ['no', 'yes']
extra_paid_class (object) has 2 unique values: ['no', 'yes']
failures (int64) has 4 unique values: [1, 0, 3, 2]
family_edu_supp (object) has 2 unique values: ['no', 'yes']
famsize (object) has 2 unique values: ['LE3', 'GT3']
freetime_after_school (int64) has 5 unique values: [3, 1, 4, 2, 5]
goout_with_friends (int64) has 5 unique values: [3, 2, 4, 5, 1]
guardian (object) has 3 unique values: ['mother', 'father', 'other']
health_status (int64) has 5 unique values: [3, 2, 5, 1, 4]
internet_access (object) has 2 unique values: ['yes', 'no']
nursery (object) has 2 unique values: ['yes', 'no']
reason_to_chose_school (object) has 4 unique values: ['course', 'reputation', 'other', 'home']
romantic_relationship (object) has 2 unique values: ['yes', 'no']
row_id (int64) has range: 0.00 - 78.00, 0 nan values
school (object) has 2 unique values: ['MS', 'GP']
sex (object) has 2 unique values: ['M', 'F']
traveltime (int64) has 3 unique values: [1, 2, 3]
weekend_alcohol_consum (int64) has 5 unique values: [3, 2, 1, 4, 5]
weekly_studytime (int64) has 4 unique values: [1, 3, 4, 2]
workday_alcohol_consum (int64) has 5 unique values: [2, 1, 5, 3, 4]

-> train.csv has 316 rows and 32 columns.
Here is some information about the columns:
Family_quality_reln (int64) has 5 unique values: [4, 5, 3, 2, 1]
Father_edu (int64) has 5 unique values: [4, 1, 3, 2, 0]
Father_job (object) has 5 unique values: ['teacher', 'other', 'services', 'health', 'at_home']
G3 (int64) has range: 0.00 - 20.00, 0 nan values
Interested_in_higher_edu (object) has 2 unique values: ['yes', 'no']
Mother_edu (int64) has 5 unique values: [4, 2, 3, 1, 0]
Mother_job (object) has 5 unique values: ['services', 'other', 'health', 'at_home', 'teacher']
Parrent_status (object) has 2 unique values: ['T', 'A']
absences (int64) has range: 0.00 - 75.00, 0 nan values
address (object) has 2 unique values: ['U', 'R']
age (int64) has 7 unique values: [15, 18, 16, 17, 21, 19, 20]
extra_curr_activities (object) has 2 unique values: ['yes', 'no']
extra_edu_supp (object) has 2 unique values: ['yes', 'no']
extra_paid_class (object) has 2 unique values: ['no', 'yes']
failures (int64) has 4 unique values: [1, 0, 3, 2]
family_edu_supp (object) has 2 unique values: ['yes', 'no']
famsize (object) has 2 unique values: ['GT3', 'LE3']
freetime_after_school (int64) has 5 unique values: [4, 5, 2, 3, 1]
goout_with_friends (int64) has 5 unique values: [4, 3, 5, 2, 1]
guardian (object) has 3 unique values: ['father', 'mother', 'other']
health_status (int64) has 5 unique values: [3, 5, 4, 1, 2]
internet_access (object) has 2 unique values: ['yes', 'no']
nursery (object) has 2 unique values: ['no', 'yes']
reason_to_chose_school (object) has 4 unique values: ['other', 'home', 'course', 'reputation']
romantic_relationship (object) has 2 unique values: ['no', 'yes']
row_id (int64) has range: 0.00 - 315.00, 0 nan values
school (object) has 2 unique values: ['GP', 'MS']
sex (object) has 2 unique values: ['F', 'M']
traveltime (int64) has 4 unique values: [1, 2, 3, 4]
weekend_alcohol_consum (int64) has 5 unique values: [1, 3, 2, 4, 5]
weekly_studytime (int64) has 4 unique values: [2, 1, 3, 4]
workday_alcohol_consum (int64) has 5 unique values: [1, 3, 2, 4, 5]
