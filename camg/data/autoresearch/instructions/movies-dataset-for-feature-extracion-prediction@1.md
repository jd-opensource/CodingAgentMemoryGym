# OpenMLE-fast task

Task ID: `movies-dataset-for-feature-extracion-prediction@1`

Native metric: `MovieGenrePredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (461 bytes)
- `data/sample_submission.csv` (32717 bytes); columns: ["Id", "Predicted"]
- `data/test.csv` (541865 bytes); columns: ["Id", "Title", "Synopsis", "Cast", "Year", "Rating", "Votes", "Runtime", "IsSeries"]
- `data/train.csv` (2093744 bytes); columns: ["Id", "Title", "Synopsis", "Cast", "Year", "Rating", "Votes", "Runtime", "IsSeries", "Genre"]

## Public description

Competition: Multi-label Genre Prediction for IMDB Netflix Titles

Data provided (relative to public/):
- train.csv: inputs + labels (Genre pipe-delimited).
- test.csv: inputs only, no labels.
- sample_submission.csv: example submission (Id, Predicted).

Columns:
- Id, Title, Synopsis, Cast, Year, Rating, Votes, Runtime, IsSeries, Genre (train.csv only).

Submission format:
- CSV with columns Id and Predicted; genres pipe-delimited in canonical title case.
