# OpenMLE-fast task

Task ID: `ufc-datasets-1994-2025@2`

Native metric: `UFCFinishMethodMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (548 bytes)
- `data/sample_submission.csv` (121766 bytes); columns: ["fight_id", "Decision", "KO/TKO", "Submission"]
- `data/test.csv` (156738 bytes); columns: ["fight_id", "r_id", "b_id", "r_name", "b_name", "division", "title_fight"]
- `data/train.csv` (685994 bytes); columns: ["fight_id", "r_id", "b_id", "r_name", "b_name", "division", "title_fight", "finish_type"]

## Public description

Competition: Predict the UFC Finish Method (pre-fight tri-class)

Files:
- train.csv: Training data with columns [fight_id, r_id, b_id, r_name, b_name, division, title_fight, finish_type].
- test.csv: Test data with the same feature columns as train.csv but without finish_type.
- sample_submission.csv: Expected submission format with columns [fight_id, Decision, KO/TKO, Submission].

Task:
- Predict probabilities for each finish type (Decision, KO/TKO, Submission) for every fight_id in test.csv.
- The probabilities in each row must sum to 1.
