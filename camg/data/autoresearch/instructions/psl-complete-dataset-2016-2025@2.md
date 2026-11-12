# OpenMLE-fast task

Task ID: `psl-complete-dataset-2016-2025@2`

Native metric: `PslRunOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (280 bytes)
- `data/sample_submission.csv` (1862324 bytes); columns: ["row_id", "prob_0", "prob_1", "prob_2", "prob_3", "prob_4", "prob_5plus"]
- `data/test.csv` (3329421 bytes); columns: ["row_id", "match_id", "season", "date", "venue", "inning", "batting_team", "bowling_team", "over", "ball", "batter", "bowler", "non_striker", "match_type", "umpire_1", "umpire_2", "match_phase", "delivery_no", "balls_bowled_so_far", "score_before", "wickets_before", "runs_last_12_balls", "dots_streak", "boundaries_streak", "run_rate_so_far", "target", "runs_required", "balls_remaining", "required_run_rate"]
- `data/train.csv` (12758510 bytes); columns: ["row_id", "match_id", "season", "date", "venue", "inning", "batting_team", "bowling_team", "over", "ball", "batter", "bowler", "non_striker", "match_type", "umpire_1", "umpire_2", "match_phase", "delivery_no", "balls_bowled_so_far", "score_before", "wickets_before", "runs_last_12_balls", "dots_streak", "boundaries_streak", "run_rate_so_far", "target", "runs_required", "balls_remaining", "required_run_rate", "run_class"]

## Public description

Files in this dataset (relative to public/):
- train.csv: Training features with target column 'run_class' (classes: 0,1,2,3,4,5plus)
- test.csv: Test features without targets
- sample_submission.csv: Sample submission with columns row_id, prob_0..prob_5plus that sum to 1 per row
