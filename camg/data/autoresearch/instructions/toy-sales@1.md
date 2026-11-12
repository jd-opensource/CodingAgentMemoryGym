# OpenMLE-fast task

Task ID: `toy-sales@1`

Native metric: `ToySalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1327 bytes)
- `data/inventory.csv` (13081 bytes); columns: ["Store_ID", "Product_ID", "Stock_On_Hand"]
- `data/products.csv` (1396 bytes); columns: ["Product_ID", "Product_Name", "Product_Category", "Product_Cost", "Product_Price"]
- `data/sample_submission.csv` (1660286 bytes); columns: ["row_id", "Units"]
- `data/stores.csv` (2948 bytes); columns: ["Store_ID", "Store_Name", "Store_City", "Store_Location", "Store_Open_Date"]
- `data/test.csv` (3682542 bytes); columns: ["row_id", "Date", "Store_ID", "Product_ID"]
- `data/train.csv` (17775121 bytes); columns: ["Date", "Store_ID", "Product_ID", "Units"]

## Public description

Mexico Toy Sales: Hierarchical Daily Demand Forecasting

Problem statement
Forecast daily unit demand for each store–product pair in a fictitious national toy retailer.

What to predict
- Target: Units (non-negative real) sold per day.
- Horizon: 92 consecutive days (2018-07-01 to 2018-09-30), inclusive.
- Granularity: Store_ID × Product_ID × Date.
- Submission format: CSV with columns [row_id, Units] that matches public/test.csv exactly.

Files in this directory (public/)
- train.csv: Daily unit sales for Store_ID × Product_ID × Date over the training window (2017-01-01 to 2018-06-30). Missing combinations are filled with Units = 0.
- test.csv: Rows to predict, columns [row_id, Date, Store_ID, Product_ID].
- sample_submission.csv: Example submission with valid row_id values and baseline Units.
- products.csv: Product metadata, including Product_ID, Product_Category, Product_Cost, Product_Price (as strings like '$9.99').
- stores.csv: Store metadata, including Store_ID, Store_City, Store_Location, Store_Open_Date.
- inventory.csv: Optional static feature (Store_ID × Product_ID snapshot of Stock_On_Hand).

Evaluation
- Primary metric used here for validation: RMSE on Units.
- Your submission must match public/test.csv row_id values exactly (no duplicates/missing), and contain a numeric Units column.
