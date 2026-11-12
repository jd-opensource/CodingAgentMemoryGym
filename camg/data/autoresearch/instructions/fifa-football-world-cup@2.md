# OpenMLE-fast task

Task ID: `fifa-football-world-cup@2`

Native metric: `FifaAttendanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3918 bytes)
- `data/sample_submission.csv` (2248 bytes); columns: ["match_id", "attendance"]
- `data/test.csv` (17475 bytes); columns: ["match_id", "home_team", "away_team", "venue", "round", "host", "year", "date", "dayofweek", "month", "is_host_home", "is_host_away", "teams_field_size", "matches_in_tournament", "home_rank_2022", "away_rank_2022", "home_points_2022", "away_points_2022"]
- `data/train.csv` (112860 bytes); columns: ["match_id", "home_team", "away_team", "venue", "round", "host", "year", "date", "dayofweek", "month", "is_host_home", "is_host_away", "teams_field_size", "matches_in_tournament", "home_rank_2022", "away_rank_2022", "home_points_2022", "away_points_2022", "attendance"]

## Public description

World Cup Match Attendance Forecasting (1930–2022)

Overview
- Task: Predict the stadium attendance for FIFA World Cup matches using only information available before kickoff.
- Target: attendance (a nonnegative real number of spectators) for each match in the test set.
- Split: Chronological. Train = 1930–2014 tournaments, Test = 2018–2022 tournaments (128 matches). This mirrors real-world forecasting for recent tournaments while preventing leakage across eras.

Files provided
- train.csv: Training rows with features and the target column attendance.
- test.csv: Test rows with the same features (without attendance).
- sample_submission.csv: Valid example submission with random predictions and correct schema.

Columns
Each row represents a single match. All fields are pre-match and safe to use. Unless noted, columns are strings.
- match_id: Unique identifier for the match, formatted as "<year>_<seq>".
- home_team, away_team: Team names (historical entities preserved, e.g., West Germany, USSR).
- venue: Stadium and city as recorded pre-match.
- round: Competition round (e.g., Group Stage, Round of 16, Quarter-finals, Semi-finals, Final, Third-place match).
- host: Host nation(s) string for the tournament year. For co-hosted years, both hosts appear, separated by a comma.
- year: Tournament year (integer).
- date: ISO 8601 date (YYYY-MM-DD) of the match.
- dayofweek: Day name (e.g., Monday).
- month: Integer month (1–12).
- is_host_home, is_host_away: Boolean flags for whether the team is the host nation in that year.
- teams_field_size: Total number of teams in the tournament (integer; era/context feature).
- matches_in_tournament: Total number of matches in the tournament (integer; era/context feature).
- home_rank_2022, away_rank_2022: FIFA world rankings (as of 2022-10-06) for 2022 matches only; NaN for all other years.
- home_points_2022, away_points_2022: FIFA ranking points (as of 2022-10-06) for 2022 matches only; NaN for all other years.
- attendance [train only]: Number of spectators in the stadium (nonnegative real number).

Important notes
- All features are pre-match. No realized in-game or post-tournament outcomes are included.
- Ranking features are provided only for 2022 rows; do not impute them using outcomes.
- High-cardinality categoricals (teams, venue) and era shifts are part of the challenge.

Evaluation
- Metric: Root Mean Squared Log Error (RMSLE) using the ln(1 + y) convention.
  - For each match i with true attendance yi and prediction pi (both nonnegative):
    RMSLE = sqrt(mean((ln(1 + yi) − ln(1 + pi))^2))
  - Why: Attendance is strictly nonnegative and highly skewed. RMSLE emphasizes relative error and is robust to large outliers.

Submission format
- A single CSV file with exactly two columns in this order:
  - match_id
  - attendance
- Include one row per match_id present in test.csv.
- Predictions must be numeric and ≥ 0. Decimals are allowed.

Design guidance and baseline ideas
- Time-aware modeling: Use train (≤2014) only to fit features/encoders; apply to test (2018–2022). Avoid leakage from future eras when computing aggregates.
- Feature engineering ideas (optional):
  - Extract temporal context (weekday, month), host-team flags, knockout vs group tiers from round, venue/team historical aggregates computed using only prior years.
  - Target/impact encoding or regularized encoding for high-cardinality venue/team features.
  - Use ranking features for 2022 rows to proxy team drawing power; leave them missing for earlier years.
- Modeling: Gradient boosting trees, regularized GLMs on log-scale, and modern tabular deep models can all perform well.

Final deliverables participants will use
- train.csv
- test.csv
- sample_submission.csv

Your goal
- Build a model that generalizes across eras, captures venue/team/round effects, and produces accurate attendance forecasts on the 2018 and 2022 World Cups.
