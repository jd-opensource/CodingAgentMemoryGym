# OpenMLE-fast task

Task ID: `psl-2025-season-10-ball-by-ball-showdown@1`

Native metric: `PslNextBallRunsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (538 bytes)
- `data/sample_submission.csv` (96451 bytes); columns: ["row_id", "runs_pred"]
- `data/test.csv` (593526 bytes); columns: ["row_id", "match_id", "innings", "over", "ball", "phase", "is_powerplay", "batting_team", "bowling_team", "venue", "city", "date", "toss_winner", "toss_decision", "balls_per_over", "cum_runs", "wickets_down", "balls_bowled_so_far", "legal_balls_so_far", "run_rate_so_far", "start_over_runs", "start_over_wkts", "dots_in_over", "boundaries_in_over", "striker", "non_striker", "bowler", "striker_balls", "striker_sr", "bowler_conceded", "bowler_balls", "bowler_overs", "bowler_econ", "recent5_runs_sum", "recent5_runs_mean", "recent12_runs_sum", "recent12_runs_mean", "recent5_dots_sum", "recent5_boundaries_sum", "recent5_wkts_sum", "target_runs", "required_runs", "required_rr"]
- `data/train.csv` (1840727 bytes); columns: ["row_id", "match_id", "innings", "over", "ball", "phase", "is_powerplay", "batting_team", "bowling_team", "venue", "city", "date", "toss_winner", "toss_decision", "balls_per_over", "cum_runs", "wickets_down", "balls_bowled_so_far", "legal_balls_so_far", "run_rate_so_far", "start_over_runs", "start_over_wkts", "dots_in_over", "boundaries_in_over", "striker", "non_striker", "bowler", "striker_balls", "striker_sr", "bowler_conceded", "bowler_balls", "bowler_overs", "bowler_econ", "recent5_runs_sum", "recent5_runs_mean", "recent12_runs_sum", "recent12_runs_mean", "recent5_dots_sum", "recent5_boundaries_sum", "recent5_wkts_sum", "target_runs", "required_runs", "required_rr", "runs_total"]

## Public description

PSL Season 10 — Next-Ball Runs Prediction Challenge

Data description
- train.csv: Pre-ball context features plus the target runs_total.
- test.csv: The same features for held-out matches; runs_total is hidden.
- sample_submission.csv: Example submission with required columns ['row_id', 'runs_pred'].

Submission format
- CSV with exactly two columns: row_id and runs_pred.
- Include one prediction for each row_id in test.csv.

Evaluation
- Metric: Mean Absolute Error (MAE) between runs_pred and the true runs_total on the test set.
