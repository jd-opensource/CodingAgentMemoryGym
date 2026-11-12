# OpenMLE-fast task

Task ID: `palmer-penguins-csv@1`

Native metric: `PalmerPenguinsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (631 bytes)
- `data/sample_submission.csv` (5772 bytes); columns: ["Id", "Species"]
- `data/test.csv` (10230 bytes); columns: ["Id", "Culmen Length (mm)", "Culmen Depth (mm)", "Flipper Length (mm)", "Body Mass (g)", "Sex", "Delta 15 N (o/oo)", "Delta 13 C (o/oo)", "Island", "Clutch Completion", "studyName", "Date Egg"]
- `data/train.csv` (24590 bytes); columns: ["Culmen Length (mm)", "Culmen Depth (mm)", "Flipper Length (mm)", "Body Mass (g)", "Sex", "Delta 15 N (o/oo)", "Delta 13 C (o/oo)", "Island", "Clutch Completion", "studyName", "Date Egg", "Species"]

## Public description

Title: Palmer Penguins Species Classification

Data in this directory:
- train.csv: features plus the Species column.
- test.csv: features only, plus an Id column to align submissions.
- sample_submission.csv: example submission containing Id and Species.

Features included (columns): Culmen Length (mm), Culmen Depth (mm), Flipper Length (mm), Body Mass (g), Sex, Delta 15 N (o/oo), Delta 13 C (o/oo), Island, Clutch Completion, studyName, Date Egg.
Target: Species (three classes).

Evaluation: Macro F1 across Species classes.

Submission format: CSV with two columns: Id and Species; Ids must match those in test.csv exactly.
