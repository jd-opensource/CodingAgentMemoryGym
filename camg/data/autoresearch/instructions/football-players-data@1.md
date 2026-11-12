# OpenMLE-fast task

Task ID: `football-players-data@1`

Native metric: `FIFAValuationWageMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5977 bytes)
- `data/sample_submission.csv` (146650 bytes); columns: ["id", "value_euro", "wage_euro"]
- `data/test.csv` (545610 bytes); columns: ["id", "age", "height_cm", "weight_kgs", "positions", "nationality", "overall_rating", "potential", "preferred_foot", "international_reputation(1-5)", "weak_foot(1-5)", "skill_moves(1-5)", "body_type", "release_clause_euro", "crossing", "finishing", "heading_accuracy", "short_passing", "volleys", "dribbling", "curve", "freekick_accuracy", "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", "reactions", "balance", "shot_power", "jumping", "stamina", "strength", "long_shots", "aggression", "interceptions", "positioning", "vision", "penalties", "composure", "marking", "standing_tackle", "sliding_tackle"]
- `data/train.csv` (2350885 bytes); columns: ["age", "height_cm", "weight_kgs", "positions", "nationality", "overall_rating", "potential", "value_euro", "wage_euro", "preferred_foot", "international_reputation(1-5)", "weak_foot(1-5)", "skill_moves(1-5)", "body_type", "release_clause_euro", "crossing", "finishing", "heading_accuracy", "short_passing", "volleys", "dribbling", "curve", "freekick_accuracy", "long_passing", "ball_control", "acceleration", "sprint_speed", "agility", "reactions", "balance", "shot_power", "jumping", "stamina", "strength", "long_shots", "aggression", "interceptions", "positioning", "vision", "penalties", "composure", "marking", "standing_tackle", "sliding_tackle"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (3541 lines)
test.csv (3541 lines)
train.csv (14160 lines)```

-> sample_submission.csv has 3540 rows and 3 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 3539.00, 0 nan values
value_euro (float64) has range: 8549.57 - 211255115.01, 0 nan values
wage_euro (float64) has range: 77.14 - 307459.75, 0 nan values

-> test.csv has 3540 rows and 43 columns.
Here is some information about the columns:
acceleration (int64) has range: 15.00 - 96.00, 0 nan values
age (int64) has range: 17.00 - 40.00, 0 nan values
aggression (int64) has range: 11.00 - 94.00, 0 nan values
agility (int64) has range: 15.00 - 95.00, 0 nan values
balance (int64) has range: 18.00 - 94.00, 0 nan values
ball_control (int64) has range: 5.00 - 94.00, 0 nan values
body_type (object) has 4 unique values: ['Normal', 'Lean', 'Stocky', 'Courtois']
composure (int64) has range: 12.00 - 91.00, 0 nan values
crossing (int64) has range: 5.00 - 91.00, 0 nan values
curve (int64) has range: 6.00 - 90.00, 0 nan values
dribbling (int64) has range: 5.00 - 95.00, 0 nan values
finishing (int64) has range: 5.00 - 94.00, 0 nan values
freekick_accuracy (int64) has range: 4.00 - 92.00, 0 nan values
heading_accuracy (int64) has range: 5.00 - 94.00, 0 nan values
height_cm (float64) has range: 152.40 - 203.20, 0 nan values
id (int64) has range: 0.00 - 3539.00, 0 nan values
interceptions (int64) has range: 3.00 - 89.00, 0 nan values
international_reputation(1-5) (int64) has 4 unique values: [2, 1, 3, 4]
jumping (int64) has range: 26.00 - 93.00, 0 nan values
long_passing (int64) has range: 10.00 - 89.00, 0 nan values
long_shots (int64) has range: 4.00 - 89.00, 0 nan values
marking (int64) has range: 5.00 - 92.00, 0 nan values
nationality (object) has 121 unique values. Some example values: ['England', 'Germany', 'Spain', 'Argentina']
overall_rating (int64) has range: 47.00 - 91.00, 0 nan values
penalties (int64) has range: 8.00 - 90.00, 0 nan values
positioning (int64) has range: 3.00 - 93.00, 0 nan values
positions (object) has 389 unique values. Some example values: ['CB', 'GK', 'ST', 'CM']
potential (int64) has range: 50.00 - 95.00, 0 nan values
preferred_foot (object) has 2 unique values: ['Right', 'Left']
reactions (int64) has range: 30.00 - 91.00, 0 nan values
release_clause_euro (float64) has range: 18000.00 - 185800000.00, 329 nan values
short_passing (int64) has range: 7.00 - 93.00, 0 nan values
shot_power (int64) has range: 10.00 - 89.00, 0 nan values
skill_moves(1-5) (int64) has 5 unique values: [3, 2, 4, 1, 5]
sliding_tackle (int64) has range: 6.00 - 90.00, 0 nan values
sprint_speed (int64) has range: 15.00 - 96.00, 0 nan values
stamina (int64) has range: 12.00 - 96.00, 0 nan values
standing_tackle (int64) has range: 6.00 - 90.00, 0 nan values
strength (int64) has range: 25.00 - 94.00, 0 nan values
vision (int64) has range: 10.00 - 92.00, 0 nan values
volleys (int64) has range: 4.00 - 90.00, 0 nan values
weak_foot(1-5) (int64) has 5 unique values: [4, 3, 2, 1, 5]
weight_kgs (float64) has range: 53.10 - 107.00, 0 nan values

