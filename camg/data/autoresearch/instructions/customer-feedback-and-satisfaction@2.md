# OpenMLE-fast task

Task ID: `customer-feedback-and-satisfaction@2`

Native metric: `CustomerSatisfactionTopBoxMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (564 bytes)
- `data/sample_submission.csv` (192203 bytes); columns: ["id", "TopBox"]
- `data/test.csv` (257726 bytes); columns: ["id", "Age", "Gender", "Country", "Income", "ProductQuality", "ServiceQuality", "PurchaseFrequency"]
- `data/train.csv` (1091278 bytes); columns: ["id", "Age", "Gender", "Country", "Income", "ProductQuality", "ServiceQuality", "PurchaseFrequency", "TopBox"]

## Public description

Customer Top-Box Satisfaction Classification

Files
- train.csv: Training data with features and the target column TopBox.
- test.csv: Test data with the same feature columns as train.csv (without TopBox).
- sample_submission.csv: Example submission file (columns: id, TopBox).

Columns
- id: Unique identifier for each row.
- Age, Gender, Country, Income, ProductQuality, ServiceQuality, PurchaseFrequency.
- TopBox (train only): 1 if satisfaction is at the top level, else 0.

Evaluation
- ROC-AUC on TopBox using your probabilities in sample_submission format.
