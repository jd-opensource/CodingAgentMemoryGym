# OpenMLE-fast task

Task ID: `boston-housing-dataset@1`

Native metric: `BostonHousingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (401 bytes)
- `data/sample_submission.csv` (3351 bytes); columns: ["Id", "medv"]
- `data/test.csv` (10717 bytes); columns: ["Id", "crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat"]
- `data/train.csv` (25267 bytes); columns: ["crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "medv"]

## Public description

Boston Home Value Prediction Challenge

Problem statement
Build a model that predicts the median value of owner-occupied homes (in $1000s) using tabular features.

Data description
- train.csv: Features + target medv for training.
- test.csv: Id + features without medv.
- sample_submission.csv: Required submission format (Id, medv).

Columns
Each row includes 13 features and the target label medv.
