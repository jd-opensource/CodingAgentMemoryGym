# OpenMLE-fast task

Task ID: `student-performance-prediction@1_duplicate_1`

Native metric: `StudentPerformanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4094 bytes)
- `data/sample_submission.csv` (5994 bytes); columns: ["id", "G3"]
- `data/test.csv` (27700 bytes); columns: ["id", "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", "subject"]
- `data/train.csv` (84734 bytes); columns: ["id", "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences", "subject", "G3"]

## Public description

```
description.txt (33 lines)
sample_submission.csv (262 lines)
test.csv (262 lines)
train.csv (784 lines)```

-> sample_submission.csv has 261 rows and 2 columns.
Here is some information about the columns:
G3 (float64) has 1 unique values: [11.348659003831418]
id (int64) has range: 10.00 - 1041.00, 0 nan values

-> test.csv has 261 rows and 32 columns.
Here is some information about the columns:
Dalc (int64) has 5 unique values: [3, 1, 2, 5, 4]
Fedu (int64) has 5 unique values: [1, 2, 4, 3, 0]
Fjob (object) has 5 unique values: ['at_home', 'teacher', 'services', 'other', 'health']
Medu (int64) has 5 unique values: [1, 3, 4, 2, 0]
Mjob (object) has 5 unique values: ['at_home', 'services', 'teacher', 'other', 'health']
Pstatus (object) has 2 unique values: ['T', 'A']
Walc (int64) has 5 unique values: [3, 1, 2, 4, 5]
absences (int64) has range: 0.00 - 32.00, 0 nan values
activities (object) has 2 unique values: ['no', 'yes']
address (object) has 2 unique values: ['U', 'R']
age (int64) has 7 unique values: [16, 18, 19, 15, 17, 22, 20]
failures (int64) has 4 unique values: [0, 2, 3, 1]
famrel (int64) has 5 unique values: [3, 2, 1, 4, 5]
famsize (object) has 2 unique values: ['LE3', 'GT3']
famsup (object) has 2 unique values: ['no', 'yes']
freetime (int64) has 5 unique values: [4, 5, 2, 3, 1]
goout (int64) has 5 unique values: [4, 5, 2, 1, 3]
guardian (object) has 3 unique values: ['mother', 'father', 'other']
health (int64) has 5 unique values: [1, 3, 5, 4, 2]
higher (object) has 2 unique values: ['yes', 'no']
id (int64) has range: 10.00 - 1041.00, 0 nan values
internet (object) has 2 unique values: ['yes', 'no']
nursery (object) has 2 unique values: ['yes', 'no']
paid (object) has 2 unique values: ['no', 'yes']
reason (object) has 4 unique values: ['course', 'home', 'reputation', 'other']
romantic (object) has 2 unique values: ['no', 'yes']
school (object) has 2 unique values: ['GP', 'MS']
schoolsup (object) has 2 unique values: ['no', 'yes']
sex (object) has 2 unique values: ['F', 'M']
studytime (int64) has 4 unique values: [1, 2, 4, 3]
subject (object) has 2 unique values: ['mat', 'por']
traveltime (int64) has 4 unique values: [1, 2, 3, 4]

-> train.csv has 783 rows and 33 columns.
Here is some information about the columns:
Dalc (int64) has 5 unique values: [4, 1, 3, 2, 5]
Fedu (int64) has 5 unique values: [1, 2, 3, 4, 0]
Fjob (object) has 5 unique values: ['other', 'services', 'teacher', 'at_home', 'health']
G3 (int64) has range: 0.00 - 20.00, 0 nan values
Medu (int64) has 5 unique values: [2, 1, 4, 3, 0]
Mjob (object) has 5 unique values: ['at_home', 'services', 'health', 'other', 'teacher']
Pstatus (object) has 2 unique values: ['T', 'A']
Walc (int64) has 5 unique values: [5, 3, 2, 4, 1]
absences (int64) has range: 0.00 - 75.00, 0 nan values
activities (object) has 2 unique values: ['yes', 'no']
address (object) has 2 unique values: ['U', 'R']
age (int64) has 8 unique values: [18, 15, 16, 17, 19, 20, 21, 22]
failures (int64) has 4 unique values: [0, 2, 1, 3]
famrel (int64) has 5 unique values: [4, 5, 3, 2, 1]
famsize (object) has 2 unique values: ['LE3', 'GT3']
famsup (object) has 2 unique values: ['yes', 'no']
freetime (int64) has 5 unique values: [3, 2, 4, 5, 1]
goout (int64) has 5 unique values: [2, 3, 5, 4, 1]
guardian (object) has 3 unique values: ['mother', 'father', 'other']
health (int64) has 5 unique values: [3, 4, 5, 1, 2]
higher (object) has 2 unique values: ['yes', 'no']
id (int64) has range: 0.00 - 1043.00, 0 nan values
internet (object) has 2 unique values: ['yes', 'no']
nursery (object) has 2 unique values: ['yes', 'no']
paid (object) has 2 unique values: ['no', 'yes']
reason (object) has 4 unique values: ['course', 'home', 'reputation', 'other']
romantic (object) has 2 unique values: ['yes', 'no']
school (object) has 2 unique values: ['GP', 'MS']
schoolsup (object) has 2 unique values: ['yes', 'no']
sex (object) has 2 unique values: ['M', 'F']
studytime (int64) has 4 unique values: [2, 1, 4, 3]
subject (object) has 2 unique values: ['por', 'mat']
traveltime (int64) has 4 unique values: [4, 2, 3, 1]
