# OpenMLE-fast task

Task ID: `rolling-stone-album-rankings@1`

Native metric: `RollingStoneAlbumRankMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3537 bytes)
- `data/sample_submission.csv` (2019 bytes); columns: ["row_id", "prediction"]
- `data/test.csv` (18413 bytes); columns: ["row_id", "rank_2003", "rank_2012", "release_year", "genre", "type", "weeks_on_billboard", "peak_billboard_position", "spotify_popularity", "artist_member_count", "artist_gender", "artist_birth_year_sum", "debut_album_release_year", "ave_age_at_top_500", "years_between"]
- `data/train.csv` (44502 bytes); columns: ["row_id", "rank_2003", "rank_2012", "release_year", "genre", "type", "weeks_on_billboard", "peak_billboard_position", "spotify_popularity", "artist_member_count", "artist_gender", "artist_birth_year_sum", "debut_album_release_year", "ave_age_at_top_500", "years_between", "y"]

## Public description

Competition: Predict Rolling Stone 2020 Album Rank (including Not-in-List)

Problem statement
Participants must build models to predict an album’s position on Rolling Stone’s 2020 “500 Greatest Albums of All Time” list, using album- and artist-level metadata and historical signals. Albums not appearing in the 2020 Top 500 are encoded as 501 (“not in list”). The target is an ordinal value in [1, 501], where lower is better.

Data description
You are provided with a tabular dataset consisting of album/artist descriptors, historical ranks, and popularity signals. The training set includes the target y (the 2020 rank or 501 if not on the list). The test set contains the same feature columns but no target. All rows represent albums; there are no image/audio files.

Feature columns included
- Historical ranks: rank_2003, rank_2012
- Album metadata: release_year, genre, type
- Popularity signals: weeks_on_billboard, peak_billboard_position, spotify_popularity
- Artist descriptors: artist_member_count, artist_gender, artist_birth_year_sum, debut_album_release_year, ave_age_at_top_500, years_between

Notes
- The following potentially leaky or identifier fields are excluded from the released train/test feature sets: rank_2020, differential, album_id, spotify_url, album, clean_name, sort_name.
- Missing values exist in several columns (e.g., genre, weeks_on_billboard, spotify_popularity). Handle them in your pipeline using train-only statistics.
- Special values: peak_billboard_position may include 201 to indicate “200+ / did not chart in top 200.” Treat this as worse than 200.

Target
- y ∈ [1, 501], where 501 encodes “not in the 2020 Top 500.” The training set includes y.

Files provided
- train.csv: Features + target y + row_id.
- test.csv: Features + row_id (no target).
- sample_submission.csv: Template with row_id and prediction columns.

Submission format
- A CSV with two columns:
  - row_id: Matches the row_id provided in test.csv.
  - prediction: Your model’s predicted ordinal rank for 2020 in [1, 501]. Real-valued predictions are permitted but will be clipped to [1, 501] and evaluated against integer targets; you may round to integers to reflect the ordinal nature.

Evaluation metric
- Mean Absolute Error (MAE) between your predictions and the true y values for the test set.
  - MAE is appropriate for ordinal targets, penalizing errors proportionally to their distance.
  - Encoding 501 as “not in list” preserves the ordinal structure and yields fair penalties when predicting in-list vs. out-of-list.

Recommended approach
- Data processing: robust handling of missing values, special sentinels, and mixed data types.
- Feature engineering: consider temporal recency (2020 − release_year), age at release, popularity intensity (weeks_on_billboard / peak_billboard_position clipped to [1, 201]), and interactions.
- Modeling: try tree-based methods, linear/regularized models, or ordinal regression approaches. Fit categorical encoders only on train data to avoid leakage.
- Evaluation: use cross-validation for model selection; ensure deterministic pipelines.

Train/test split
- The split is stratified by coarse rank buckets to stabilize evaluation across the ordinal space: Top 50, 51–200, 201–500, and 501 (“not in list”). The split is deterministic.

Important rules
- Do not use external data or identifier columns (e.g., URLs) to look up labels.
- Ensure your submission includes all test row_ids exactly once and contains valid numeric predictions.
