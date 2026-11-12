# OpenMLE-fast task

Task ID: `depression-surveydataset-for-analysis@1`

Native metric: `DepressionRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (343 bytes)
- `data/sample_submission.csv` (4388 bytes); columns: ["id", "Depression"]
- `data/test.csv` (49816 bytes); columns: ["id", "Gender", "Age", "City", "Working Professional or Student", "Profession", "Academic Pressure", "Work Pressure", "CGPA", "Study Satisfaction", "Job Satisfaction", "Sleep Duration", "Dietary Habits", "Degree", "Work/Study Hours", "Financial Stress", "Family History of Mental Illness"]
- `data/train.csv` (204444 bytes); columns: ["id", "Gender", "Age", "City", "Working Professional or Student", "Profession", "Academic Pressure", "Work Pressure", "CGPA", "Study Satisfaction", "Job Satisfaction", "Sleep Duration", "Dietary Habits", "Degree", "Work/Study Hours", "Financial Stress", "Family History of Mental Illness", "Depression"]

## Public description

Non-clinical Depression Risk Prediction

Files in this directory:
- train.csv: Training data with id, features, and the target column 'Depression'.
- test.csv: Test data with id and features (no target labels).
- sample_submission.csv: Example submission format with columns ['id', 'Depression'] where 'Depression' are probabilities in [0,1].
