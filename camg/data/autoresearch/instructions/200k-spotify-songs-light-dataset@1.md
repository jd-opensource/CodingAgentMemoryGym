# OpenMLE-fast task

Task ID: `200k-spotify-songs-light-dataset@1`

Native metric: `SpotifyPopularityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (663 bytes)
- `data/sample_submission.csv` (1127188 bytes); columns: ["id", "Popularity"]
- `data/test.csv` (4938034 bytes); columns: ["id", "artist", "song", "emotion", "variance", "Genre", "Release Date", "Key", "Tempo", "Loudness", "Explicit", "Energy", "Danceability", "Positiveness", "Speechiness", "Liveness", "Acousticness", "Instrumentalness"]
- `data/train.csv` (20579315 bytes); columns: ["artist", "song", "emotion", "variance", "Genre", "Release Date", "Key", "Tempo", "Loudness", "Explicit", "Energy", "Danceability", "Positiveness", "Speechiness", "Liveness", "Acousticness", "Instrumentalness", "Popularity"]

## Public description

Spotify Track Popularity Generalization Challenge

Files in this directory:
- train.csv: Labeled training set (features + Popularity).
- test.csv: Unlabeled test set (id + features; no Popularity).
- sample_submission.csv: Example submission with required columns (id,Popularity).

Columns:
Shared feature columns across train/test: artist, song, emotion, variance, Genre, Release Date, Key, Tempo, Loudness, Explicit, Energy, Danceability, Positiveness, Speechiness, Liveness, Acousticness, Instrumentalness
Label column (train.csv only): Popularity (0–100)
Submission: Provide a CSV with exactly two columns: id,Popularity. Values will be clipped to [0,100].
