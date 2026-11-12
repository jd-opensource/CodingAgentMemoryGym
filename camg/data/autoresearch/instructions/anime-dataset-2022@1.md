# OpenMLE-fast task

Task ID: `anime-dataset-2022@1`

Native metric: `AnimeRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (225 bytes)
- `data/sample_submission.csv` (78328 bytes); columns: ["anime_id", "Rating"]
- `data/test.csv` (2673461 bytes); columns: ["anime_id", "Name", "Japanese_name", "Description", "Tags", "Voice_actors", "staff", "Related_anime", "Related_Mange", "Type", "Studio", "Release_season", "Episodes", "Release_year", "End_year", "Content_Warning"]
- `data/train.csv` (10739164 bytes); columns: ["anime_id", "Name", "Japanese_name", "Description", "Tags", "Voice_actors", "staff", "Related_anime", "Related_Mange", "Type", "Studio", "Release_season", "Episodes", "Release_year", "End_year", "Content_Warning", "Rating"]

## Public description

Files in public/ directory:
- train.csv: Training data with features and Rating target.
- test.csv: Test data with features only (no Rating).
- sample_submission.csv: Example submission format with columns [anime_id, Rating].
