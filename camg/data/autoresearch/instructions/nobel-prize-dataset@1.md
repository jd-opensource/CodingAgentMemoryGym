# OpenMLE-fast task

Task ID: `nobel-prize-dataset@1`

Native metric: `NobelPrizeCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (830 bytes)
- `data/sample_submission.csv` (4962 bytes); columns: ["Id", "Category"]
- `data/test.csv` (31873 bytes); columns: ["Id", "Work", "Award Year", "Date Awarded", "Prize Amount", "Prize Amount Adjusted"]
- `data/train.csv` (116000 bytes); columns: ["Id", "Work", "Award Year", "Date Awarded", "Prize Amount", "Prize Amount Adjusted", "Category"]

## Public description

Title: Predict Nobel Prize Category from Citation and Metadata

Problem statement
- Task: Predict the Nobel Prize category for each record using the official award citation (text) and structured metadata.
- Target classes: Physics, Chemistry, Physiology or Medicine, Literature, Peace, Economic Sciences.

Data in public/
- train.csv: Training data with columns Id, Work, Award Year, Date Awarded, Prize Amount, Prize Amount Adjusted, Category.
- test.csv: Test data with columns Id, Work, Award Year, Date Awarded, Prize Amount, Prize Amount Adjusted.
- sample_submission.csv: Example submission with columns Id, Category.

Evaluation
- Primary metric: Macro F1 across the target classes present in the test set.
- Submission format: A single CSV with columns Id, Category. Ids must match test.csv exactly and in the same order.
