# OpenMLE-fast task

Task ID: `stroke-diagnosis-and-health-metrics-data@1`

Native metric: `StrokeRiskPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (280 bytes)
- `data/sample_submission.csv` (21400 bytes); columns: ["Id", "Stroke"]
- `data/test.csv` (209182 bytes); columns: ["Id", "Age", "Gender", "SES", "Hypertension", "Heart_Disease", "BMI", "Avg_Glucose", "Diabetes", "Smoking_Status"]
- `data/train.csv` (644628 bytes); columns: ["Id", "Age", "Gender", "SES", "Hypertension", "Heart_Disease", "BMI", "Avg_Glucose", "Diabetes", "Smoking_Status", "Stroke"]

## Public description

Competition: Stroke Risk Prediction Challenge

Files in this public directory:
- train.csv: Training data with features and target column 'Stroke'
- test.csv: Test data with features only and an 'Id' column
- sample_submission.csv: Example submission with columns ['Id', 'Stroke']
