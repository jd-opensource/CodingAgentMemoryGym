# OpenMLE-fast task

Task ID: `blinkit-sales-dataset@1`

Native metric: `BlinkitSalesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1559 bytes)
- `data/sample_submission.csv` (48570 bytes); columns: ["row_id", "Sales"]
- `data/test.csv` (76860 bytes); columns: ["row_id", "ItemContentKey", "Item Identifier", "ItemKey", "OutletKey", "Item Visibility", "Item Weight", "Rating"]
- `data/train.csv` (299217 bytes); columns: ["row_id", "ItemContentKey", "Item Identifier", "ItemKey", "OutletKey", "Item Visibility", "Item Weight", "Sales", "Rating"]

## Public description

```
description.txt (43 lines)
sample_submission.csv (2035 lines)
test.csv (2035 lines)
train.csv (6490 lines)```

-> sample_submission.csv has 2034 rows and 2 columns.
Here is some information about the columns:
Sales (float64) has 1 unique values: [140.91811893974418]
row_id (int64) has range: 2.00 - 8517.00, 0 nan values

-> test.csv has 2034 rows and 8 columns.
Here is some information about the columns:
Item Identifier (object) has 1168 unique values. Some example values: ['FDX40', 'DRM37', 'FDI41', 'FDR37']
Item Visibility (float64) has range: 0.00 - 0.33, 0 nan values
Item Weight (float64) has range: 4.55 - 21.35, 338 nan values
ItemContentKey (int64) has 2 unique values: [1, 2]
ItemKey (int64) has range: 1.00 - 16.00, 0 nan values
OutletKey (int64) has range: 1.00 - 16.00, 0 nan values
Rating (float64) has range: 1.00 - 5.00, 0 nan values
row_id (int64) has range: 2.00 - 8517.00, 0 nan values

-> train.csv has 6489 rows and 9 columns.
Here is some information about the columns:
Item Identifier (object) has 1556 unique values. Some example values: ['NCY18', 'FDX04', 'FDV38', 'DRN47']
Item Visibility (float64) has range: 0.00 - 0.33, 0 nan values
Item Weight (float64) has range: 4.55 - 21.35, 1125 nan values
ItemContentKey (int64) has 2 unique values: [1, 2]
ItemKey (int64) has range: 1.00 - 16.00, 0 nan values
OutletKey (int64) has range: 1.00 - 16.00, 0 nan values
Rating (float64) has range: 1.00 - 5.00, 0 nan values
Sales (float64) has range: 31.29 - 266.89, 0 nan values
row_id (int64) has range: 0.00 - 8522.00, 0 nan values
