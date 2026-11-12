# OpenMLE-fast task

Task ID: `twitchdata@2`

Native metric: `TwitchFollowerGrowthMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2484 bytes)
- `data/sample_submission.csv` (4393 bytes); columns: ["row_id", "Followers gained"]
- `data/test.csv` (13024 bytes); columns: ["row_id", "Watch time(Minutes)", "Stream time(minutes)", "Peak viewers", "Average viewers", "Followers", "Views gained", "Partnered", "Mature", "Language"]
- `data/train.csv` (57862 bytes); columns: ["row_id", "Watch time(Minutes)", "Stream time(minutes)", "Peak viewers", "Average viewers", "Followers", "Views gained", "Partnered", "Mature", "Language", "Followers gained"]

## Public description

Top Streamers Follower Growth Prediction

Problem statement:
Predict annual follower growth for Twitch channels using operational and engagement signals. Given tabular features describing each channel’s past-year activity and audience, estimate the number of followers gained over the same period for unseen channels.

Data description:
The competition provides tabular files with one row per channel.
- train.csv: feature columns plus the target column.
- test_data.csv: feature columns only (no target).
- sample_submission.csv: a template showing the expected submission format.

Columns
- row_id: unique identifier for each row. Present in train.csv and test_data.csv. Use it to align predictions to test_data rows.
- Features: Watch time(Minutes), Stream time(minutes), Peak viewers, Average viewers, Followers, Views gained, Partnered, Mature, Language.
- Target: Followers gained (in train.csv only).

Important notes
- The Channel field is excluded to avoid identity-based leakage; build models from quantified behavioral and audience signals.
- Numeric features are heavy-tailed; log1p transformations and robust models can help. One-hot encode Language, treat Partnered and Mature as binary indicators, and consider interaction effects.

Train/test split
- The data are split deterministically into train/test with approximate stratification by Language to preserve distributional diversity in both sets.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Followers gained.
- Definition: For N test rows with true values yi and predictions pi, RMSLE = sqrt( (1/N) * sum_i ( log1p(max(yi, 0)) − log1p(max(pi, 0)) )^2 ).
- Rationale: Follower growth spans orders of magnitude. RMSLE emphasizes relative accuracy across small and large channels and is robust to zeros.

Submission format
- CSV file with two columns: row_id and Followers gained.
- row_id must match exactly the row_id values in test_data.csv; provide one prediction per test row.

What’s provided
- train.csv: features + Followers gained.
- test_data.csv: features only.
- sample_submission.csv: row_id and placeholder Followers gained values.

Guidance to participants
- Make full use of the provided features; no need to filter the scale.
- Apply careful preprocessing (e.g., log1p, encoding) and feature engineering.
- Train and evaluate models with cross-validation if desired; the leaderboard uses RMSLE on the held-out test set.
- Ensure predictions are non-negative real numbers.
