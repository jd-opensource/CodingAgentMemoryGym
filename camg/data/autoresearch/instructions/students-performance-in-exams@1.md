# OpenMLE-fast task

Task ID: `students-performance-in-exams@1`

Native metric: `StudentsPerformanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1685 bytes)
- `data/sample_submission.csv` (10946 bytes); columns: ["math score", "reading score", "writing score"]
- `data/test.csv` (9427 bytes); columns: ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
- `data/train.csv` (44599 bytes); columns: ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course", "math score", "reading score", "writing score"]

## Public description

```
description.txt (37 lines)
sample_submission.csv (201 lines)
test.csv (201 lines)
train.csv (801 lines)```

-> sample_submission.csv has 200 rows and 3 columns.
Here is some information about the columns:
math score (float64) has range: 0.09 - 99.78, 0 nan values
reading score (float64) has range: 1.59 - 99.88, 0 nan values
writing score (float64) has range: 2.09 - 99.03, 0 nan values

-> test.csv has 200 rows and 5 columns.
Here is some information about the columns:
gender (object) has 2 unique values: ['male', 'female']
lunch (object) has 2 unique values: ['standard', 'free/reduced']
parental level of education (object) has 6 unique values: ['some college', "associate's degree", 'high school', "bachelor's degree", "master's degree", 'some high school']
race/ethnicity (object) has 5 unique values: ['group D', 'group B', 'group C', 'group E', 'group A']
test preparation course (object) has 2 unique values: ['none', 'completed']

-> train.csv has 800 rows and 8 columns.
Here is some information about the columns:
gender (object) has 2 unique values: ['male', 'female']
lunch (object) has 2 unique values: ['free/reduced', 'standard']
math score (int64) has range: 13.00 - 100.00, 0 nan values
parental level of education (object) has 6 unique values: ['some high school', 'high school', 'some college', "associate's degree", "bachelor's degree", "master's degree"]
race/ethnicity (object) has 5 unique values: ['group C', 'group D', 'group A', 'group E', 'group B']
reading score (int64) has range: 27.00 - 100.00, 0 nan values
test preparation course (object) has 2 unique values: ['completed', 'none']
writing score (int64) has range: 23.00 - 100.00, 0 nan values
