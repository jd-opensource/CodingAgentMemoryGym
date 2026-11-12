# OpenMLE-fast task

Task ID: `nepal-t20i-2014-present-ball-by-ball-data@1`

Native metric: `NepalT20BallOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (322 bytes)
- `data/sample_submission.csv` (896943 bytes); columns: ["row_id", "0", "1", "2", "3", "4", "5+", "6", "W"]
- `data/test.csv` (559853 bytes); columns: ["row_id", "match_no", "innings", "event_name", "event_stage", "batting_team", "bowling_team", "over", "ball_number", "bowler", "batsman", "non_striker", "super_over"]
- `data/train.csv` (2031297 bytes); columns: ["row_id", "match_no", "innings", "event_name", "event_stage", "batting_team", "bowling_team", "over", "ball_number", "bowler", "batsman", "non_striker", "super_over", "outcome"]

## Public description

Competition: Next-Ball Outcome Forecasting in Nepal T20Is

Public files:
- train.csv
- test.csv
- sample_submission.csv

Problem: Predict probabilities over classes {0,1,2,3,4,5+,6,W} for each ball.
Submission format: CSV with columns [row_id, 0, 1, 2, 3, 4, 5+, 6, W]; rows must sum to 1.
Evaluation: Multiclass log loss.
