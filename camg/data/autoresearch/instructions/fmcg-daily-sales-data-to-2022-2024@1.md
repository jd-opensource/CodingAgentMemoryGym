# OpenMLE-fast task

Task ID: `fmcg-daily-sales-data-to-2022-2024@1`

Native metric: `FMCGSalesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (351 bytes)
- `data/sample_submission.csv` (136468 bytes); columns: ["row_id", "units_sold"]
- `data/test.csv` (1113152 bytes); columns: ["row_id", "date", "sku", "brand", "segment", "category", "channel", "region", "pack_type", "price_unit", "promotion_flag", "delivery_days", "stock_available", "delivered_qty"]
- `data/train.csv` (17892795 bytes); columns: ["row_id", "date", "sku", "brand", "segment", "category", "channel", "region", "pack_type", "price_unit", "promotion_flag", "delivery_days", "stock_available", "delivered_qty", "units_sold"]

## Public description

FMCG Daily Multiseries One-Day-Ahead Forecasting
Data files (relative to public/):
- train.csv
- test.csv
- sample_submission.csv

Target and format:
- Predict 'units_sold' for each row in test.csv and submit a CSV with columns ['row_id','units_sold'].

Evaluation:
- RMSLE on all test rows. Predictions are clipped to be non-negative during scoring.
