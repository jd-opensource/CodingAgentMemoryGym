# OpenMLE-fast task

Task ID: `top-video-games-19952021-metacritic@1`

Native metric: `MetacriticScoreMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2430 bytes)
- `data/sample_submission.csv` (41961 bytes); columns: ["game_id", "meta_score"]
- `data/test.csv` (1864766 bytes); columns: ["game_id", "name", "platform", "release_year", "summary"]
- `data/train.csv` (10001815 bytes); columns: ["game_id", "name", "platform", "release_year", "summary", "meta_score"]

## Public description

Title: Predicting Metacritic Critic Scores from Game Metadata and Descriptions (1995–2021)

Problem statement
- Goal: Given a video game’s metadata and textual description, predict its Metacritic critic metascore (0–100).
- You will train on historical releases and predict scores for future releases, requiring generalization across time and platforms.

Data description
- Provided files:
  - train.csv: Training data with features and the target.
  - test.csv: Test data with features only.
  - sample_submission.csv: Example submission with the correct format.
- Columns:
  - game_id: Unique integer identifier for each record.
  - name: Title of the game.
  - platform: Platform on which the game was released (e.g., PlayStation 4, PC, Switch).
  - release_year: Year the game was released (integer).
  - summary: Textual description/summary from Metacritic.
  - meta_score: Target variable (only in train.csv).
- Notes:
  - Text fields may be long and vary in style and structure.
  - Platform strings have been standardized (trimmed) and release_date has been converted to release_year.
  - Duplicate exact rows are removed to avoid leakage.

Training/test split
- Time-aware split to emulate forward prediction:
  - Train: releases from 1995–2018.
  - Test: releases from 2019–2021.
- All rows use a deterministic game_id assignment to preserve correspondence.

Task and expectations
- This is a regression task on meta_score (continuous, 0–100).
- Recommended approaches include:
  - Data processing: clean text (lowercase, punctuation handling), handle missing summaries as empty strings.
  - Feature engineering: encode platform as categorical, extract n-grams or TF-IDF from name/summary, add simple temporal features from release_year.
  - Modeling: linear models, gradient boosting over engineered features, transformer-based text models, or multimodal architectures combining text and tabular inputs.

Evaluation metric
- Root Mean Squared Error (RMSE) between your predictions and the ground truth metascores on the test set.
- RMSE is calculated as sqrt(mean((y_pred - y_true)^2)). Lower is better.

Submission format
- Submit a CSV with the following columns:
  - game_id
  - meta_score
- The file must include exactly one row per game_id present in test.csv, with meta_score as a finite numeric prediction (recommended range 0–100).

Final data files
- train.csv
- test.csv
- sample_submission.csv
