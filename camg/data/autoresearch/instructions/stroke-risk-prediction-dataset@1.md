# OpenMLE-fast task

Task ID: `stroke-risk-prediction-dataset@1`

Native metric: `StrokeRiskRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (135 bytes)
- `data/sample_submission.csv` (423065 bytes); columns: ["id", "Stroke Risk (%)"]
- `data/test.csv` (682678 bytes); columns: ["id", "Chest Pain", "Shortness of Breath", "Irregular Heartbeat", "Fatigue & Weakness", "Dizziness", "Swelling (Edema)", "Pain in Neck/Jaw/Shoulder/Back", "Excessive Sweating", "Persistent Cough", "Nausea/Vomiting", "High Blood Pressure", "Chest Discomfort (Activity)", "Cold Hands/Feet", "Snoring/Sleep Apnea", "Anxiety/Feeling of Doom", "Age"]
- `data/train.csv` (2299344 bytes); columns: ["id", "Chest Pain", "Shortness of Breath", "Irregular Heartbeat", "Fatigue & Weakness", "Dizziness", "Swelling (Edema)", "Pain in Neck/Jaw/Shoulder/Back", "Excessive Sweating", "Persistent Cough", "Nausea/Vomiting", "High Blood Pressure", "Chest Discomfort (Activity)", "Cold Hands/Feet", "Snoring/Sleep Apnea", "Anxiety/Feeling of Doom", "Age", "Stroke Risk (%)"]

## Public description

Title: Stroke Risk Prediction (Regression)

Files:
- train.csv
- test.csv
- sample_submission.csv

Evaluation: RMSE on Stroke Risk (%)
