# OpenMLE-fast task

Task ID: `tmdb-5000-movies@1`

Native metric: `MovieRevenuePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (718 bytes)
- `data/sample_submission.csv` (16167 bytes); columns: ["id", "revenue"]
- `data/test.csv` (9023451 bytes); columns: ["budget", "genres", "homepage", "id", "keywords", "original_language", "original_title", "overview", "production_companies", "production_countries", "runtime", "spoken_languages", "status", "tagline", "title", "cast", "crew"]
- `data/train.csv` (27885582 bytes); columns: ["budget", "genres", "homepage", "id", "keywords", "original_language", "original_title", "overview", "production_companies", "production_countries", "revenue", "runtime", "spoken_languages", "status", "tagline", "title", "cast", "crew"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (647 lines)
test.csv (647 lines)
train.csv (2584 lines)```

-> sample_submission.csv has 646 rows and 2 columns.
The columns are: id, revenue

-> test.csv has 646 rows and 17 columns.
The columns are: budget, genres, homepage, id, keywords, original_language, original_title, overview, production_companies, production_countries, runtime, spoken_languages, status, tagline, title... and 2 more columns

-> train.csv has 2583 rows and 18 columns.
The columns are: budget, genres, homepage, id, keywords, original_language, original_title, overview, production_companies, production_countries, revenue, runtime, spoken_languages, status, tagline... and 3 more columns
