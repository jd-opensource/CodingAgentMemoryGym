# OpenMLE-fast task

Task ID: `smartphone-features-dataset@1`

Native metric: `BatteryRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (404 bytes)
- `data/sample_submission.csv` (1779 bytes); columns: ["id", "battery_mAh"]
- `data/test.csv` (36053 bytes); columns: ["id", "Name", "Dimensions", "SoC", "CPU", "GPU", "RAM", "Storage", "Display", "OS"]
- `data/train.csv` (147279 bytes); columns: ["id", "Name", "Dimensions", "SoC", "CPU", "GPU", "RAM", "Storage", "Display", "OS", "battery_mAh"]

## Public description

Samsung Battery Capacity Prediction Challenge

Files
- train.csv: Training set with features and target battery_mAh.
- test.csv: Test set with the same feature columns (without battery_mAh).
- sample_submission.csv: Template showing the required submission format.

Submission
- Submit a CSV with exactly two columns: id,battery_mAh
- The id values must match those in test.csv and be in the same order.
