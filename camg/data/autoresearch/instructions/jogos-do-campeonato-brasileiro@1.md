# OpenMLE-fast task

Task ID: `jogos-do-campeonato-brasileiro@1`

Native metric: `FootballOutcomeLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3089 bytes)
- `data/sample_submission.csv` (117034 bytes); columns: ["id", "home_win", "draw", "away_win"]
- `data/test.csv` (203338 bytes); columns: ["id", "competition", "datetime", "season", "round_stage", "home_team", "away_team", "home_team_state", "away_team_state", "home_country", "away_country", "home_team_canon", "away_team_canon"]
- `data/train.csv` (519299 bytes); columns: ["id", "competition", "datetime", "season", "round_stage", "home_team", "away_team", "home_team_state", "away_team_state", "home_country", "away_country", "home_team_canon", "away_team_canon", "target"]

## Public description

Brazilian Football Match Outcome Forecasting (3-way)

Problem statement
You are given historical match records from three major competitions that Brazilian clubs play: the national league (Brasileirão), the national cup (Copa do Brasil), and the continental competition (Libertadores). Your task is to predict the probability of each match outcome (home win, draw, away win) for future matches, using only the provided contextual information (teams, date, competition, round/stage, etc.).

Files provided
After running the provided preparation script, you will work with the following files:
- train.csv: Rows are matches with features and the target label.
- test.csv: Rows are matches with features only (no labels).
- sample_submission.csv: Example submission with the correct format and random but valid probabilities.

Do not reference or use any file other than train.csv, test.csv, and sample_submission.csv for your submission.

Data description
Each row corresponds to a single match. Columns include:
- id: Unique match identifier.
- competition: One of {brasileirao, copa_do_brasil, libertadores}.
- datetime: Match kickoff timestamp (local dataset timezone).
- season: Integer year of the season.
- round_stage: Round number or stage name depending on competition.
- home_team, away_team: Team names (as in the dataset).
- home_team_state, away_team_state: State abbreviations when available (mostly for Brasileirão and Copa do Brasil).
- home_country, away_country: Country codes when available (mostly for Libertadores).
- home_team_canon, away_team_canon: Canonicalized team identifiers useful for feature engineering.
- target (train only): One of {home_win, draw, away_win}.

Train/test split
A strict chronological split is used to avoid leakage from the future:
- Training: Matches up to and including the 2018 season.
- Test: Matches from seasons 2019 through 2021 (inclusive).
Only rows with complete labels and valid timestamps are included.

Task and submission format
For every row in test.csv, predict the probability of each outcome. Your submission must be a CSV with the following columns:
- id
- home_win
- draw
- away_win
Each row’s three probabilities must be non-negative and sum to 1 (within numerical tolerance).

Evaluation
Submissions are evaluated using multiclass log loss over the three outcomes in the order [home_win, draw, away_win]. Log loss rewards calibrated probabilities and handles class imbalance without thresholds.

Important notes
- The data includes matches from three competitions with different contexts and dynamics. Robust feature engineering across competitions and time can substantially improve performance.
- This problem is designed to be time-aware. Do not leak information from test seasons into training-derived features.
- Team naming across competitions is heterogeneous. Canonicalized names are provided to help you build historical form/strength features across competitions.
- The preparation script ensures that test labels are not present in test.csv and that all three outcome classes occur in the training set.
