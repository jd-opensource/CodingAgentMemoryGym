# OpenMLE-fast task

Task ID: `200k-spotify-songs-light-dataset@2`

Native metric: `ExplicitnessDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3153 bytes)
- `data/sample_submission.csv` (1158162 bytes); columns: ["row_id", "explicit_probability"]
- `data/test.csv` (5137157 bytes); columns: ["row_id", "artist", "song", "emotion", "variance", "Genre", "Release Date", "Key", "Tempo", "Loudness", "Popularity", "Energy", "Danceability", "Positiveness", "Speechiness", "Liveness", "Acousticness", "Instrumentalness"]
- `data/test.jsonl` (16774684 bytes)
- `data/train.csv` (20029641 bytes); columns: ["artist", "song", "emotion", "variance", "Genre", "Release Date", "Key", "Tempo", "Loudness", "Popularity", "Energy", "Danceability", "Positiveness", "Speechiness", "Liveness", "Acousticness", "Instrumentalness", "Explicit"]

## Public description

Competition: Acoustic Explicitness Detection (Binary Classification)

Overview
Predict whether a song contains explicit content using only lightweight audio descriptors and metadata — no lyrics or audio required. You will build models that infer explicitness from per-track features such as genre, tempo, loudness, energy, valence, and more. The evaluation is performed on artists never seen during training to emphasize generalization and avoid memorization.

Files
- train.csv: Labeled training data with per-track features and the target.
- test.jsonl: Test data in JSON Lines format. Each line is one track record without the target.
- sample_submission.csv: Example submission file with the expected format and random, valid predictions.

Target
- Explicit (binary): 1 indicates explicit content, 0 indicates non-explicit.

Submission format
- CSV with the following columns:
  - row_id: Integer identifier for each test record.
  - explicit_probability: A real-valued probability in [0, 1] that the track is explicit.

Evaluation
- Metric: ROC-AUC on the explicit class (Explicit = 1).
  - Why ROC-AUC: It is threshold-free, robust to class imbalance, and measures your model’s ability to rank explicit tracks higher than non-explicit ones.

Data description (columns)
Each record contains the following columns (train.csv includes the Explicit target, test.jsonl omits it):
- artist: Artist or group name.
- song: Track title (identity only; do not rely on lyrics/text).
- emotion: Dominant emotion label derived from lyrics modeling (noisy; use at your discretion).
- variance: Variability measure across audio features.
- Genre: Primary musical genre (string).
- Release Date: Year of release (integer).
- Key: Musical key (e.g., "F Maj", "G min").
- Tempo: BPM.
- Loudness: Average loudness in dB (typically negative).
- Popularity: Popularity score (0–100).
- Energy: Energy level (0–100).
- Danceability: How danceable (0–100).
- Positiveness: Valence/positivity (0–100).
- Speechiness: Spoken-word presence (0–100).
- Liveness: Likelihood of being live (0–100).
- Acousticness: Acoustic score (0–100).
- Instrumentalness: Likelihood of instrumental (0–100).

Train/test split
- The split is performed by artist: all tracks of a given artist appear only in one of the sets. This enforces cold-start generalization on unseen artists.
- The split is deterministic and maintains full dataset scale (all available tracks are included).

Modeling notes
- This is a tabular ML problem. Strong baselines include gradient-boosted decision trees, tabular neural networks, and linear/logistic models with careful feature engineering.
- Useful feature engineering ideas:
  - Parse Key into pitch class and mode (Maj/min).
  - Normalize/standardize numeric features; winsorize outliers in Loudness if needed.
  - Clean/normalize categorical values (e.g., Genre casing).
  - Avoid using song titles as lexical features to prevent unintended leakage.

Deliverables
- Submit a CSV with row_id and explicit_probability as described above. Higher ROC-AUC is better.

Good luck, and enjoy modeling explicitness from acoustics and metadata!
