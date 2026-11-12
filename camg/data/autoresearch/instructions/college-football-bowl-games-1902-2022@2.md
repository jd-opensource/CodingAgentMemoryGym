# OpenMLE-fast task

Task ID: `college-football-bowl-games-1902-2022@2`

Native metric: `CollegeFootballAttendanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2342 bytes)
- `data/sample_submission.csv` (2245 bytes); columns: ["id", "attendance"]
- `data/test.csv` (17391 bytes); columns: ["id", "year", "date", "day", "sponsor", "bowl_name", "team_a", "team_b", "rank_a", "rank_b"]
- `data/train.csv` (99483 bytes); columns: ["id", "year", "date", "day", "sponsor", "bowl_name", "team_a", "team_b", "rank_a", "rank_b", "attendance"]

## Public description

College Football Bowl Attendance Forecasting (1902–2021)

Problem statement
Forecast the announced attendance for NCAA college football bowl games using only pregame context. You will build a model that, given the matchup, year/date/day, bowl, and sponsor, predicts game-day attendance. This mirrors real planning needs for venues and sponsors where demand must be estimated before kickoff.

Files
- train.csv: Training set with features and the target attendance.
- test.csv: Test set with the same features but without the target.
- sample_submission.csv: Example submission with valid formatting.

Target
- attendance: Integer count of attendees per game.

Features
Each row represents one bowl game. Postgame information (scores, MVP) is removed to avoid leakage. Teams are provided as an unordered pair with aligned ranks.
- id: Unique game identifier.
- year: Year of the game.
- date: Calendar date string of the game (as provided).
- day: Day-of-week string.
- sponsor: Bowl sponsor name (may be empty).
- bowl_name: Bowl name.
- team_a, team_b: Team names sorted alphabetically (unordered matchup).
- rank_a, rank_b: Pregame ranks aligned to team_a/team_b (float where present; missing otherwise).

Train/test split
- Time-based split to emulate future forecasting.
- Train: year ≤ 2015.
- Test: 2016 ≤ year ≤ 2021.

Evaluation
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) on attendance values:
RMSLE = sqrt( (1/N) * Σ_i ( log1p(max(p_i, 0)) − log1p(y_i) )^2 )
Notes:
- Use non-negative predictions; log1p is used for numerical stability and to balance relative error across different stadium sizes and eras.

Submission format
- CSV with exactly two columns and header:
  - id: the game identifier matching test.csv
  - attendance: your non-negative prediction
- One row per id in test.csv; IDs must match exactly.

Modeling tips (non-binding)
- Consider robust encodings for high-cardinality categorical features (teams, bowls, sponsors), e.g., regularized/target encoding with time-aware schemes.
- Handle distribution shift: include year/decade features or interactions like bowl × decade and sponsor × year.
- Treat ranks as numeric with missing indicators to capture early eras without polling.
- Tree-based ensembles and linear models with engineered features are strong baselines.
