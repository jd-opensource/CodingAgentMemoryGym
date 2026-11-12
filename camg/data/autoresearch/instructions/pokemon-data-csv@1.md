# OpenMLE-fast task

Task ID: `pokemon-data-csv@1`

Native metric: `PokemonStatsRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1049 bytes)
- `data/sample_submission.csv` (29852 bytes); columns: ["row_id", "hp", "attack", "defense", "special_attack", "special_defense", "speed"]
- `data/test.csv` (28637 bytes); columns: ["row_id", "base_experience", "height", "weight", "types", "abilities", "moves"]
- `data/train.csv` (134935 bytes); columns: ["row_id", "base_experience", "height", "weight", "types", "abilities", "moves", "hp", "attack", "defense", "special_attack", "special_defense", "speed"]

## Public description

Title: Predict Pokémon Base Stats from Non-Stat Attributes

Problem statement
Build a multi-target regression model that predicts a Pokémon’s six base battle stats from its non-stat attributes.

Files provided
- train.csv: Training data with features and target columns.
- test.csv: Test data with the same feature columns as train.csv but without the target columns.
- sample_submission.csv: Example submission format with randomly generated but valid predictions.

Columns
Input features in both train.csv and test.csv:
- row_id
- base_experience
- height
- weight
- types
- abilities
- moves

Target columns (train.csv only; must be predicted for test.csv):
- hp
- attack
- defense
- special_attack
- special_defense
- speed

Evaluation
Submissions are evaluated using a normalized multi-target RMSE. Lower is better.

Submission format
Your submission must be a CSV with columns: row_id, hp, attack, defense, special_attack, special_defense, speed.
The row_id values must exactly match those in test.csv, without duplicates or missing rows.
