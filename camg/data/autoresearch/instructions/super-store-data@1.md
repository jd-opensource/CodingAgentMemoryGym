# OpenMLE-fast task

Task ID: `super-store-data@1`

Native metric: `SuperStoreSalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (370 bytes)
- `data/sample_submission.csv` (228454 bytes); columns: ["id", "sales"]
- `data/test.csv` (305820 bytes); columns: ["id", "state", "category", "sub_category", "year", "month"]
- `data/train.csv` (3131056 bytes); columns: ["id", "state", "category", "sub_category", "year", "month", "sales", "quantity", "discount_mean", "ship_share_first_class", "ship_share_same_day", "ship_share_second_class", "ship_share_standard_class", "lead_time_mean_days", "n_unique_products"]

## Public description

Competition: Hierarchical Monthly Sales Forecasting (State × Category × Sub-Category)

Files provided under public/:
- train.csv
- test.csv
- sample_submission.csv

Data description (relative to public/):
- Train file: train.csv (2014-01 to 2017-06)
- Test file: test.csv (2017-07 to 2017-12, no labels)
- Sample submission: sample_submission.csv (columns: id, sales)
