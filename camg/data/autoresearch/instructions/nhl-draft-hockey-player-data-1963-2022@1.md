# OpenMLE-fast task

Task ID: `nhl-draft-hockey-player-data-1963-2022@1`

Native metric: `NHLDraftDebutMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3072 bytes)
- `data/sample_submission.csv` (30747 bytes); columns: ["id", "debut_probability"]
- `data/test.csv` (102624 bytes); columns: ["id", "year", "overall_pick", "team", "player", "nationality", "position", "age", "amateur_team"]
- `data/train.csv` (774085 bytes); columns: ["id", "year", "overall_pick", "team", "player", "nationality", "position", "age", "amateur_team", "nhl_debut"]

## Public description

Title: Predict NHL Debut from Draft-Day Data

Problem statement:
Given only information available on draft day, predict the probability that a drafted player will ever appear in at least one NHL game.

Target definition:
nhl_debut = 1 if the player played at least one NHL game (for skaters: games_played > 0; for goalies: goalie_games_played > 0). Otherwise nhl_debut = 0.

Data description:
You are provided with train and test tabular data built from historical NHL draft records. Features are strictly draft-day attributes:
- id: unique identifier for the draft pick
- year: draft year
- overall_pick: overall pick number
- team: drafting franchise
- player: player name (identifier only; do not use as a modeling feature or to link to external outcome data)
- nationality: two-letter nationality code
- position: player position (raw; you may canonicalize)
- age: player age at draft
- amateur_team: amateur team or program at time of draft

Train set contains an additional column:
- nhl_debut: binary target label as defined above

All post-draft outcome columns (e.g., games_played, goals, assists, point_shares, goalie statistics, to_year) are excluded from both train and test features to prevent label leakage.

Files:
- train.csv: training data with features and nhl_debut label (primarily draft years up to 2010)
- test.csv: test data with features only (primarily draft years 2011–2016)
- sample_submission.csv: example submission with the required format

Evaluation:
Submissions must provide, for every id in test.csv, a single column of predicted probabilities named debut_probability in [0, 1]. The leaderboard score is the ROC-AUC computed between your predicted probabilities and the hidden nhl_debut labels for the test set. ROC-AUC is threshold-free and handles class imbalance well, providing a fair and precise comparison of models.

Rules and guidance:
- Use only draft-day features provided in the files. Do not attempt to reconstruct labels or use any outcome variables.
- The player column is provided purely as an identifier; do not use it directly as a feature and do not join it to external outcome sources.
- External data is permitted for neutral feature engineering (e.g., mapping amateur programs to leagues), but must not directly encode post-draft outcomes.
- Recommended steps: data cleaning and typing, categorical encoding, position normalization, textual feature extraction from amateur_team, era-aware normalization, and ML models such as logistic regression, tree-based ensembles, calibrated classifiers, etc.

Submission format:
CSV with two columns and no index rows beyond the header line:
- id: matching the ids in test.csv
- debut_probability: a numeric probability in [0, 1]

Notes:
- The split uses earlier draft years for training and later years for testing to emulate realistic deployment on future drafts. Recent right-censored years are excluded from evaluation.
- Ensure robust handling of categorical values and missing entries. Careful preprocessing and feature engineering are essential for strong performance.
