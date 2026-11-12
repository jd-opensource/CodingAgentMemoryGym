# OpenMLE-fast task

Task ID: `a-collection-of-technical-manuals@1`

Native metric: `TechnicalManualsClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (427 bytes)
- `data/sample_submission.csv` (24015 bytes); columns: ["id", "label"]
- `data/test.csv` (517683 bytes); columns: ["id", "text", "manual_id"]
- `data/train.csv` (1929513 bytes); columns: ["id", "text", "label", "manual_id"]

## Public description

Technical Manual Section Classification Challenge

Contents (under public/):
- train.csv: Training set with columns [id, text, label, manual_id].
- test.csv: Test set with columns [id, text, manual_id]. No labels provided.
- sample_submission.csv: Template for submissions with columns [id, label].

Task: Predict the exact section heading (label) for each text excerpt in test.csv.
Evaluation: Macro F1 on the 'label' column.
