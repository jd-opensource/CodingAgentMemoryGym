# OpenMLE-fast task

Task ID: `ipl-complete-dataset-20082020@1`

Native metric: `IPLWinProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1280 bytes)
- `data/sample_submission.csv` (546772 bytes); columns: ["row_id", "win_probability"]
- `data/test.csv` (8662046 bytes); columns: ["row_id", "match_id", "inning", "over", "ball", "batting_team", "bowling_team", "batter", "non_striker", "bowler", "date", "city", "venue", "toss_winner", "toss_decision", "match_type", "runs_so_far", "wickets_fallen", "legal_balls_bowled", "legal_balls_remaining", "overs_completed", "balls_in_over", "is_chasing", "target_runs", "runs_required", "current_run_rate", "required_run_rate"]
- `data/train.csv` (51772930 bytes); columns: ["row_id", "match_id", "inning", "over", "ball", "batting_team", "bowling_team", "batter", "non_striker", "bowler", "date", "city", "venue", "toss_winner", "toss_decision", "match_type", "runs_so_far", "wickets_fallen", "legal_balls_bowled", "legal_balls_remaining", "overs_completed", "balls_in_over", "is_chasing", "target_runs", "runs_required", "current_run_rate", "required_run_rate", "win"]

## Public description

Competition: IPL Ball-by-Ball Win Probability Prediction

Problem statement
Given the full game state at the start of each delivery in an IPL match, predict the probability that the batting team at that delivery will eventually win the match.

Data description
You are provided with preprocessed CSV files:
- train.csv: One row per delivery with contextual features and the binary label win.
- test.csv: Same features as train.csv, but without the label. Predict win_probability for each row.

Key columns include:
- row_id (identifier)
- match_id, inning, over, ball
- batting_team, bowling_team, batter, non_striker, bowler
- date, city, venue, toss_winner, toss_decision, match_type
- runs_so_far, wickets_fallen, legal_balls_bowled, legal_balls_remaining, overs_completed, balls_in_over
- is_chasing, target_runs, runs_required, current_run_rate, required_run_rate

Train/test split
- Split by match_id to avoid leakage across deliveries within a match.
- Chronological split: Train consists of earlier seasons; test consists of the most recent seasons.

Submission format
- CSV with exactly two columns: row_id, win_probability.
- Each row_id from test.csv must appear once; win_probability in [0, 1].

Evaluation metric
- Binary LogLoss (cross-entropy) over test deliveries.
