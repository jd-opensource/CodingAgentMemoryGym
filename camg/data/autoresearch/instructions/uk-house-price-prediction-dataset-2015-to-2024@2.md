# OpenMLE-fast task

Task ID: `uk-house-price-prediction-dataset-2015-to-2024@2`

Native metric: `UKHousePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (459 bytes)
- `data/sample_submission.csv` (655814 bytes); columns: ["row_id", "price"]
- `data/test.csv` (2453871 bytes); columns: ["date", "postcode", "property_type", "new_build", "freehold", "street", "locality", "town", "district", "county", "row_id"]
- `data/train.csv` (6201037 bytes); columns: ["price", "date", "postcode", "property_type", "new_build", "freehold", "street", "locality", "town", "district", "county", "row_id"]

## Public description

Competition: UK House Price Cold-Start Generalization (2015–2024)

Files in this directory:
- train.csv: Training data with features and target column price.
- test.csv: Test data with the same features as train.csv plus row_id, but without price.
- sample_submission.csv: Example submission with columns [row_id, price].

Evaluation: RMSLE on price. Lower is better.
Submission format: CSV with columns [row_id, price]; row_id must exactly match test.csv.
