# OpenMLE-fast task

Task ID: `international-rugby-union-results-from-18712022@1`

Native metric: `RugbyOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (620 bytes)
- `data/sample_submission.csv` (17113 bytes); columns: ["match_id", "home_win", "draw", "away_win"]
- `data/test.csv` (28322 bytes); columns: ["match_id", "date", "home_team", "away_team", "competition", "stadium", "city", "country", "neutral", "world_cup"]
- `data/train.csv` (312872 bytes); columns: ["match_id", "date", "home_team", "away_team", "competition", "stadium", "city", "country", "neutral", "world_cup", "outcome"]

## Public description

International Rugby Union Outcome Forecasting

Files
- train.csv: training rows with columns [match_id, date, home_team, away_team, competition, stadium, city, country, neutral, world_cup, outcome]
- test.csv: test rows without labels with columns [match_id, date, home_team, away_team, competition, stadium, city, country, neutral, world_cup]
- sample_submission.csv: example submission with columns [match_id, home_win, draw, away_win]
- description.txt: this description

Submission format
- CSV with columns exactly: [match_id, home_win, draw, away_win].
- Probabilities per row should be non-negative and sum to 1.
