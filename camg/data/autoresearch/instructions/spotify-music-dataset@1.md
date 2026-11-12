# OpenMLE-fast task

Task ID: `spotify-music-dataset@1`

Native metric: `SpotifyPopularityRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2967 bytes)
- `data/sample_submission.csv` (21603 bytes); columns: ["sample_id", "track_popularity"]
- `data/test.csv` (119788 bytes); columns: ["sample_id", "acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence", "duration_ms", "key", "mode", "time_signature", "playlist_genre", "playlist_subgenre", "track_album_release_date", "release_year", "track_age_years"]
- `data/train.csv` (489333 bytes); columns: ["sample_id", "acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence", "duration_ms", "key", "mode", "time_signature", "playlist_genre", "playlist_subgenre", "track_album_release_date", "release_year", "track_age_years", "track_popularity"]

## Public description

Spotify Track Popularity Prediction

Problem statement
Build a model that predicts a song’s Spotify popularity score (0–100) using its audio features, basic musical attributes, lightweight playlist context, and release information. You will be given a single train/test split. Your task is to train on train.csv and submit predictions for the rows in test.csv.

Files provided
- train.csv — Training data with features and the target column track_popularity.
- test.csv — Test data with the same features as train.csv but without the target.
- sample_submission.csv — Example submission file with the correct format and random predictions.

Target
- track_popularity: real-valued score in [0, 100].

Features
All rows contain a subset of the following variables. Numerical columns are provided as numbers where available; categorical columns are strings. Missing values may be present.
- Audio features (numeric): acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence, duration_ms
- Musical attributes (numeric): key, mode, time_signature
- Playlist context (categorical): playlist_genre, playlist_subgenre
- Release info: track_album_release_date (string in YYYY or YYYY-MM-DD), plus engineered numeric fields release_year and track_age_years (years), where track_age_years is computed against a fixed reference year (2025) for determinism.

Identifier
- sample_id: Unique identifier for each row. Use this to align your predictions with test.csv.

Evaluation
- Metric: Root Mean Squared Error (RMSE) between your predictions and the ground truth track_popularity values.
- Implementation details: The evaluator joins your submission to the ground truth by sample_id. Predictions are validated as finite numbers and then clipped to [0, 100] before scoring to ensure numerical stability.

Submission format
Submit a CSV with the following columns and no index:
- sample_id
- track_popularity
Rows must correspond exactly to the sample_id values in test.csv.

Train/test split summary
- One deterministic 80/20 split.
- Stratified by the combination of playlist_genre and a release_year bin (e.g., <=1980, 1980s, 1990s, 2000s, 2010s, 2020s) to preserve genre/time distributions.
- Grouping ensures a single track does not appear in both train and test.

Recommended approaches
- Data processing: Handle missing values; consider transforming skewed features (e.g., loudness), and standardizing or scaling numeric features when appropriate.
- Feature engineering: Interactions between audio features and genre/era can help. Try encoding playlist_genre/subgenre, and experimenting with temporal features based on release year and age.
- Modeling: Strong baselines include gradient-boosted trees, regularized linear models, random forests, and shallow neural networks.
- Validation: Although only a single train/test split is provided, you may create your own internal cross-validation scheme for model selection.
