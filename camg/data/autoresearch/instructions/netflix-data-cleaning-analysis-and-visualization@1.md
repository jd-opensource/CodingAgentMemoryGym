# OpenMLE-fast task

Task ID: `netflix-data-cleaning-analysis-and-visualization@1`

Native metric: `NetflixGenreF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (412 bytes)
- `data/sample_submission.csv` (71502 bytes); columns: ["id", "labels"]
- `data/test.csv` (149305 bytes); columns: ["id", "type", "title", "director", "country", "date_added", "release_year", "rating", "duration"]
- `data/train.csv` (850271 bytes); columns: ["id", "type", "title", "director", "country", "date_added", "release_year", "rating", "duration", "labels"]

## Public description

Title: Netflix Multi-Label Genre Prediction from Metadata

Problem statement:
Given metadata for Netflix titles, predict all applicable content categories (labels) for each title.

Files provided to participants:
- train.csv
- test.csv
- sample_submission.csv

Submission format:
- CSV with columns: id, labels (comma-separated).

Evaluation metric:
- Macro-averaged F1 over labels built from test ground truth.
