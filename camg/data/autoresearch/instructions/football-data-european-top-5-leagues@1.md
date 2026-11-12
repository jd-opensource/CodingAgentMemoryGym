# OpenMLE-fast task

Task ID: `football-data-european-top-5-leagues@1`

Native metric: `FootballOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/coaches.csv` (2661 bytes); columns: ["coach_id", "name", "team_id", "nationality"]
- `data/description.txt` (1789 bytes)
- `data/leagues.csv` (418 bytes); columns: ["league_id", "name", "country", "country_id", "icon_url", "cl_spot", "uel_spot", "relegation_spot"]
- `data/players.csv` (162629 bytes); columns: ["player_id", "team_id", "name", "position", "date_of_birth", "nationality"]
- `data/sample_submission.csv` (23957 bytes); columns: ["match_id", "p_home", "p_draw", "p_away"]
- `data/seasons.csv` (95 bytes); columns: ["season_id", "league_id", "year"]
- `data/stadiums.csv` (6018 bytes); columns: ["stadium_id", "name", "location", "capacity"]
- `data/teams.csv` (7198 bytes); columns: ["team_id", "name", "founded_year", "stadium_id", "league_id", "coach_id", "cresturl"]
- `data/test.csv` (11813 bytes); columns: ["match_id", "season_id", "league_id", "matchday", "home_team_id", "away_team_id", "utc_date"]
- `data/train.csv` (56132 bytes); columns: ["match_id", "season_id", "league_id", "matchday", "home_team_id", "away_team_id", "utc_date", "target"]
- `data/train_scores.csv` (15285 bytes); columns: ["match_id", "full_time_home", "full_time_away"]

## Public description

Euro5 Pre-Match Outcome Prediction (2023–24)

Problem statement
Predict pre-match three-way outcome probabilities (home win, draw, away win) for fixtures across Europe’s top five leagues during the 2023–24 season. Output well-calibrated probabilities for each test match using only information available before kickoff.

Files provided
- train.csv: Training fixtures with target labels. Columns: match_id, season_id, league_id, matchday, home_team_id, away_team_id, utc_date, target.
- test.csv: Test fixtures without labels. Same columns as train.csv except target is omitted.
- sample_submission.csv: Example submission file containing match_id and three probability columns p_home, p_draw, p_away.
- train_scores.csv: Full-time scores for training fixtures only. Columns: match_id, full_time_home, full_time_away.
- teams.csv, players.csv, coaches.csv, stadiums.csv, leagues.csv, seasons.csv: Metadata tables and keys for joins.

Target definition
The target (column 'target' in train.csv) is derived from full-time scores as:
- HOME_TEAM if home goals > away goals
- DRAW if home goals == away goals
- AWAY_TEAM if home goals < away goals

Train/test split
A temporally realistic split is applied independently per league: the last ~20% of matchdays are assigned to the test set, and earlier matchdays to the training set. This prevents label leakage and mimics real forecasting.

Evaluation
- Metric: Multiclass log loss (cross-entropy) over the outcomes {HOME_TEAM, DRAW, AWAY_TEAM}.
- Submission format: CSV with columns [match_id, p_home, p_draw, p_away]. Probabilities must be non-negative, finite, and sum to 1 within small numerical tolerance.

Deliverables
- A single CSV with columns [match_id, p_home, p_draw, p_away]. Ensure the match_id set exactly matches test.csv.
