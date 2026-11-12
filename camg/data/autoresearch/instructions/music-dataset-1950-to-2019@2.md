# OpenMLE-fast task

Task ID: `music-dataset-1950-to-2019@2`

Native metric: `LyricsYearPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (354 bytes)
- `data/sample_submission.csv` (81277 bytes); columns: ["song_id", "release_year"]
- `data/test.csv` (2648780 bytes); columns: ["song_id", "lyrics", "genre", "len"]
- `data/train.csv` (10686627 bytes); columns: ["song_id", "lyrics", "genre", "len", "release_year"]

## Public description

EraTrace: Predict a song's release year from its lyrics

Files
- train.csv (columns: song_id, lyrics, genre, len, release_year)
- test.csv (columns: song_id, lyrics, genre, len)
- sample_submission.csv (columns: song_id, release_year)

Evaluation
- Metric: Mean Absolute Error (MAE) on release_year.
- Submit a CSV matching sample_submission.csv format.
