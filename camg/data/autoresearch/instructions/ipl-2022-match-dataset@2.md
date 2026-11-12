# OpenMLE-fast task

Task ID: `ipl-2022-match-dataset@2`

Native metric: `IPLRunOutcomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3546 bytes)
- `data/sample_submission.csv` (592329 bytes); columns: ["row_id", "p_0", "p_1", "p_2", "p_3", "p_4", "p_5", "p_6", "p_7"]
- `data/test.csv` (1905294 bytes); columns: ["row_id", "ID", "innings", "overs", "ballnumber", "batter", "bowler", "non-striker", "BattingTeam", "City", "Date", "Season", "MatchNumber", "Team1", "Team2", "Venue", "TossWinner", "TossDecision", "Team1Players", "Team2Players", "Umpire1", "Umpire2"]
- `data/train.csv` (7653860 bytes); columns: ["row_id", "ID", "innings", "overs", "ballnumber", "batter", "bowler", "non-striker", "BattingTeam", "City", "Date", "Season", "MatchNumber", "Team1", "Team2", "Venue", "TossWinner", "TossDecision", "Team1Players", "Team2Players", "Umpire1", "Umpire2", "total_run"]

## Public description

Title: IPL 2022 Ball-Level Run Outcome Probabilities

Background
T20 cricket delivers rapid, high-variance outcomes at every ball, ranging from dot balls to boundaries and rare multi-run plays. Modeling the full probability distribution of run outcomes for each delivery enables strategic decision-making, broadcast insights, and performance analytics.

Problem Statement
Using only pre-delivery context for each ball (match and in-play context available before the ball is bowled), predict the probability distribution over discrete run outcomes: 0, 1, 2, 3, 4, 5, 6, 7 runs.
Participants must build models that take the provided structured context and output well-calibrated probabilities for all eight classes for every ball in the test set.

Data Description
The competition provides ball-by-ball context joined with match-level pre-match information. Outcome-related columns (e.g., extras_type, batsman_run, extras_run, non_boundary, isWicketDelivery, player_out, dismissal kind, fielders involved, match result fields) are excluded from features to prevent leakage. The target label for training is the total runs scored off the ball (an integer in {0,1,2,3,4,5,6,7}).

Files
- train.csv: Feature columns plus the target column total_run.
- test_data.csv: Feature columns only; no target.
- sample_submission.csv: Example submission with row_id and eight probability columns (p_0, p_1, p_2, p_3, p_4, p_5, p_6, p_7). Probabilities per row must be non-negative and sum to 1.

Key Columns (features include but are not limited to)
- row_id: Unique identifier for each ball (provided for indexing and submission).
- ID: Match identifier.
- innings: Innings number (1 or 2; super over balls, if any, are treated consistently).
- overs: Over number (0-based integer within an innings).
- ballnumber: Ball number within the over (1–6; super over also present if applicable).
- batter, bowler, non-striker: Player names (categorical).
- BattingTeam: Team name for the batting side.
- City, Date, Season, MatchNumber, Team1, Team2, Venue, TossWinner, TossDecision: Pre-match context.
- Team1Players, Team2Players, Umpire1, Umpire2: Additional categorical context from match information.

Evaluation
For every row_id in test_data.csv, submissions must provide a valid probability distribution across classes {0,1,2,3,4,5,6,7} using columns p_0, p_1, ..., p_7.
- Metric: Multiclass log loss (cross-entropy) averaged over the test rows.
- Numerical stability: Probabilities are clipped to a small lower bound and renormalized row-wise if they do not sum to 1.
- Format enforcement: The set of row_id values must exactly match test_data.csv.

Guidance and Expectations
- This is a probabilistic classification task with class imbalance (dot balls and singles are frequent; 5 and 7 are rare). Proper handling (e.g., calibrated models, class weighting, probabilistic modeling) is important.
- Suggested modeling pipeline:
  - Data processing: encode categorical features (players, teams, venue, toss), parse date/season, and derive contextual features (e.g., over, innings, match-up effects).
  - Feature engineering: player form proxies, team strengths, venue effects, toss decision impact, over-phase buckets, recency within innings.
  - Model training: gradient boosting, regularized linear models, neural nets for tabular data, or probabilistic classifiers.
  - Model evaluation: cross-entropy calibration, validation via CV on training, attention to rare outcomes.
- The task is challenging yet solvable using modern ML methods over tabular data.
