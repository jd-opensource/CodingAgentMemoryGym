# OpenMLE-fast task

Task ID: `tmdb-datasets@1`

Native metric: `TMDBRevenueMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (518 bytes)
- `data/sample_submission.csv` (9384 bytes); columns: ["id", "revenue"]
- `data/test.csv` (5590592 bytes); columns: ["id", "belongs_to_collection", "budget", "genres", "homepage", "imdb_id", "original_language", "original_title", "overview", "popularity", "poster_path", "production_companies", "production_countries", "release_date", "runtime", "spoken_languages", "status", "tagline", "title", "Keywords", "cast", "crew"]
- `data/train.csv` (22713242 bytes); columns: ["id", "belongs_to_collection", "budget", "genres", "homepage", "imdb_id", "original_language", "original_title", "overview", "popularity", "poster_path", "production_companies", "production_countries", "release_date", "runtime", "spoken_languages", "status", "tagline", "title", "Keywords", "cast", "crew", "revenue"]

## Public description

TMDB Revenue Forecast

Files
- train.csv: Training set with features and the target column revenue.
- test.csv: Test set with the same feature schema as train.csv, but without revenue.
- sample_submission.csv: Submission template with id,revenue for all rows in test.csv.

Evaluation
- Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) on revenue.

Submission format
- CSV with two columns and header: id,revenue.
- id must match exactly the ids in test.csv (no missing/extra/duplicate ids).
