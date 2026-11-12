# OpenMLE-fast task

Task ID: `titanic-csv@1`

Native metric: `TitanicSurvivalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2165 bytes)
- `data/sample_submission.csv` (2124 bytes); columns: ["PassengerId", "Survived"]
- `data/test.csv` (19210 bytes); columns: ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
- `data/train.csv` (42327 bytes); columns: ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (269 lines)
test.csv (269 lines)
train.csv (624 lines)```

-> sample_submission.csv has 268 rows and 2 columns.
Here is some information about the columns:
PassengerId (int64) has range: 4.00 - 886.00, 0 nan values
Survived (float64) has 1 unique values: [0.5]

-> test.csv has 268 rows and 11 columns.
Here is some information about the columns:
Age (float64) has range: 0.67 - 64.00, 40 nan values
Cabin (object) has 38 unique values. Some example values: ['G6', 'C23 C25 C27', 'B96 B98', 'F2']
Embarked (object) has 3 unique values: ['S', 'Q', 'C']
Fare (float64) has range: 0.00 - 263.00, 0 nan values
Name (object) has 268 unique values. Some example values: ['Rice, Mrs. William (Margaret Norton)', 'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 'Allen, Mr. William Henry', 'Moran, Mr. James']
Parch (int64) has 7 unique values: [0, 1, 2, 5, 3, 4, 6]
PassengerId (int64) has range: 4.00 - 886.00, 0 nan values
Pclass (int64) has 3 unique values: [1, 3, 2]
Sex (object) has 2 unique values: ['female', 'male']
SibSp (int64) has 7 unique values: [1, 0, 3, 4, 2, 5, 8]
Ticket (object) has 136 unique values. Some example values: ['347082', 'CA. 2343', '3101295', '347088']

-> train.csv has 623 rows and 12 columns.
Here is some information about the columns:
Age (float64) has range: 0.42 - 80.00, 137 nan values
Cabin (object) has 113 unique values. Some example values: ['D', 'E101', 'B28', 'F G73']
Embarked (object) has 3 unique values: ['S', 'C', 'Q', nan]
Fare (float64) has range: 0.00 - 512.33, 0 nan values
Name (object) has 623 unique values. Some example values: ['Dooley, Mr. Patrick', 'Braund, Mr. Owen Harris', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 'Heikkinen, Miss. Laina']
Parch (int64) has 4 unique values: [0, 1, 2, 3]
PassengerId (int64) has range: 1.00 - 891.00, 0 nan values
Pclass (int64) has 3 unique values: [3, 1, 2]
Sex (object) has 2 unique values: ['male', 'female']
SibSp (int64) has 4 unique values: [1, 0, 2, 3]
Survived (int64) has 2 unique values: [0, 1]
Ticket (object) has 559 unique values. Some example values: ['1601', 'PC 17757', '239853', 'PC 17760']
