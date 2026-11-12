# OpenMLE-fast task

Task ID: `graduate-admissions@1`

Native metric: `GraduateAdmissionsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1532 bytes)
- `data/sample_submission.csv` (2329 bytes); columns: ["ID", "Chance of Admit"]
- `data/test.csv` (2921 bytes); columns: ["ID", "GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR", "CGPA", "Research"]
- `data/train.csv` (13449 bytes); columns: ["ID", "GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR", "CGPA", "Research", "Chance of Admit"]

## Public description

```
description.txt (37 lines)
sample_submission.csv (101 lines)
test.csv (101 lines)
train.csv (401 lines)```

-> sample_submission.csv has 100 rows and 2 columns.
Here is some information about the columns:
Chance of Admit (float64) has range: 0.01 - 1.00, 0 nan values
ID (int64) has range: 1.00 - 500.00, 0 nan values

-> test.csv has 100 rows and 8 columns.
Here is some information about the columns:
CGPA (float64) has range: 7.43 - 9.74, 0 nan values
GRE Score (int64) has range: 294.00 - 340.00, 0 nan values
ID (int64) has range: 1.00 - 500.00, 0 nan values
LOR (float64) has 8 unique values: [3.5, 5.0, 4.5, 3.0, 2.5, 4.0, 2.0, 1.5]
Research (int64) has 2 unique values: [0, 1]
SOP (float64) has 9 unique values: [4.5, 3.0, 4.0, 2.5, 3.5, 5.0, 2.0, 1.5, 1.0]
TOEFL Score (int64) has range: 94.00 - 119.00, 0 nan values
University Rating (int64) has 5 unique values: [5, 3, 4, 2, 1]

-> train.csv has 400 rows and 9 columns.
Here is some information about the columns:
CGPA (float64) has range: 6.80 - 9.92, 0 nan values
Chance of Admit (float64) has range: 0.34 - 0.97, 0 nan values
GRE Score (int64) has range: 290.00 - 340.00, 0 nan values
ID (int64) has range: 3.00 - 499.00, 0 nan values
LOR (float64) has 9 unique values: [4.0, 3.0, 2.5, 3.5, 4.5, 2.0, 5.0, 1.5, 1.0]
Research (int64) has 2 unique values: [1, 0]
SOP (float64) has 9 unique values: [4.5, 5.0, 3.5, 3.0, 4.0, 1.5, 2.5, 2.0, 1.0]
TOEFL Score (int64) has range: 92.00 - 120.00, 0 nan values
University Rating (int64) has 5 unique values: [4, 5, 3, 2, 1]
