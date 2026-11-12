# OpenMLE-fast task

Task ID: `hospital-emergency-dataset@2`

Native metric: `HospitalERWaitTimeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (260 bytes)
- `data/sample_submission.csv` (20294 bytes); columns: ["row_id", "wait_above_45"]
- `data/test.csv` (99152 bytes); columns: ["row_id", "Patient Admission Date", "Patient Gender", "Patient Age", "Patient Race", "Department Referral"]
- `data/train.csv` (409386 bytes); columns: ["row_id", "Patient Admission Date", "Patient Gender", "Patient Age", "Patient Race", "Department Referral", "wait_above_45"]

## Public description

Emergency Room Wait-time Escalation Prediction

Files in this public directory:
- train.csv: Features + target (wait_above_45).
- test.csv: Features only; targets hidden.
- sample_submission.csv: Example submission format with columns [row_id, wait_above_45].
