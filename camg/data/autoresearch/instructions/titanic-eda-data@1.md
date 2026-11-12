# OpenMLE-fast task

Task ID: `titanic-eda-data@1`

Native metric: `TitanicSurvivalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2230 bytes)
- `data/sample_submission.csv` (1679 bytes); columns: ["PassengerId", "Survived"]
- `data/test.csv` (14021 bytes); columns: ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
- `data/train.csv` (47630 bytes); columns: ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (212 lines)
test.csv (212 lines)
train.csv (681 lines)```

-> sample_submission.csv has 211 rows and 2 columns.
Here is some information about the columns:
PassengerId (int64) has range: 2.00 - 885.00, 0 nan values
Survived (float64) has 1 unique values: [0.5]

-> test.csv has 211 rows and 11 columns.
Here is some information about the columns:
Age (float64) has range: 0.67 - 70.00, 56 nan values
Cabin (object) has 44 unique values. Some example values: ['C23 C25 C27', 'B57 B59 B63 B66', 'C126', 'B18']
Embarked (object) has 3 unique values: ['C', 'S', 'Q']
Fare (float64) has range: 0.00 - 263.00, 0 nan values
Name (object) has 211 unique values. Some example values: ['Ryerson, Miss. Emily Borie', 'Ryerson, Miss. Susan Parker "Suzette"', 'Bazzani, Miss. Albina', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)']
Parch (int64) has 5 unique values: [2, 0, 1, 4, 3]
PassengerId (int64) has range: 2.00 - 885.00, 0 nan values
Pclass (int64) has 3 unique values: [1, 2, 3]
Sex (object) has 2 unique values: ['female', 'male']
SibSp (int64) has 4 unique values: [2, 0, 1, 3]
Ticket (object) has 168 unique values. Some example values: ['347088', '19950', '239853', '13502']

-> train.csv has 680 rows and 12 columns.
Here is some information about the columns:
Age (float64) has range: 0.42 - 80.00, 121 nan values
Cabin (object) has 111 unique values. Some example values: ['B96 B98', 'G6', 'C22 C26', 'F2']
Embarked (object) has 3 unique values: ['C', 'S', nan, 'Q']
Fare (float64) has range: 0.00 - 512.33, 0 nan values
Name (object) has 680 unique values. Some example values: ['Ahlin, Mrs. Johan (Johanna Persdotter Larsson)', 'Duff Gordon, Lady. (Lucille Christiana Sutherland) ("Mrs Morgan")', 'Cherry, Miss. Gladys', 'Maioni, Miss. Roberta']
Parch (int64) has 7 unique values: [0, 2, 1, 5, 6, 3, 4]
PassengerId (int64) has range: 1.00 - 891.00, 0 nan values
Pclass (int64) has 3 unique values: [1, 2, 3]
Sex (object) has 2 unique values: ['female', 'male']
SibSp (int64) has 7 unique values: [1, 0, 2, 3, 4, 8, 5]
Survived (int64) has 2 unique values: [1, 0]
Ticket (object) has 513 unique values. Some example values: ['CA. 2343', '1601', '347082', 'CA 2144']
