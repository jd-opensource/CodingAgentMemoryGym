# OpenMLE-fast task

Task ID: `2025-premier-league-stats-matches-salaries@1`

Native metric: `PremierLeagueAttendanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (866 bytes)
- `data/player_possession_stats.csv` (43460 bytes); columns: ["player", "nation", "position", "team", "age", "90s", "touches", "deffensive_touches", "middle_touches", "attacking_touches", "attempted_take_ons", "successful_take_ons", "takeons_tackled", "carries", "total_distance_carried", "received"]
- `data/player_salaries.csv` (33957 bytes); columns: ["Player", "Nation", "Position", "Team", "Age", "Weekly", "Annual"]
- `data/player_stats.csv` (48435 bytes); columns: ["name", "nation", "position", "team", "age", "born", "played", "starts", "minutes", "goals", "assists", "penalty_kicks", "penalty_kick_attempts", "yellow", "red", "expected_goals", "progressive_carries", "progressive_passes", "received_progressive_passes"]
- `data/sample_submission.csv` (964 bytes); columns: ["id", "Attendance"]
- `data/standings.csv` (1473 bytes); columns: ["rank", "team", "win", "loss", "draw", "goals", "conceded", "points", "last5", "top_scorer", "keeper"]
- `data/team_possession_stats.csv` (1296 bytes); columns: ["team", "possession", "touches", "deffensive_touches", "middle_touches", "attacking_touches", "attempted_take_ons", "successful_take_ons", "carries", "total_distance_carried"]
- `data/team_salary.csv` (661 bytes); columns: ["team", "players", "weekly", "annual"]
- `data/team_stats.csv` (1328 bytes); columns: ["team", "players", "age", "possession", "goals", "assists", "penalty_kicks", "penalty_kick_attempts", "yellows", "reds", "expected_goals", "expected_assists", "progressive_carries", "progressive_passes"]
- `data/test.csv` (7996 bytes); columns: ["id", "week", "Day", "Date", "Time", "Home", "Away", "Venue", "Referee"]
- `data/train.csv` (25409 bytes); columns: ["id", "week", "Day", "Date", "Time", "Home", "Away", "Venue", "Referee", "Attendance"]

## Public description

Title: Premier League 2024/25 Match Attendance Forecasting

Problem statement
- Predict stadium attendance (integer) for Premier League fixtures.

Files in this public directory
- train.csv: Fixture-level data with target column Attendance and features including week, Day, Date, Time, Home, Away, Venue, Referee.
- test.csv: Same schema as train.csv except without the Attendance column.
- sample_submission.csv: Example submission with the required format (columns: id, Attendance).
- Auxiliary CSVs for feature engineering:
  - team_salary.csv
  - player_salaries.csv
  - team_stats.csv
  - team_possession_stats.csv
  - player_stats.csv
  - player_possession_stats.csv
  - standings.csv

Evaluation metric
- Root Mean Squared Log Error (RMSLE) computed on Attendance.

Submission format
- CSV with two columns: id, Attendance (non-negative integer recommended).
