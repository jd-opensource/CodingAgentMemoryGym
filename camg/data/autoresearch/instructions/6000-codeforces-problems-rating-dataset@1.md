# OpenMLE-fast task

Task ID: `6000-codeforces-problems-rating-dataset@1`

Native metric: `CodeforcesRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (407 bytes)
- `data/sample_submission.csv` (15251 bytes); columns: ["id", "Problem Rating"]
- `data/test.csv` (53409 bytes); columns: ["id", "Problem_tag_1", "Problem_tag_2", "Problem_tag_3", "Problem_tag_4", "Solved"]
- `data/train.csv` (247226 bytes); columns: ["id", "Problem_tag_1", "Problem_tag_2", "Problem_tag_3", "Problem_tag_4", "Solved", "Problem Rating"]

## Public description

Codeforces Difficulty Prediction Challenge

Files
- train.csv
- test.csv
- sample_submission.csv

Columns
- id
- Problem_tag_1, Problem_tag_2, Problem_tag_3, Problem_tag_4
- Solved
- Problem Rating (train only)

Task
Predict Problem Rating for each id in test.csv and submit a CSV with two columns: id and Problem Rating.

Evaluation
RMSE (lower is better) on hidden ground truth corresponding to test.csv.
