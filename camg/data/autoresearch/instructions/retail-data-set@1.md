# OpenMLE-fast task

Task ID: `retail-data-set@1`

Native metric: `RetailDemandForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (370 bytes)
- `data/sample_submission.csv` (5899080 bytes); columns: ["source", "product_id", "date", "quantity"]
- `data/test.csv` (4791563 bytes); columns: ["source", "product_id", "date"]
- `data/train.csv` (994851 bytes); columns: ["source", "product_id", "date", "quantity"]

## Public description

Title: Hierarchical Multi-Series Retail Demand Forecasting (Dual-Source)

Files in this folder:
- train.csv: Columns [source, product_id, date, quantity].
- test.csv: Columns [source, product_id, date].
- sample_submission.csv: Columns [source, product_id, date, quantity].

Submission
- Submit a CSV with the same columns and keys as test.csv plus the quantity column.
