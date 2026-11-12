# OpenMLE-fast task

Task ID: `basketball@1`

Native metric: `NbaRookieLongevityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (425 bytes)
- `data/sample_submission.csv` (2890 bytes); columns: ["Id", "5Yrs"]
- `data/test.csv` (17663 bytes); columns: ["Id", "GP", "MIN", "PTS", "FGS", "FGA", "3PM", "3PA", "FTM", "FTA", "OREB", "DREB", "AST", "STL", "BLK", "TOV"]
- `data/train.csv` (72376 bytes); columns: ["Id", "GP", "MIN", "PTS", "FGS", "FGA", "3PM", "3PA", "FTM", "FTA", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "5Yrs"]

## Public description

NBA Rookie Longevity — Predict 5-Year Career Survival from First-Season Box Scores

Files (relative to public/):
- train.csv
- test.csv
- sample_submission.csv

Columns:
- Identifier: Id
- Target: 5Yrs (binary; submit probabilities in [0,1])
- Features: GP, MIN, PTS, FGS, FGA, 3PM, 3PA, FTM, FTA, OREB, DREB, AST, STL, BLK, TOV

Split:
- Deterministic stratified 80/20 split by 5Yrs

Evaluation:
- Metric: LogLoss on 5Yrs
