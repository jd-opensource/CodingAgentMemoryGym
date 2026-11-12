# OpenMLE-fast task

Task ID: `nba-player-stats-1998-2025@1`

Native metric: `NBANextSeasonPointsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (473 bytes)
- `data/sample_submission.csv` (5736 bytes); columns: ["row_id", "pts_next"]
- `data/test.csv` (82109 bytes); columns: ["row_id", "Age", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
- `data/train.csv` (1931729 bytes); columns: ["row_id", "Age", "Pos", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "pts_next"]

## Public description

Title: NBA Next-Season PTS per Game Forecasting

Files in public/
- train.csv: Training data with row_id, features from season Y, and pts_next (target).
- test.csv: Test data with row_id and features from season Y.
- sample_submission.csv: Example submission file with row_id and pts_next.

Submission format
- A CSV with exactly two columns: row_id, pts_next.
- Every row_id in test.csv must appear exactly once in the submission.
- Predictions must be numeric and finite.
