# OpenMLE-fast task

Task ID: `ucl-202122-uefa-champions-league@1`

Native metric: `UCLGoalsAssistsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1063 bytes)
- `data/sample_submission.csv` (1678 bytes); columns: ["id", "goals", "assists"]
- `data/test.csv` (27880 bytes); columns: ["position", "attempts_total_attempts", "attempts_on_target", "attempts_off_target", "attempts_blocked", "attempts_match_played", "attacking_corner_taken", "attacking_offsides", "attacking_dribbles", "attacking_match_played", "distribution_pass_accuracy", "distribution_pass_attempted", "distribution_pass_completed", "distribution_cross_accuracy", "distribution_cross_attempted", "distribution_cross_complted", "distribution_freekicks_taken", "distribution_match_played", "defending_balls_recoverd", "defending_tackles", "defending_t_won", "defending_t_lost", "defending_clearance_attempted", "defending_match_played", "disciplinary_fouls_committed", "disciplinary_fouls_suffered", "disciplinary_red", "disciplinary_yellow", "disciplinary_minutes_played", "disciplinary_match_played", "key_minutes_played", "key_match_played", "key_distance_covered", "gk_saved", "gk_conceded", "gk_saved_penalties", "gk_cleansheets", "gk_punches_made", "gk_match_played", "id"]
- `data/train.csv` (110449 bytes); columns: ["position", "attempts_total_attempts", "attempts_on_target", "attempts_off_target", "attempts_blocked", "attempts_match_played", "attacking_corner_taken", "attacking_offsides", "attacking_dribbles", "attacking_match_played", "distribution_pass_accuracy", "distribution_pass_attempted", "distribution_pass_completed", "distribution_cross_accuracy", "distribution_cross_attempted", "distribution_cross_complted", "distribution_freekicks_taken", "distribution_match_played", "defending_balls_recoverd", "defending_tackles", "defending_t_won", "defending_t_lost", "defending_clearance_attempted", "defending_match_played", "disciplinary_fouls_committed", "disciplinary_fouls_suffered", "disciplinary_red", "disciplinary_yellow", "disciplinary_minutes_played", "disciplinary_match_played", "key_minutes_played", "key_match_played", "key_distance_covered", "gk_saved", "gk_conceded", "gk_saved_penalties", "gk_cleansheets", "gk_punches_made", "gk_match_played", "id", "goals", "assists"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (152 lines)
test.csv (152 lines)
train.csv (601 lines)```

-> sample_submission.csv has 151 rows and 3 columns.
The columns are: id, goals, assists

-> test.csv has 151 rows and 40 columns.
The columns are: position, attempts_total_attempts, attempts_on_target, attempts_off_target, attempts_blocked, attempts_match_played, attacking_corner_taken, attacking_offsides, attacking_dribbles, attacking_match_played, distribution_pass_accuracy, distribution_pass_attempted, distribution_pass_completed, distribution_cross_accuracy, distribution_cross_attempted... and 25 more columns

-> train.csv has 600 rows and 42 columns.
The columns are: position, attempts_total_attempts, attempts_on_target, attempts_off_target, attempts_blocked, attempts_match_played, attacking_corner_taken, attacking_offsides, attacking_dribbles, attacking_match_played, distribution_pass_accuracy, distribution_pass_attempted, distribution_pass_completed, distribution_cross_accuracy, distribution_cross_attempted... and 27 more columns
