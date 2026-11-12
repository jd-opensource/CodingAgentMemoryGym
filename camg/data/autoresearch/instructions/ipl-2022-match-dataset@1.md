# OpenMLE-fast task

Task ID: `ipl-2022-match-dataset@1`

Native metric: `IPLWicketPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3655 bytes)
- `data/sample_submission.csv` (124173 bytes); columns: ["row_id", "is_wicket"]
- `data/test.csv` (850428 bytes); columns: ["row_id", "innings", "overs", "ballnumber", "batter", "bowler", "non_striker", "BattingTeam", "City", "Date", "Season", "MatchNumber", "Team1", "Team2", "Venue", "TossWinner", "TossDecision", "Umpire1", "Umpire2"]
- `data/train.csv` (3168707 bytes); columns: ["row_id", "innings", "overs", "ballnumber", "batter", "bowler", "non_striker", "BattingTeam", "City", "Date", "Season", "MatchNumber", "Team1", "Team2", "Venue", "TossWinner", "TossDecision", "Umpire1", "Umpire2", "is_wicket"]

## Public description

Competition: IPL 2022 Ball-Level Wicket Probability

Background
Tata IPL 2022 logs capture every delivery with rich pre-delivery context (who bowls, who bats, inning/over/ball index, teams, venue, toss info, etc.). Wickets are pivotal events that swing momentum and strategy. Anticipating wicket risk before the ball is bowled is a high-impact analytics task for sports data science.

Problem Statement
Given only pre-delivery context, predict the probability that a delivery results in a wicket. Your model must output a calibrated probability in [0, 1] for each ball in the test set.

Files Provided
- train.csv: Training rows with features and target.
- test.csv: Test rows with the same features (without the target).
- sample_submission.csv: A sample of the expected submission format.

Columns
Each row represents a single ball (delivery). Rows are uniquely identified by row_id.
- row_id: Unique identifier of a ball-level event composed from match and delivery indices.
- Features (pre-delivery context only):
  - innings: Inning number (1 or 2).
  - overs: Over index within the inning (integer, usually 0–19).
  - ballnumber: Ball index within the over (1–6).
  - batter: Batter on strike.
  - bowler: Bowler delivering the ball.
  - non_striker: Non-striker batter.
  - BattingTeam: Team batting for this delivery.
  - City: City of the venue.
  - Date: Match date (YYYY-MM-DD).
  - Season: Season year (2022).
  - MatchNumber: Tournament stage or match number.
  - Team1, Team2: Teams participating in the match.
  - Venue: Full venue description.
  - TossWinner: Team that won the toss.
  - TossDecision: Toss decision (bat/field).
  - Umpire1, Umpire2: Umpires officiating the match.
- Target (train.csv only):
  - is_wicket: Binary indicator (1 if the delivery results in a wicket, else 0).

Submission Format
Submit a CSV file with the following columns:
- row_id
- is_wicket: Predicted probability of a wicket for the corresponding row_id (float in [0, 1]).

Evaluation
Submissions are evaluated using Average Precision (area under the precision–recall curve) on the positive class (is_wicket = 1). This metric is well-suited to the natural class imbalance in wicket events, rewards correct ranking of high-risk deliveries, and is robust to probability calibration. Ties are handled consistently via a stable sort; probabilities outside [0, 1] will be clipped.

Data Integrity and Split
- The split is grouped by match and time-aware: complete matches belong entirely to train or test, ordered chronologically.
- Only pre-delivery features are included; any post-delivery outcomes (e.g., runs scored, extras, dismissal kind) are excluded to prevent leakage.
- Category coverage: all categorical values present in test also occur in train at least once to ensure solvability; if a rare category appears only in test, it is consolidated under a deterministic placeholder token.
- The target column appears only in train.csv.

Notes and Tips
- Strong baselines include gradient boosting, regularized linear models, and modern tabular DL. Handle high-cardinality categorical features (batter/bowler/venue/teams/umpires) using frequency or hashing encodings; target encoding with proper CV may help, but avoid leakage.
- Consider engineered order-aware features (e.g., over and ball as cyclic encodings) and interactions (bowler–batter matchup, venue effects).
- Ensure robust preprocessing: handle string categories, deduplicate by delivery key, and verify no missing values in critical identifiers. Calibrate probabilities when appropriate.

Deliverable
A single CSV with row_id and is_wicket probabilities for every row in test.csv.