-> train.csv has 14159 rows and 44 columns.
Here is some information about the columns:
acceleration (int64) has range: 12.00 - 97.00, 0 nan values
age (int64) has range: 17.00 - 46.00, 0 nan values
aggression (int64) has range: 11.00 - 95.00, 0 nan values
agility (int64) has range: 11.00 - 96.00, 0 nan values
balance (int64) has range: 16.00 - 96.00, 0 nan values
ball_control (int64) has range: 8.00 - 96.00, 0 nan values
body_type (object) has 9 unique values: ['Normal', 'Lean', 'Stocky', 'Neymar', 'Shaqiri', 'Messi', 'Akinfenwa', 'PLAYER_BODY_TYPE_25', 'C. Ronaldo']
composure (int64) has range: 12.00 - 96.00, 0 nan values
crossing (int64) has range: 6.00 - 93.00, 0 nan values
curve (int64) has range: 6.00 - 94.00, 0 nan values
dribbling (int64) has range: 4.00 - 97.00, 0 nan values
finishing (int64) has range: 2.00 - 95.00, 0 nan values
freekick_accuracy (int64) has range: 3.00 - 94.00, 0 nan values
heading_accuracy (int64) has range: 4.00 - 93.00, 0 nan values
height_cm (float64) has range: 152.40 - 205.74, 0 nan values
interceptions (int64) has range: 5.00 - 92.00, 0 nan values
international_reputation(1-5) (int64) has 5 unique values: [1, 2, 3, 4, 5]
jumping (int64) has range: 15.00 - 95.00, 0 nan values
long_passing (int64) has range: 9.00 - 93.00, 0 nan values
long_shots (int64) has range: 3.00 - 94.00, 0 nan values
marking (int64) has range: 3.00 - 94.00, 0 nan values
nationality (object) has 154 unique values. Some example values: ['England', 'Germany', 'Spain', 'France']
overall_rating (int64) has range: 47.00 - 94.00, 0 nan values
penalties (int64) has range: 5.00 - 92.00, 0 nan values
positioning (int64) has range: 2.00 - 95.00, 0 nan values
positions (object) has 783 unique values. Some example values: ['CB', 'GK', 'ST', 'CM']
potential (int64) has range: 51.00 - 94.00, 0 nan values
preferred_foot (object) has 2 unique values: ['Right', 'Left']
reactions (int64) has range: 24.00 - 96.00, 0 nan values
release_clause_euro (float64) has range: 13000.00 - 226500000.00, 1253 nan values
short_passing (int64) has range: 7.00 - 93.00, 0 nan values
shot_power (int64) has range: 2.00 - 95.00, 0 nan values
skill_moves(1-5) (int64) has 5 unique values: [1, 2, 3, 4, 5]
sliding_tackle (int64) has range: 3.00 - 90.00, 0 nan values
sprint_speed (int64) has range: 12.00 - 96.00, 0 nan values
stamina (int64) has range: 12.00 - 97.00, 0 nan values
standing_tackle (int64) has range: 2.00 - 93.00, 0 nan values
strength (int64) has range: 20.00 - 97.00, 0 nan values
value_euro (float64) has range: 10000.00 - 110500000.00, 0 nan values
vision (int64) has range: 10.00 - 94.00, 0 nan values
volleys (int64) has range: 3.00 - 90.00, 0 nan values
wage_euro (float64) has range: 1000.00 - 565000.00, 0 nan values
weak_foot(1-5) (int64) has 5 unique values: [2, 3, 4, 5, 1]
weight_kgs (float64) has range: 49.90 - 110.20, 0 nan values
