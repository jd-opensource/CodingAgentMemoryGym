# OpenMLE-fast task

Task ID: `ipl-20082024-ball-by-ball-with-extra-columns@1`

Native metric: `NextBallOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (800 bytes)
- `data/sample_submission.csv` (4938474 bytes); columns: ["row_id", "prob_0", "prob_1", "prob_2", "prob_3", "prob_4", "prob_5", "prob_6", "prob_7_plus"]
- `data/test.csv` (7199508 bytes); columns: ["Match_ID", "Date", "Season", "Batting team", "Bowling team", "Innings No", "Ball No", "Bowler", "Striker", "Non Striker", "batsman_run", "extras", "type of extras", "total_runs", "score/wicket", "wicket_confirmation", "wicket_type", "fielders_involved", "Player Out", "year", "Teams", "Venue", "Toss_Winner", "Toss_Decision", "over", "ball_no", "row_id"]
- `data/train.csv` (52623626 bytes); columns: ["Match_ID", "Date", "Season", "Batting team", "Bowling team", "Innings No", "Ball No", "Bowler", "Striker", "Non Striker", "batsman_run", "extras", "type of extras", "total_runs", "score/wicket", "wicket_confirmation", "wicket_type", "fielders_involved", "Player Out", "year", "Teams", "Venue", "Toss_Winner", "Toss_Decision", "over", "ball_no", "row_id", "label"]

## Public description

IPL Next-Ball Outcome Prediction (2008–2024)

Data description
- Provided files:
  - train.csv: Training data with contextual features and next-ball labels.
  - test.csv: Same format as train.csv but without the label column.
  - sample_submission.csv: Expected submission format: probabilities per row_id across 8 classes.

Evaluation
- Metric: Multiclass Log Loss.
- Submission format: CSV with columns [row_id, prob_0, prob_1, prob_2, prob_3, prob_4, prob_5, prob_6, prob_7_plus].
  - Each row_id must match a row in test.csv.
  - Probabilities must be non-negative, finite, and sum to 1 per row.

Train/test split
- Chronological split by season: train up to 2022, test 2023–2024.

Submission
- Create a CSV with the exact columns listed in Evaluation and probabilities for each test row_id.
