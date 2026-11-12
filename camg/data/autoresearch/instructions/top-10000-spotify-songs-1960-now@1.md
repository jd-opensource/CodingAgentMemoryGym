# OpenMLE-fast task

Task ID: `top-10000-spotify-songs-1960-now@1`

Native metric: `SpotifyPopularityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (367 bytes)
- `data/sample_submission.csv` (107755 bytes); columns: ["Track URI", "Popularity"]
- `data/test.csv` (1439971 bytes); columns: ["Track URI", "Track Name", "Artist URI(s)", "Artist Name(s)", "Album URI", "Album Name", "Album Artist URI(s)", "Album Artist Name(s)", "Album Release Date", "Album Image URL", "Disc Number", "Track Number", "Track Duration (ms)", "Track Preview URL", "Explicit", "ISRC", "Added By", "Added At", "Artist Genres", "Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Time Signature", "Album Genres", "Label", "Copyrights"]
- `data/train.csv` (5778455 bytes); columns: ["Track URI", "Track Name", "Artist URI(s)", "Artist Name(s)", "Album URI", "Album Name", "Album Artist URI(s)", "Album Artist Name(s)", "Album Release Date", "Album Image URL", "Disc Number", "Track Number", "Track Duration (ms)", "Track Preview URL", "Explicit", "Popularity", "ISRC", "Added By", "Added At", "Artist Genres", "Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Time Signature", "Album Genres", "Label", "Copyrights"]

## Public description

Competition: Spotify Popularity Prediction (0–100)

Files in this public folder:
- train.csv: training data with target column 'Popularity'.
- test.csv: test data without the target.
- sample_submission.csv: a valid sample submission with columns ['Track URI', 'Popularity'].

Notes:
- Identifier column: 'Track URI'.
- Target column: 'Popularity' (range 0–100).
