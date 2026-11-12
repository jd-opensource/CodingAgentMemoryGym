# OpenMLE-fast task

Task ID: `2021-nfl-predictions@2`

Native metric: `NFLMarginOfVictoryMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2566 bytes)
- `data/sample_submission.csv` (3112 bytes); columns: ["id", "mov"]
- `data/test.csv` (57564 bytes); columns: ["id", "date", "season", "neutral", "playoff", "team1", "team2", "elo1_pre", "elo2_pre", "qbelo1_pre", "qbelo2_pre", "qb1", "qb2", "qb1_value_pre", "qb2_value_pre", "qb1_adj", "qb2_adj"]
- `data/train.csv` (2834631 bytes); columns: ["id", "date", "season", "neutral", "playoff", "team1", "team2", "elo1_pre", "elo2_pre", "qbelo1_pre", "qbelo2_pre", "qb1", "qb2", "qb1_value_pre", "qb2_value_pre", "qb1_adj", "qb2_adj", "mov"]

## Public description

Title: NFL Margin of Victory Forecasting (2021 Test)

Problem statement
Using only information available before kickoff, predict the expected margin of victory (MOV) for team1 in NFL games. MOV is defined as score1 - score2. Train on historical games and generate one numeric prediction per game for the held-out 2021 season test set (including postseason).

Files
- train.csv: Training set with features and the target column mov.
- test.csv: Test set with the same features, without mov.
- sample_submission.csv: A sample submission with the correct format.

Columns
- id: Unique identifier for each game row. Use this to align your predictions to test rows.
- date: Game date (YYYY-MM-DD). Note: postseason games for the 2021 season occur in early 2022 by date but the season is 2021.
- season: Season year (integer). Train covers 1920–2020; test is 2021 (regular + postseason).
- neutral: Neutral-site indicator (0/1).
- playoff: Playoff round code (empty for regular season; examples include w, d, c, s for Wild Card, Divisional, Conference, Super Bowl).
- team1, team2: Team abbreviations.
- elo1_pre, elo2_pre: Pre-game team Elo ratings.
- qbelo1_pre, qbelo2_pre: Pre-game quarterback-adjusted Elo ratings.
- qb1, qb2: Starting quarterback identifiers (string; may be empty historically).
- qb1_value_pre, qb2_value_pre: Pre-game QB value estimates.
- qb1_adj, qb2_adj: Pre-game QB adjustment terms.
- mov (train only): Final margin of victory, score1 - score2. Ties are mov = 0.

Split
- Train: all seasons < 2021
- Test: season == 2021 (regular season and playoffs)

Evaluation
- Metric: Mean Absolute Error (MAE) on mov.
- Submission format: CSV with columns [id, mov]. The id values must match those in test.csv; mov must be a finite numeric value for every test row.

Guidance (non-binding)
- Feature engineering: Differences/spreads (e.g., elo1_pre - elo2_pre, qbelo1_pre - qbelo2_pre), indicators for neutral site and playoffs, and time-aware features you construct (e.g., rolling team form, rest days). Ensure any rolling stats only use data from games before each prediction date.
- Modeling: Linear models, gradient boosting, random forests, or neural tabular models can work well. Consider robust loss functions due to heavy-tailed margins.

Rules on leakage
- The released files do not include post-game columns or pre-computed win probabilities. Do not attempt to reconstruct post-game information or use information not available before kickoff.

Deliverable
- A CSV file with columns [id, mov], containing one prediction per row in test.csv.
