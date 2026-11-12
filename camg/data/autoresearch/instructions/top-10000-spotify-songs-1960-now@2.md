# OpenMLE-fast task

Task ID: `top-10000-spotify-songs-1960-now@2`

Native metric: `SpotifyDecadeClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2613 bytes)
- `data/sample_submission.csv` (22026 bytes); columns: ["id", "decade"]
- `data/test.csv` (265438 bytes); columns: ["id", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature", "duration_ms", "explicit", "popularity", "artist_genres"]
- `data/train.csv` (1105128 bytes); columns: ["id", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature", "duration_ms", "explicit", "popularity", "artist_genres", "decade"]

## Public description

Competition title: Predict the Release Decade of a Song from Audio Features

Problem statement
Build a model that predicts the release decade of a song (one of: 1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s) using Spotify audio features and selected metadata that do not trivially reveal dates. The goal is to capture how musical characteristics evolved across eras and generalize to unseen songs.

Files provided
- train.csv: Feature table with one row per song and the ground-truth label column decade.
- test.csv: Same features as train.csv but without the decade column.
- sample_submission.csv: Example submission file with the required columns id and decade.

Target and identifiers
- Target: decade (categorical), one of {1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s}.
- Identifier: id (integer, unique per row). Use it exactly as provided when creating your submission.

Features
Columns are derived from Spotify audio analysis and selected metadata fields.
- Numeric audio features: danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature
- Additional numeric/binary: duration_ms, explicit (0/1), popularity
- Categorical text (optional to use): artist_genres (comma-separated list; can be used as multi-label features)

Notes
- Fields that directly or indirectly reveal dates (e.g., album_release_date, ISRC, URL fields, playlist curator/timestamps, and text likely to leak years) were removed during preparation.
- All information is tabular; no external media files are required.

Evaluation
- Metric: Macro-averaged F1 score across the eight decade classes.
- Why macro F1: It treats all decades equally and encourages balanced performance, which is important under class imbalance and concept drift.

Submission format
- A CSV file with two columns and a header row: id, decade
- id must exactly match the ids in test.csv
- decade must be one of: 1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s

Suggested workflow (non-exhaustive)
- Data processing: parse genre strings; handle missing values; standardize/normalize numeric features where helpful.
- Feature engineering: multi-hot encode frequent genres; derive features like tempo bins, loudness dynamics, and interactions.
- Modeling: try linear models, tree-based methods (GBMs, random forests), or neural nets; consider class weighting or calibrated probabilities.
- Evaluation: use stratified validation by decade; check per-class metrics to understand weaknesses.

Submission
- Produce a CSV named submission.csv with two columns: id, decade.
