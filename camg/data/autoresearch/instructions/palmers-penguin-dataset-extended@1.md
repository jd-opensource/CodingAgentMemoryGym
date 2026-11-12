# OpenMLE-fast task

Task ID: `palmers-penguin-dataset-extended@1`

Native metric: `PenguinSpeciesClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (450 bytes)
- `data/sample_submission.csv` (37850 bytes); columns: ["id", "species"]
- `data/test.csv` (94959 bytes); columns: ["id", "island", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex", "year"]
- `data/train.csv` (128090 bytes); columns: ["id", "island", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex", "year", "species"]

## Public description

Competition: Robust Penguin Species Classification under Temporal & Ecological Shift

Files:
- train.csv
- test.csv
- sample_submission.csv

Task: Predict the species for rows in test.csv.

Target: species
Features: id, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, year

Submission format: CSV with columns [id, species]. Valid species: Adelie, Chinstrap, Gentoo.

Evaluation: Macro-averaged F1 over the three classes.
