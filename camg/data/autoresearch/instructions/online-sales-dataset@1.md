# OpenMLE-fast task

Task ID: `online-sales-dataset@1`

Native metric: `OnlineSalesShippingCostMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (713 bytes)
- `data/sample_submission.csv` (231900 bytes); columns: ["Id", "ShippingCost"]
- `data/test.csv` (1356213 bytes); columns: ["Id", "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country", "Discount", "PaymentMethod", "Category", "SalesChannel", "ReturnStatus", "ShipmentProvider", "WarehouseLocation", "OrderPriority"]
- `data/train.csv` (5630242 bytes); columns: ["Id", "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country", "Discount", "PaymentMethod", "Category", "SalesChannel", "ReturnStatus", "ShipmentProvider", "WarehouseLocation", "OrderPriority", "ShippingCost"]

## Public description

Online Retail Shipping Cost Prediction (Regression)

Problem statement:
Predict the shipping cost for individual e-commerce orders using transactional and logistics attributes. Your task is to train a model on historical orders and generalize to future orders.

Final competition files:
- train.csv: Feature columns plus ShippingCost.
- test.csv: Feature columns only (no ShippingCost).
- sample_submission.csv: A valid example submission with columns [Id, ShippingCost].

Submission format:
- A CSV file with exactly two columns in this order: Id, ShippingCost.
- Ids must match those in test.csv exactly (one prediction per test row, no duplicates or missing rows).
- ShippingCost must be finite numeric values.
