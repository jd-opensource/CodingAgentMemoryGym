# OpenMLE-fast task

Task ID: `titanic-survival-analysis-dataset@2`

Native metric: `TitanicSurvivalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2219 bytes)
- `data/sample_submission.csv` (6222 bytes); columns: ["PassengerId", "Survived"]
- `data/test.csv` (18378 bytes); columns: ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
- `data/train.csv` (43159 bytes); columns: ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (269 lines)
test.csv (269 lines)
train.csv (624 lines)```

-> sample_submission.csv has 268 rows and 2 columns.
Here is some information about the columns:
PassengerId (int64) has range: 1.00 - 889.00, 0 nan values
Survived (float64) has range: 0.01 - 1.00, 0 nan values

-> test.csv has 268 rows and 11 columns.
Here is some information about the columns:
Age (float64) has range: 0.92 - 80.00, 46 nan values
Cabin (object) has 59 unique values. Some example values: ['C23 C25 C27', 'D17', 'B22', 'B30']
Embarked (object) has 3 unique values: ['S', 'C', nan, 'Q']
Fare (float64) has range: 0.00 - 263.00, 0 nan values
Name (object) has 268 unique values. Some example values: ['Johnston, Miss. Catherine Helen "Carrie"', 'Braund, Mr. Owen Harris', 'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 'Palsson, Master. Gosta Leonard']
Parch (int64) has 6 unique values: [0, 1, 5, 2, 4, 3]
PassengerId (int64) has range: 1.00 - 889.00, 0 nan values
Pclass (int64) has 3 unique values: [3, 1, 2]
Sex (object) has 2 unique values: ['male', 'female']
SibSp (int64) has 7 unique values: [1, 3, 0, 5, 8, 4, 2]
Ticket (object) has 241 unique values. Some example values: ['SC/Paris 2123', 'CA. 2343', '1601', 'CA 2144']

-> train.csv has 623 rows and 12 columns.
Here is some information about the columns:
Age (float64) has range: 0.42 - 74.00, 131 nan values
Cabin (object) has 113 unique values. Some example values: ['G6', 'F33', 'E101', 'B96 B98']
Embarked (object) has 3 unique values: ['C', 'S', 'Q', nan]
Fare (float64) has range: 0.00 - 512.33, 0 nan values
Name (object) has 623 unique values. Some example values: ['Dooley, Mr. Patrick', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 'Heikkinen, Miss. Laina', 'Allen, Mr. William Henry']
Parch (int64) has 7 unique values: [0, 2, 1, 5, 3, 4, 6]
PassengerId (int64) has range: 2.00 - 891.00, 0 nan values
Pclass (int64) has 3 unique values: [1, 3, 2]
Sex (object) has 2 unique values: ['female', 'male']
SibSp (int64) has 7 unique values: [1, 0, 4, 3, 2, 5, 8]
Survived (int64) has 2 unique values: [1, 0]
Ticket (object) has 518 unique values. Some example values: ['347082', '3101295', '347088', 'CA 2144']
