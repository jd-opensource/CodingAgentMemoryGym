# OpenMLE-fast task

Task ID: `player-injuries-and-team-performance-dataset@1`

Native metric: `InjuryImpactMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3713 bytes)
- `data/sample_submission.csv` (3748 bytes); columns: ["row_id", "avg_missed_gd"]
- `data/test.csv` (19573 bytes); columns: ["Name", "Team Name", "Position", "Age", "Season", "FIFA rating", "Injury", "Date of Injury", "Match1_before_injury_Result", "Match1_before_injury_Opposition", "Match1_before_injury_GD", "Match1_before_injury_Player_rating", "Match2_before_injury_Result", "Match2_before_injury_Opposition", "Match2_before_injury_GD", "Match2_before_injury_Player_rating", "Match3_before_injury_Result", "Match3_before_injury_Opposition", "Match3_before_injury_GD", "Match3_before_injury_Player_rating", "row_id"]
- `data/train.csv` (91937 bytes); columns: ["Name", "Team Name", "Position", "Age", "Season", "FIFA rating", "Injury", "Date of Injury", "Match1_before_injury_Result", "Match1_before_injury_Opposition", "Match1_before_injury_GD", "Match1_before_injury_Player_rating", "Match2_before_injury_Result", "Match2_before_injury_Opposition", "Match2_before_injury_GD", "Match2_before_injury_Player_rating", "Match3_before_injury_Result", "Match3_before_injury_Opposition", "Match3_before_injury_GD", "Match3_before_injury_Player_rating", "row_id", "avg_missed_gd"]

## Public description

Title: Injury Absence Impact Forecast

Problem statement
Given an injury event and information available up to the injury date, predict how the team will perform during the player’s absence. Specifically, for each injury event, forecast the average goal difference across the first up to three league matches missed by the injured player.

Task
- Input: tabular information about the injured player, club, season, injury type and date, plus team/player form in the three matches immediately prior to the injury.
- Output: a single numeric value per injury event: the average goal difference across the first one to three missed matches (only the missed matches actually recorded are averaged).

Why this matters
Clubs need to anticipate the short-term impact of losing a player in order to plan tactics and squad rotation. Forecasting goal difference during the absence is a practical, quantitative measure of team performance.

Files provided
- train.csv: rows are injury events. Contains features, an opaque identifier column row_id, and the target column avg_missed_gd.
- test.csv: rows are injury events. Contains the same features and row_id as train.csv but without the target column.
- sample_submission.csv: example file with columns [row_id, avg_missed_gd].

Target definition
- avg_missed_gd = mean of the available goal differences among the first three missed matches for that injury event. If only one or two missed matches have a recorded goal difference, the mean is taken over the available ones.

Data description
Each row corresponds to one injury event and includes (columns may contain missing values):
- Player and injury metadata: Name, Team Name, Position, Age, Season, FIFA rating, Injury, Date of Injury.
- Pre-injury form: for up to three matches before the injury, each with Result, Opposition, Goal Difference (GD), and Player rating.

Leakage prevention (already applied in the provided files)
- All columns related to the missed matches (both features and results/opposition) and all columns after the player returns are removed from the features.
- Date of return is excluded from the features.
- An opaque row_id is provided for identification and does not encode any target information.

Official split
- Time-based forecasting split. Training includes earlier seasons; test covers the most recent season.
- The public data files already reflect this split. No validation set is provided; participants should create their own time-aware validation strategy.

Evaluation
- Metric: Mean Absolute Error (MAE).
- Definition: MAE = mean over all test rows of |prediction - ground truth|, where ground truth is avg_missed_gd.
- Rationale: Goal difference is a continuous team performance signal. MAE is robust and interpretable (in goals), and treats over- and under-estimation symmetrically.

Submission format
- CSV with two columns in this exact order: row_id, avg_missed_gd
- row_id must match exactly the identifiers in test.csv (one-to-one). avg_missed_gd must be finite numeric values.

Modeling notes (non-binding guidance)
- Useful features often include: recent team form (pre-injury GD and W/D/L), player role and quality proxies (position, FIFA rating), team identity, injury type, and season effects. Text-like categorical fields (e.g., Opposition names) may require encoding or can be ignored.
- Handle missing values carefully and consider robust encoders for categorical variables.
- Do not rely on any fields that occur after the injury date or describe the missed matches themselves.

Ethics and fairness
- This task evaluates forecasting ability using only information available up to the injury. The design avoids schedule lookup or post-event leakage.

Good luck!
