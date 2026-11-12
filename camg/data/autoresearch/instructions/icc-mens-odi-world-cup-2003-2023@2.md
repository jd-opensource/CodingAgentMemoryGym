# OpenMLE-fast task

Task ID: `icc-mens-odi-world-cup-2003-2023@2`

Native metric: `NextBallWicketMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (833 bytes)
- `data/sample_submission.csv` (633774 bytes); columns: ["row_id", "next_is_wicket"]
- `data/test.csv` (2962427 bytes); columns: ["row_id", "match_id", "inning", "batting_team", "bowling_team", "over", "ball_in_over", "batter", "bowler", "runs_off_bat", "extras", "total_runs", "is_wicket", "wicket_type", "player_out", "current_score", "partnership_runs", "wickets_lost", "balls_bowled", "run_rate", "target_runs", "target_overs", "runs_remaining", "balls_remaining", "required_run_rate", "projected_score", "pressure_index"]
- `data/train.csv` (15196462 bytes); columns: ["row_id", "match_id", "inning", "batting_team", "bowling_team", "over", "ball_in_over", "batter", "bowler", "runs_off_bat", "extras", "total_runs", "is_wicket", "wicket_type", "player_out", "current_score", "partnership_runs", "wickets_lost", "balls_bowled", "run_rate", "target_runs", "target_overs", "runs_remaining", "balls_remaining", "required_run_rate", "projected_score", "pressure_index", "next_is_wicket"]

## Public description

ICC Men’s ODI World Cup Next-Ball Wicket Probability

Files
- train.csv: Training rows with features and the target next_is_wicket.
- test.csv: Test rows with the same features as train.csv but without next_is_wicket.
- sample_submission.csv: Example submission with columns [row_id, next_is_wicket].

Schema
- Both train.csv and test.csv include: row_id, match_id, inning, batting_team, bowling_team, over, ball_in_over, batter, bowler, runs_off_bat, extras, total_runs, is_wicket, wicket_type, player_out, current_score, partnership_runs, wickets_lost, balls_bowled, run_rate, target_runs, target_overs, runs_remaining, balls_remaining, required_run_rate, projected_score, pressure_index.
- train.csv additionally includes: next_is_wicket.

Submission
- Submit a CSV with columns: row_id,next_is_wicket for all rows in test.csv.
