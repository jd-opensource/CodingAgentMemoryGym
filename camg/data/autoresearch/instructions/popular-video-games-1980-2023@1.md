# OpenMLE-fast task

Task ID: `popular-video-games-1980-2023@1`

Native metric: `GamePopularityRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3336 bytes)
- `data/sample_submission.csv` (3184 bytes); columns: ["game_id", "times_listed"]
- `data/test.csv` (159424 bytes); columns: ["game_id", "title", "release_date", "team", "genres", "summary"]
- `data/train.csv` (761677 bytes); columns: ["game_id", "title", "release_date", "team", "genres", "summary", "times_listed"]

## Public description

Competition: Cold-Start Game Popularity Forecast

Problem statement
- Predict how many users will list a newly released video game on their collections/backlogs (times_listed) using only information available at or near release time. Train on historical games and generalize to future releases under temporal distribution shift.

Files provided
- train.csv: Training data with features and the target times_listed.
- test.csv: Test data with features only (no target).
- sample_submission.csv: Example of the required submission format with random but valid values.

Columns
- Shared feature columns (present in train.csv and test.csv):
  - game_id: Unique identifier for each game (integer). Use this to align predictions.
  - title: Game title (string).
  - release_date: Release date (ISO YYYY-MM-DD when available).
  - team: Development/publishing team as a Python-like list string, e.g., "['Nintendo', 'MercurySteam']".
  - genres: Genres as a Python-like list string, e.g., "['Adventure', 'RPG']".
  - summary: Short synopsis text (may be multilingual).
- Target column (only in train.csv):
  - times_listed: Non-negative integer count representing how many users listed the game.

What you must build
- A model that combines structured features (time, team, genres) and text (title, summary) to forecast popularity. You are encouraged to:
  - Parse list-like strings for team/genres using robust literal parsing.
  - Create temporal features from release_date (year, month, decade, seasonality).
  - Engineer textual features (bag-of-words/TF-IDF/embeddings) from title and summary.
  - Use suitable regressors (e.g., regularized linear models, gradient boosting, shallow neural nets). Blend models if helpful.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on times_listed.
- Definition: For each game i with ground truth y_i and prediction p_i,
  - e_i = log1p(max(p_i, 0)) − log1p(max(y_i, 0))
  - RMSLE = sqrt(mean(e_i^2)) over all test rows.
- Requirements:
  - Submission must be a CSV with exactly two columns and a header: game_id,times_listed.
  - Include each game_id from test.csv exactly once (order does not matter).
  - Predictions must be numeric and finite. Negative predictions are clipped to 0 before scoring.

Split policy and leakage prevention
- Temporal generalization is enforced with a chronological split: train contains earlier releases, test contains later releases. Only the columns listed above are provided; post-release engagement and rating signals were removed to prevent label leakage. Your solution should rely on information that could reasonably be known at or near release.

Baseline difficulty and tips
- Difficulty: Medium–Hard due to heavy-tailed targets, temporal drift, multi-label categorical parsing, and noisy/concise multilingual text.
- Practical tips:
  - Calibrate/regularize carefully; consider log-target models (fit on log1p(y)) and invert at inference.
  - Combine text + categorical + temporal features; frequency encodings for teams; multi-hot or target-agnostic encodings for genres.
  - Validate with time-aware splits to avoid optimistic estimates.

Submission format
- CSV with header and exactly two columns: game_id,times_listed
- The set of game_id must exactly match test.csv. Extra/missing/duplicated IDs or extra columns will be rejected.
