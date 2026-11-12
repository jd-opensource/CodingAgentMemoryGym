# OpenMLE-fast task

Task ID: `online-retails-sale-dataset@2`

Native metric: `RetailReturnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (307 bytes)
- `data/sample_submission.csv` (506826 bytes); columns: ["row_id", "returned_within_60d"]
- `data/test.csv` (5939389 bytes); columns: ["row_id", "InvoiceNo", "InvoiceDate", "InvoiceTime", "StockCode", "Description", "Quantity", "UnitPrice", "Totalsale", "CustomerID", "Country"]
- `data/train.csv` (23578105 bytes); columns: ["row_id", "InvoiceNo", "InvoiceDate", "InvoiceTime", "StockCode", "Description", "Quantity", "UnitPrice", "Totalsale", "CustomerID", "Country", "returned_within_60d"]

## Public description

Predict item returns within 60 days (Customer–SKU level)

Files
- train.csv: Training set with features and binary label 'returned_within_60d'.
- test.csv: Test set with the same features but without labels.
- sample_submission.csv: Example submission file with columns ['row_id', 'returned_within_60d'].
