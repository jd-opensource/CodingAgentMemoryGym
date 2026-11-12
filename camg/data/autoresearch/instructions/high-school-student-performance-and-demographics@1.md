# OpenMLE-fast task

Task ID: `high-school-student-performance-and-demographics@1`

Native metric: `FinalGradePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (550 bytes)
- `data/sample_submission.csv` (1057 bytes); columns: ["final_grade"]
- `data/test.csv` (40298 bytes); columns: ["school", "sex", "age", "address_type", "family_size", "parent_status", "mother_education", "father_education", "mother_job", "father_job", "school_choice_reason", "guardian", "travel_time", "study_time", "class_failures", "school_support", "family_support", "extra_paid_classes", "activities", "nursery_school", "higher_ed", "internet_access", "romantic_relationship", "family_relationship", "free_time", "social", "weekday_alcohol", "weekend_alcohol", "health", "absences", "subject"]
- `data/train.csv` (163500 bytes); columns: ["school", "sex", "age", "address_type", "family_size", "parent_status", "mother_education", "father_education", "mother_job", "father_job", "school_choice_reason", "guardian", "travel_time", "study_time", "class_failures", "school_support", "family_support", "extra_paid_classes", "activities", "nursery_school", "higher_ed", "internet_access", "romantic_relationship", "family_relationship", "free_time", "social", "weekday_alcohol", "weekend_alcohol", "health", "absences", "final_grade", "subject"]

## Public description

Public data overview

Files under public/:
- train.csv: Training set containing features and the target column 'final_grade'. No leakage columns ('grade_1', 'grade_2', 'student_id') are included. The 'subject' column indicates Math or Portuguese.
- test.csv: Test set containing the same feature columns as train.csv, excluding the target 'final_grade'. Use this to generate predictions.
- sample_submission.csv: A sample submission file with a single column 'final_grade' and one row per test instance. Replace values with your model's predictions.
