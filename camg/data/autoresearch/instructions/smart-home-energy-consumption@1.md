# OpenMLE-fast task

Task ID: `smart-home-energy-consumption@1`

Native metric: `SmartHomeEnergyConsumptionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (259 bytes)
- `data/sample_submission.csv` (310970 bytes); columns: ["Id", "Energy Consumption (kWh)"]
- `data/test.csv` (541147 bytes); columns: ["Id", "Home ID", "Appliance Type", "Time", "Date", "Outdoor Temperature (°C)", "Household Size"]
- `data/train.csv` (4155268 bytes); columns: ["Id", "Home ID", "Appliance Type", "Energy Consumption (kWh)", "Time", "Date", "Outdoor Temperature (°C)", "Household Size"]

## Public description

Competition: Smart Home Appliance-Level Energy Prediction

Files in public/:
- train.csv
- test.csv
- sample_submission.csv

Submission format:
- CSV with columns: Id, Energy Consumption (kWh)

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE)
