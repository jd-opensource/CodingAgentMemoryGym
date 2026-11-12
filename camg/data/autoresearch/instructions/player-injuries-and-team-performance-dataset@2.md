# OpenMLE-fast task

Task ID: `player-injuries-and-team-performance-dataset@2`

Native metric: `PlayerInjuryDeltaMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3289 bytes)
- `data/sample_submission.csv` (1288 bytes); columns: ["injury_id", "target_delta"]
- `data/test.csv` (12692 bytes); columns: ["injury_id", "Name", "Team Name", "Position", "Age", "Season", "FIFA rating", "Injury", "Date of Injury", "Match1_before_injury_Result", "Match1_before_injury_Opposition", "Match1_before_injury_GD", "Match1_before_injury_Player_rating", "Match2_before_injury_Result", "Match2_before_injury_Opposition", "Match2_before_injury_GD", "Match2_before_injury_Player_rating", "Match3_before_injury_Result", "Match3_before_injury_Opposition", "Match3_before_injury_GD", "Match3_before_injury_Player_rating"]
- `data/train.csv` (73672 bytes); columns: ["injury_id", "Name", "Team Name", "Position", "Age", "Season", "FIFA rating", "Injury", "Date of Injury", "Match1_before_injury_Result", "Match1_before_injury_Opposition", "Match1_before_injury_GD", "Match1_before_injury_Player_rating", "Match2_before_injury_Result", "Match2_before_injury_Opposition", "Match2_before_injury_GD", "Match2_before_injury_Player_rating", "Match3_before_injury_Result", "Match3_before_injury_Opposition", "Match3_before_injury_GD", "Match3_before_injury_Player_rating", "target_delta"]

## Public description

Post-Injury Player Performance Delta (Regression Challenge)

Overview
Forecast the short‑term change in a player’s performance rating immediately after returning from injury. For each injury event, use only information available up to the injury date to predict the rating delta between the first matches after return and the pre‑injury form.

Task
Given an injury event with metadata and the three matches prior to the injury, predict:
  target_delta = mean(player rating over first up to three post‑return matches) − mean(player rating over the three matches before injury)
The target is organizer‑computed for the training set and hidden for the test set.

Files
- train.csv: Training data with features and target_delta.
- test.csv: Test data with the same features, without target_delta.
- sample_submission.csv: Template with injury_id and a placeholder target_delta to demonstrate the required format.

Target and features
- Label (only in train.csv): target_delta, a continuous value in rating points.
- Identifier: injury_id, a unique row identifier to join outputs.
- Features (all rows):
  - Player/injury metadata: Name, Team Name, Position, Age, Season, FIFA rating, Injury, Date of Injury.
  - Pre‑injury context (up to three matches): for each of Match1/2/3_before_injury_*, the fields Result, Opposition, GD, Player_rating.
- Excluded from features to avoid leakage: any after‑injury fields, any missed‑match fields, and Date of return.

Data notes
- Ratings may include strings like “6(S)” indicating substitute appearances; numeric parsing is needed.
- Results are categorical (W/D/L); GD is numeric goal difference; Opposition is a team name string (can be encoded).
- Some rows have partial availability (fewer than three ratings before/after); the target uses the mean over available matches.

Split policy
- Time‑aware split by season for robust generalization: train covers seasons prior to 2023/24; test covers 2023/24.
- Every test row has at least one pre‑injury and one post‑return rating in the source, enabling a well‑defined target.

Evaluation
- Metric: Mean Absolute Error (MAE) between predicted target_delta and ground truth.
- Submission format: CSV with columns [injury_id, target_delta] exactly, in the same row order as test.csv.
- Predictions must be numeric and finite. Values outside [-20, 20] are rejected.

Modeling guidance
- Suggested preprocessing:
  - Parse ratings (strip “(S)”), cast to float; compute rolling means over pre‑injury ratings and form.
  - Encode categorical variables (team, position, injury type, season) via target‑safe encodings (e.g., one‑hot, frequency).
  - Derive features such as: average pre‑injury rating, rating trend across last three matches, average GD and result points, opposition strength proxies (e.g., frequency encoding), days‑since‑season start from Date of Injury.
- Baseline models: Regularized linear models, tree‑based ensembles (gradient boosting, random forest), or neural nets.
- Consider robust validation (e.g., group by player name or time‑based folds) to manage leakage and distribution shift.

Submission
- Create a file with columns [injury_id, target_delta].
- Ensure the order of injury_id matches test.csv exactly.
- Lower MAE is better.
