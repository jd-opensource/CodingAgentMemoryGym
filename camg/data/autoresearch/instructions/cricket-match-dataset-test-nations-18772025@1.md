# OpenMLE-fast task

Task ID: `cricket-match-dataset-test-nations-18772025@1`

Native metric: `CricketWinProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3422 bytes)
- `data/sample_submission.csv` (23700 bytes); columns: ["row_id", "p_team1_win"]
- `data/test.csv` (52537 bytes); columns: ["row_id", "Team 1", "Team 2", "Ground", "Match Date", "Format"]
- `data/train.csv` (219062 bytes); columns: ["row_id", "Team 1", "Team 2", "Ground", "Match Date", "Format", "target"]

## Public description

Competition: Limited-Overs International Winner Prediction (ODI + T20I)

Problem statement
Given two national teams, the venue, the match format (ODI or T20I), and the match date, predict the probability that Team 1 wins the match. Each row in the test set corresponds to a specific ODI or T20I. Your task is to submit a calibrated probability P(Team 1 wins) for every test row.

Why this is challenging and meaningful
- Limited-overs internationals are high-variance and evolve over time (law changes, team cycles, and home/away effects).
- Only coarse covariates are provided (teams, venue, format, date), so competitive solutions must engineer features (e.g., rolling strengths, rating systems, venue effects) and respect time ordering to avoid leakage.
- Strong solutions will combine temporal modeling, careful encoding of categorical variables, and probability calibration.

Data description
The competition dataset consists of international ODI and T20I matches played by Test-playing nations (plus rare ICC World XI fixtures). The following columns are provided:
- Team 1: Team listed in the first column of the source record
- Team 2: Opponent team
- Ground: Venue name
- Match Date: Match date (for multi-day strings, the last day is used internally)
- Format: Either ODI or T20I

Target
- Binary target indicating whether Team 1 won the match.

Files you will use
- train.csv: Training data with the target column.
- test.csv: Test data without the target column. Use these rows to generate predictions.
- sample_submission.csv: Sample submission with the correct format and random but valid probability values.

Important notes about labels and filtering
- Only ODI and T20I matches are included.
- Matches labeled as tied or no result are excluded from the dataset to avoid outcomes driven by exogenous factors and to keep the target well-defined.
- The Scorecard and Margin fields from the original data are not included in the competition features to prevent leakage.

Evaluation
- Submit a CSV with two columns: row_id and p_team1_win, where p_team1_win is your predicted probability that Team 1 wins.
- Scoring metric: format-stratified binary log loss. Log loss is computed separately on the ODI subset and the T20I subset of the test set, and the final score is the simple average of these two values. This prevents one format from dominating and rewards well-calibrated probabilities.

Train/test split
- Chronological split is used to reflect real-world forecasting and prevent leakage. Training covers matches before the split date; testing covers matches on or after the split date. The split is chosen to ensure that both ODI and T20I matches are present in the test set.

Submission format
- CSV with two columns, no header changes or extra columns:
  - row_id: Integer identifier matching the test set rows
  - p_team1_win: Floating-point probability in [0, 1]

Starter guidance (non-binding)
- Encode categorical variables (teams, grounds, formats) carefully, and consider time-aware encodings (e.g., rolling win rates or Elo-like ratings per format and by venue region).
- Be mindful of temporal non-stationarity and use leakage-free cross-validation within the training set.
- Calibrate probabilities (e.g., isotonic or Platt scaling) if needed.

Final data files
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building robust, well-calibrated match outcome predictors!
