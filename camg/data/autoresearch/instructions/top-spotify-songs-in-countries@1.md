# OpenMLE-fast task

Task ID: `top-spotify-songs-in-countries@1`

Native metric: `SpotifySkipPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3133 bytes)
- `data/sample_submission.csv` (318598 bytes); columns: ["row_id", "skipped"]
- `data/test.csv` (3843849 bytes); columns: ["row_id", "ts", "platform", "spotify_track_uri", "track_name", "artist_name", "album_name", "reason_start", "shuffle"]
- `data/train.csv` (14765131 bytes); columns: ["ts", "platform", "spotify_track_uri", "track_name", "artist_name", "album_name", "reason_start", "shuffle", "skipped"]

## Public description

Competition: Spotify Skip Prediction (Time-Ordered)

Problem statement
Given the context available exactly at playback start, predict the probability that a Spotify play will be skipped by the user. Each row corresponds to one play event. The target is skipped (1 if the play was skipped, 0 otherwise).

Files provided
- train.csv: Labeled events for model development. Columns:
  - ts: UTC timestamp when playback started (YYYY-MM-DD HH:MM:SS)
  - platform: Playback platform/device (e.g., web player)
  - spotify_track_uri: Track identifier (string)
  - track_name: Track title (string)
  - artist_name: Artist name (string)
  - album_name: Album name (string)
  - reason_start: What triggered playback (e.g., autoplay, clickrow)
  - shuffle: Whether shuffle mode was on (TRUE/FALSE)
  - skipped: Target label (1 if skipped, 0 otherwise)

- test.csv: Unlabeled events for prediction. Columns:
  - row_id: Unique identifier for the row to be used in your submission
  - ts, platform, spotify_track_uri, track_name, artist_name, album_name, reason_start, shuffle (same definitions as in train.csv)

- sample_submission.csv: Example submission with the correct format and random probabilities.

What is not included (to avoid leakage)
- Columns such as ms_played and reason_end are not present in train/test files because they are known only after playback starts and would leak the outcome.

Task and expectations
- Build a model that estimates P(skipped=1 | context at start) for each test row.
- You are encouraged to use time-aware feature engineering and robust encodings for high-cardinality fields (e.g., frequency/target encodings with proper cross-validation), and to consider class imbalance.

Evaluation
- Primary metric: Average Precision (AP) for the positive class (skipped = 1). Formally, let y be the true binary labels and s the submitted probabilities. Sort rows by s descending; let P@k be the precision at each rank k where yk = 1. AP = average of P@k over all positives. AP ranges from 0 to 1 and is sensitive to ranking quality under imbalance.

Submission format
- A CSV file with exactly two columns and a header:
  - row_id: Must match the row_id values found in test.csv
  - skipped: A probability in [0, 1]
- Do not include any other columns. The order of rows does not matter, but all row_id values from test.csv must be present exactly once.

Data split
- The split is strictly chronological to emulate real deployment: training rows precede the test period. This introduces realistic concept drift and cold-start cases for tracks/artists appearing for the first time in the test period.

Modeling guidance (non-exhaustive)
- Parse ts into time-of-day and calendar features (hour, day-of-week, month, year; cyclical encodings recommended).
- Consider encodings and historical aggregates for spotify_track_uri, track_name, artist_name, album_name, platform, reason_start.
- Handle class imbalance via appropriate loss functions, sampling, or thresholding.
- Validate with time-aware splits (e.g., forward-chaining) to avoid leakage.

Good luck and have fun tackling this real-world skip prediction problem!
