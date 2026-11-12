# OpenMLE-fast task

Task ID: `prediksi-kelulusan@1`

Native metric: `GraduationPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (106 bytes)
- `data/sample_submission.csv` (594 bytes); columns: ["row_id", "label"]
- `data/test.csv` (3810 bytes); columns: ["row_id", "ips1", "ips2", "ips3", "ips4", "ips5", "ips6", "ips7", "ips8"]
- `data/train.csv` (15822 bytes); columns: ["row_id", "ips1", "ips2", "ips3", "ips4", "ips5", "ips6", "ips7", "ips8", "label"]

## Public description

Train and test CSVs for Prediksi Kelulusan competition. Files: train.csv, test.csv, sample_submission.csv.
