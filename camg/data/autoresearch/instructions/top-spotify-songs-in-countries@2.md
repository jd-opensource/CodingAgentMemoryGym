# OpenMLE-fast task

Task ID: `top-spotify-songs-in-countries@2`

Native metric: `SpotifyEndReasonMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4393 bytes)
- `data/sample_submission.csv` (407118 bytes); columns: ["row_id", "reason_end"]
- `data/test.csv` (2873909 bytes); columns: ["row_id", "ts", "platform", "spotify_track_uri", "track_name", "artist_name", "album_name", "reason_start", "shuffle"]
- `data/train.csv` (17239383 bytes); columns: ["row_id", "ts", "platform", "spotify_track_uri", "track_name", "artist_name", "album_name", "reason_start", "shuffle", "reason_end"]

## Public description

Competition: Predict Spotify Playback End Reason (Time-Aware Multiclass Classification)

Problem statement
Given a Spotify play at the moment it starts, predict how that playback will end (reason_end). Each row represents one playback start event from a single user over 2013–2024. Your task is to build a model that, using only information available at start time, outputs the most likely end reason for each event in the test set. This is a time-series, imbalanced, multiclass classification problem with distribution shift over years.

Target
- reason_end: categorical label describing how playback ended (e.g., trackdone, fwdbtn, endplay, logout, backbtn, unexpected-exit-while-paused, remote, unexpected-exit, clickrow, nextbtn, appload, popup, reload, trackerror, unknown, etc.).

Input features provided
Use only information available at start time. The final competition files include the following columns:
- row_id: unique identifier for each row (integer), provided for both train and test and used to join predictions.
- ts: timestamp string for when playback started (UTC-like local format). You may derive calendar/time features from it.
- platform: categorical device/platform string.
- spotify_track_uri: track identifier string.
- track_name: track title string.
- artist_name: artist name string.
- album_name: album name string.
- reason_start: categorical indicator of how playback started (e.g., autoplay, clickrow, nextbtn, trackdone, etc.).
- shuffle: boolean-like string flag ("TRUE"/"FALSE").

Intentionally excluded from model inputs due to target leakage
- ms_played and skipped are consequences of how playback ended; these are removed from the competition files.

Files provided
- train.csv: training data with all feature columns above plus the target column reason_end.
- test.csv: test data with the same feature columns as train.csv except reason_end is withheld.
- sample_submission.csv: a template submission with two columns [row_id, reason_end].

Submission format
- CSV with exactly two columns in this order: row_id, reason_end.
- One row per row_id in test.csv; row_id must match exactly.
- reason_end must be one of the valid class labels present in the data.

Evaluation
- Primary metric: macro-averaged F1 score over all classes present in the test set.
  - For each class c: F1_c = 2 * precision_c * recall_c / (precision_c + recall_c) with 0/0 treated as 0.
  - Macro-F1 = mean of F1_c across all distinct classes in the test set.
- Rationale: reason_end is highly imbalanced (classes like trackdone and fwdbtn dominate). Macro-F1 weights all classes equally, rewarding models that capture minority modes (e.g., interruptions, errors) rather than optimizing only for the majority.

Train/test split (information for understanding only)
- Chronological split: training contains earlier events; test contains later events to simulate forward-looking prediction under temporal drift.
- The split is chosen so that every class that appears in test also appears at least once in train.
- Exact cutoff and files are produced by the provided prepare.py script and are fixed for this competition.

Modeling guidance (non-binding)
- Time features: Parse ts into year/month/day/hour, day-of-week, weekend/holiday flags (if derived from date only), and cyclical encodings.
- Categorical signals: platform, reason_start, shuffle.
- High-cardinality entities: spotify_track_uri, track_name, artist_name, album_name may benefit from hashing, frequency encoding, regularized target encoding, or learned embeddings. Use time-aware validation to avoid leakage for any history-based encodings.
- Optional context: Derive sessionization from ts gaps (e.g., 30-minute inactivity threshold), position-in-session, and causal historical propensities computed only from prior data.
- Validation: Use rolling/chronological cross-validation splits to reflect temporal shift; avoid random CV.

Rules and expectations
- Do not attempt to use information that occurs after the playback starts (e.g., ms_played, skipped, or any engineered proxy of the outcome from the future).
- Keep deterministic experiments when possible for reproducibility.

Deliverables checklist
- Submission must contain: row_id, reason_end for every row in test.csv.
- Metric is macro F1; higher is better.

Good luck and have fun tackling this challenging, real-world time-aware classification task!
