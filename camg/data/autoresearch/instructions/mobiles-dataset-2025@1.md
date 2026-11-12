# OpenMLE-fast task

Task ID: `mobiles-dataset-2025@1`

Native metric: `SmartphonePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (145 bytes)
- `data/sample_submission.csv` (4262 bytes); columns: ["device_id", "USD_Price"]
- `data/test.csv` (31270 bytes); columns: ["device_id", "Company Name", "Model Name", "Mobile Weight", "RAM", "Front Camera", "Back Camera", "Processor", "Battery Capacity", "Screen Size", "Launched Year"]
- `data/train.csv` (65554 bytes); columns: ["device_id", "Company Name", "Model Name", "Mobile Weight", "RAM", "Front Camera", "Back Camera", "Processor", "Battery Capacity", "Screen Size", "Launched Year", "USD_Price"]

## Public description

Competition: Smartphone USD Launch Price Prediction (2025)

Files:
- train.csv
- test.csv
- sample_submission.csv

Evaluation: RMSLE on USD_Price
