# OpenMLE-fast task

Task ID: `medical-insurance-cost-prediction@1`

Native metric: `MedicalInsuranceCostMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (436 bytes)
- `data/sample_submission.csv` (5901 bytes); columns: ["row_id", "charges"]
- `data/test.csv` (9072 bytes); columns: ["row_id", "age", "sex", "bmi", "children", "smoker", "region"]
- `data/train.csv` (43432 bytes); columns: ["age", "sex", "bmi", "children", "smoker", "region", "charges"]

## Public description

Task: Predict medical insurance charges (regression) from demographic and health features.

Files:
- train.csv: training data with columns [age, sex, bmi, children, smoker, region, charges].
- test.csv: test data with columns [row_id, age, sex, bmi, children, smoker, region].
- sample_submission.csv: example submission with columns [row_id, charges].

Submission format: CSV with columns [row_id, charges] for all row_id in test.csv.
