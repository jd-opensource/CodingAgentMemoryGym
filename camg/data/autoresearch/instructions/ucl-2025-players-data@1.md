# OpenMLE-fast task

Task ID: `ucl-2025-players-data@1`

Native metric: `UCLDribblesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (292 bytes)
- `data/sample_submission.csv` (3652 bytes); columns: ["id", "dribbles_per_90"]
- `data/test.csv` (29708 bytes); columns: ["id", "nationality", "field_position", "position", "weight_kg", "height_cm", "age", "id_team", "distance_covered_km_h", "top_speed", "minutes_played", "matches_appearance", "passing_accuracy_pct", "passes_attempted", "passes_completed", "crossing_accuracy_pct", "crosses_attempted", "crosses_completed", "free_kick_taken", "total_attempts", "attempts_on_target", "attempts_off_target", "blocked", "assists", "corners_taken", "offsides", "balls_recovered", "tackles", "tackles_won", "tackles_lost", "clearance_attempted", "goals", "inside_area", "outside_area", "right_foot", "left_foot", "head", "other", "penalties_scored", "fouls_committed", "fouls_suffered", "team_country", "team_name"]
- `data/train.csv` (121657 bytes); columns: ["id", "nationality", "field_position", "position", "weight_kg", "height_cm", "age", "id_team", "distance_covered_km_h", "top_speed", "minutes_played", "matches_appearance", "passing_accuracy_pct", "passes_attempted", "passes_completed", "crossing_accuracy_pct", "crosses_attempted", "crosses_completed", "free_kick_taken", "total_attempts", "attempts_on_target", "attempts_off_target", "blocked", "assists", "corners_taken", "offsides", "balls_recovered", "tackles", "tackles_won", "tackles_lost", "clearance_attempted", "goals", "inside_area", "outside_area", "right_foot", "left_foot", "head", "other", "penalties_scored", "fouls_committed", "fouls_suffered", "team_country", "team_name", "dribbles_per_90"]

## Public description

UEFA Champions League 2025 – Predict Outfield Dribbles per 90

Files provided:

- train.csv: Training data with features and target dribbles_per_90.

- test.csv: Test data with features only (no target).

- sample_submission.csv: Example submission file with columns [id, dribbles_per_90].
