# OpenMLE-fast task

Task ID: `superstore-dataset@2`

Native metric: `SuperstoreProfitMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (237 bytes)
- `data/sample_submission.csv` (57072 bytes); columns: ["OrderID", "Profit"]
- `data/test.csv` (252688 bytes); columns: ["OrderID", "CustomerID", "Country", "State", "City", "PostalCode", "Region", "Segment", "ShipMode", "Manager", "SumSales", "SumQuantity", "MeanDiscount", "NumItems", "NumUniqueProductID", "NumUniqueCategory", "NumUniqueSubCategory", "OrderYear", "OrderMonth", "OrderISOWeek", "OrderDayOfWeek", "OrderQuarter"]
- `data/train.csv` (549319 bytes); columns: ["OrderID", "CustomerID", "Country", "State", "City", "PostalCode", "Region", "Segment", "ShipMode", "Manager", "SumSales", "SumQuantity", "MeanDiscount", "NumItems", "NumUniqueProductID", "NumUniqueCategory", "NumUniqueSubCategory", "OrderYear", "OrderMonth", "OrderISOWeek", "OrderDayOfWeek", "OrderQuarter", "Profit"]

## Public description

Superstore Order Profit Forecasting

Files:
- train.csv: Training data with features and target Profit.
- test.csv: Test data with features only (Profit not included).
- sample_submission.csv: Example submission format (OrderID, Profit).
