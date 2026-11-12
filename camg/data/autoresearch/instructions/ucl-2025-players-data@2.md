# OpenMLE-fast task

Task ID: `ucl-2025-players-data@2`

Native metric: `UCLPlayersBR90Metrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2940 bytes)
- `data/sample_submission.csv` (3698 bytes); columns: ["id_player", "target"]
- `data/test.csv` (32340 bytes); columns: ["id_player", "distance_covered_km_per_h", "top_speed", "minutes_played", "matches_appearance", "tackles", "tackles_won", "tackles_lost", "clearance_attempted", "nationality", "field_position", "position", "weight_kg", "height_cm", "age", "id_team", "assists", "corners_taken", "offsides", "dribbles", "total_attempts", "attempts_on_target", "attempts_off_target", "blocked", "passing_accuracy_pct", "passes_attempted", "passes_completed", "crossing_accuracy_pct", "crosses_attempted", "crosses_completed", "free_kick_taken", "matches_appearance_distribution", "saves", "goals_conceded", "saves_on_penalty", "clean_sheets", "punches_made", "unnamed:_0", "fouls_committed", "fouls_suffered", "yellow_cards", "red_cards", "country", "team_name"]
- `data/train.csv` (132242 bytes); columns: ["id_player", "distance_covered_km_per_h", "top_speed", "minutes_played", "matches_appearance", "tackles", "tackles_won", "tackles_lost", "clearance_attempted", "nationality", "field_position", "position", "weight_kg", "height_cm", "age", "id_team", "assists", "corners_taken", "offsides", "dribbles", "total_attempts", "attempts_on_target", "attempts_off_target", "blocked", "passing_accuracy_pct", "passes_attempted", "passes_completed", "crossing_accuracy_pct", "crosses_attempted", "crosses_completed", "free_kick_taken", "matches_appearance_distribution", "saves", "goals_conceded", "saves_on_penalty", "clean_sheets", "punches_made", "unnamed:_0", "fouls_committed", "fouls_suffered", "yellow_cards", "red_cards", "country", "team_name", "target"]

## Public description

Title: UCL 2025 — Predict Balls Recovered per 90

Background
Balls recovered is a core defensive contribution reflecting pressing, positioning, anticipation, and work rate. Using player-level information from the 2025 UEFA Champions League (UCL) season spanning technical, physical, attacking, disciplinary, distribution, goalkeeping and profile data, your task is to predict each player’s balls recovered per 90 minutes.

Problem Statement
Given each player’s non-recovery statistics and profile, predict their balls recovered per 90 (BR/90) over the observed UCL 2025 period. You will build a model that generalizes across positions and clubs.

Data Description
You are provided with processed competition files built from the underlying player tables:
- train.csv: Player features with one target column.
- test.csv: Player features without the target column.
- sample_submission.csv: A sample submission with the correct format.

Feature space (examples, not exhaustive):
- Player profile: age, height, weight, nationality, field_position, position, team information.
- Physical/key stats: minutes_played, matches_appearance, top_speed, distance_covered.
- Attacking: assists, corners_taken, offsides, dribbles.
- Attempts: total_attempts, attempts_on_target, attempts_off_target, blocked.
- Distribution: passing_accuracy, passes_attempted/completed, crossing_accuracy, crosses_attempted/completed, free_kick_taken.
- Defensive (non-label aspects): tackles, tackles_won, tackles_lost, clearance_attempted.
- Goalkeeping: saves, goals_conceded, saves_on_penalty, clean_sheets, punches_made.

Target
- train.csv includes a single target column named target, defined as: balls_recovered_per90 = balls_recovered / (minutes_played / 90).
- Neither balls_recovered nor balls_recovered_per90 appear in test.csv to avoid label leakage.

Files to use
- Training file: train.csv
- Test file: test.csv
- Submission file format: CSV with columns [id_player, target]. The target column must contain your model’s predicted BR/90 for each player in test.csv, in the same row order.

Evaluation Metric
Primary metric: Weighted RMSE on BR/90.
- For each player i, let y_i be the true BR/90 and ŷ_i be your prediction. Let w_i = minutes_played_i.
- Weighted MSE = sum_i w_i * (ŷ_i - y_i)^2 / sum_i w_i.
- Weighted RMSE = sqrt(Weighted MSE).
Rationale: BR/90 already normalizes for playing time, but longer minutes provide more reliable signals. Weighting by minutes_played yields a fair and precise measure while keeping the task challenging.

Notes and Rules
- Use machine learning to process data, engineer features, train models, and evaluate results.
- Predictions must be finite real numbers. Negative predictions are clipped to 0 during scoring.
- Do not rely on any external data beyond what’s provided.
- Keep the order of rows in the submission aligned to test.csv.

Good luck, and enjoy modeling defensive impact in elite football.
