# OpenMLE-fast task

Task ID: `turbo-azcar-marketplace-cars-dataset@2`

Native metric: `AzCarMileageRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (362 bytes)
- `data/sample_submission.csv` (29945 bytes); columns: ["id", "target_km"]
- `data/test.csv` (175566 bytes); columns: ["id", "Brand", "Model", "Price", "Currency", "Year", "Engine Size", "Horsepower", "Fuel Type", "Color", "Body Type", "Transmission", "Drive Type", "Seats", "Owners", "Condition", "Market", "City"]
- `data/train.csv` (747457 bytes); columns: ["id", "Brand", "Model", "Price", "Currency", "Year", "Engine Size", "Horsepower", "Fuel Type", "Color", "Body Type", "Transmission", "Drive Type", "Seats", "Owners", "Condition", "Market", "City", "target_km"]

## Public description

Title: Azerbaijan Used‑Car Mileage Estimation

Files
- train.csv: Training data with features and target_km.
- test.csv: Test data with the same features (no target).
- sample_submission.csv: Example submission format.

Target
- target_km: Kilometers driven.

Evaluation
- Metric: RMSLE on target_km.
- Submission must have exactly two columns: id, target_km.
