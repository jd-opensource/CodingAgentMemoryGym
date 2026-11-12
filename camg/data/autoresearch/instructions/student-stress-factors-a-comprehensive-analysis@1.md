# OpenMLE-fast task

Task ID: `student-stress-factors-a-comprehensive-analysis@1`

Native metric: `StudentStressSeverityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3268 bytes)
- `data/sample_submission.csv` (2216 bytes); columns: ["id", "stress_level"]
- `data/test.csv` (11315 bytes); columns: ["id", "anxiety_level", "self_esteem", "mental_health_history", "depression", "headache", "blood_pressure", "sleep_quality", "breathing_problem", "noise_level", "living_conditions", "safety", "basic_needs", "academic_performance", "study_load", "teacher_student_relationship", "future_career_concerns", "social_support", "peer_pressure", "extracurricular_activities", "bullying"]
- `data/train.csv` (46081 bytes); columns: ["id", "anxiety_level", "self_esteem", "mental_health_history", "depression", "headache", "blood_pressure", "sleep_quality", "breathing_problem", "noise_level", "living_conditions", "safety", "basic_needs", "academic_performance", "study_load", "teacher_student_relationship", "future_career_concerns", "social_support", "peer_pressure", "extracurricular_activities", "bullying", "stress_level"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (221 lines)
test.csv (221 lines)
train.csv (881 lines)```

-> sample_submission.csv has 220 rows and 2 columns.
Here is some information about the columns:
id (object) has 220 unique values. Some example values: ['S000020', 'S000032', 'S000033', 'S000041']
stress_level (int64) has 3 unique values: [1, 2, 0]

-> test.csv has 220 rows and 21 columns.
Here is some information about the columns:
academic_performance (int64) has 6 unique values: [5, 2, 1, 0, 3, 4]
anxiety_level (int64) has range: 0.00 - 21.00, 0 nan values
basic_needs (int64) has 6 unique values: [4, 5, 2, 1, 3, 0]
blood_pressure (int64) has 3 unique values: [2, 3, 1]
breathing_problem (int64) has 6 unique values: [2, 1, 5, 4, 3, 0]
bullying (int64) has 6 unique values: [1, 5, 4, 0, 2, 3]
depression (int64) has range: 0.00 - 27.00, 0 nan values
extracurricular_activities (int64) has 6 unique values: [2, 1, 5, 0, 4, 3]
future_career_concerns (int64) has 6 unique values: [1, 5, 4, 3, 2, 0]
headache (int64) has 6 unique values: [1, 5, 4, 3, 2, 0]
id (object) has 220 unique values. Some example values: ['S001043', 'S000500', 'S000869', 'S000521']
living_conditions (int64) has 6 unique values: [3, 2, 4, 1, 5, 0]
mental_health_history (int64) has 2 unique values: [0, 1]
noise_level (int64) has 6 unique values: [1, 2, 3, 4, 0, 5]
peer_pressure (int64) has 6 unique values: [2, 1, 5, 4, 3, 0]
safety (int64) has 6 unique values: [5, 1, 2, 4, 0, 3]
self_esteem (int64) has range: 0.00 - 30.00, 0 nan values
sleep_quality (int64) has 6 unique values: [5, 1, 0, 2, 3, 4]
social_support (int64) has 4 unique values: [3, 1, 0, 2]
study_load (int64) has 6 unique values: [2, 1, 5, 3, 0, 4]
teacher_student_relationship (int64) has 6 unique values: [5, 4, 2, 1, 3, 0]

-> train.csv has 880 rows and 22 columns.
Here is some information about the columns:
academic_performance (int64) has 6 unique values: [3, 1, 4, 2, 5, 0]
anxiety_level (int64) has range: 0.00 - 21.00, 0 nan values
basic_needs (int64) has 6 unique values: [3, 2, 4, 1, 0, 5]
blood_pressure (int64) has 3 unique values: [1, 3, 2]
breathing_problem (int64) has 6 unique values: [2, 5, 1, 3, 4, 0]
bullying (int64) has 6 unique values: [2, 5, 1, 4, 3, 0]
depression (int64) has range: 0.00 - 27.00, 0 nan values
extracurricular_activities (int64) has 6 unique values: [3, 5, 2, 4, 1, 0]
future_career_concerns (int64) has 6 unique values: [2, 4, 1, 5, 3, 0]
headache (int64) has 6 unique values: [2, 4, 1, 3, 5, 0]
id (object) has 880 unique values. Some example values: ['S000205', 'S000646', 'S000130', 'S000561']
living_conditions (int64) has 6 unique values: [2, 1, 4, 3, 5, 0]
mental_health_history (int64) has 2 unique values: [1, 0]
noise_level (int64) has 6 unique values: [2, 5, 1, 4, 3, 0]
peer_pressure (int64) has 6 unique values: [3, 5, 1, 2, 4, 0]
safety (int64) has 6 unique values: [2, 1, 5, 3, 4, 0]
self_esteem (int64) has range: 0.00 - 30.00, 0 nan values
sleep_quality (int64) has 6 unique values: [2, 1, 5, 4, 3, 0]
social_support (int64) has 4 unique values: [2, 1, 3, 0]
stress_level (int64) has 3 unique values: [1, 2, 0]
study_load (int64) has 6 unique values: [2, 4, 1, 5, 3, 0]
teacher_student_relationship (int64) has 6 unique values: [3, 2, 4, 1, 0, 5]
