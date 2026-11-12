# OpenMLE-fast task

Task ID: `hair-health@1`

Native metric: `HairHealthRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (503 bytes)
- `data/sample_submission.csv` (6961 bytes); columns: ["Id", "HairLoss"]
- `data/test.csv` (15931 bytes); columns: ["Id", "Genetics", "Hormonal_Changes", "Nutritional_Deficiencies", "Stress", "Age", "Poor_Hair_Care_Habits", "Environmental_Factors", "Smoking", "Weight_Loss"]
- `data/train.csv` (38053 bytes); columns: ["Id", "Genetics", "Hormonal_Changes", "Nutritional_Deficiencies", "Stress", "Age", "Poor_Hair_Care_Habits", "Environmental_Factors", "Smoking", "Weight_Loss", "HairLoss"]

## Public description

Hair Health Risk Prediction (Tabular Binary Classification)

Files in this directory:
- train.csv: Labeled training data with feature columns and target HairLoss.
- test.csv: Unlabeled test data with the same feature columns as train.csv except HairLoss.
- sample_submission.csv: Example submission with the required columns (Id,HairLoss).

Submission format:
- CSV with header: Id,HairLoss
- One row per Id in test.csv; HairLoss is a probability in [0, 1].

Primary metric: ROC AUC (higher is better).
