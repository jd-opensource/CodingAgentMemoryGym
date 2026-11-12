# OpenMLE-fast task

Task ID: `hulu-movies-and-tv-shows@2`

Native metric: `HuluRatingsClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (890 bytes)
- `data/sample_submission.csv` (5237 bytes); columns: ["id", "rating"]
- `data/test.csv` (162570 bytes); columns: ["id", "type", "title", "country", "date_added", "release_year", "duration", "listed_in", "description"]
- `data/train.csv` (680072 bytes); columns: ["id", "type", "title", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]

## Public description

Hulu Content Rating Classification Challenge

Problem Statement
Your goal is to automatically infer parental guidance ratings for Hulu titles. Given metadata and synopsis of each title, predict one of the official content ratings: {G, PG, PG-13, R, NC-17, TV-Y, TV-Y7, TV-G, TV-PG, TV-14, TV-MA}.

Files
- train.csv: Training data including the target column rating.
- test.csv: Test data without the rating column.
- sample_submission.csv: A sample prediction file with the correct format.

Columns in train.csv and test.csv
- id: An anonymized integer identifier for each title.
- type, title, country, date_added, release_year, duration, listed_in, description: Input features.
- rating: Only in train.csv as the target label. Not present in test.csv.

Evaluation
- Metric: Macro-averaged F1 computed over hidden test labels.
- Submission format: CSV with exactly two columns: id,rating
