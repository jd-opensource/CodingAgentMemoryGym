# OpenMLE-fast task

Task ID: `sales-dataset@2`

Native metric: `SalesDeliveryDurationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2447 bytes)
- `data/sample_submission.csv` (35286 bytes); columns: ["order_id", "delivery_duration"]
- `data/test.csv` (301144 bytes); columns: ["order_id", "order_date", "ship_mode", "segment", "country", "city", "state", "postal_code", "region", "product_category_mode", "product_subcategory_mode", "product_count", "sales_sum", "quantity_sum", "discount_value_sum", "cogs_sum", "shipping_cost_per_unit", "shipping_cost_total", "regional_owner"]
- `data/train.csv` (605003 bytes); columns: ["order_id", "order_date", "ship_mode", "segment", "country", "city", "state", "postal_code", "region", "product_category_mode", "product_subcategory_mode", "product_count", "sales_sum", "quantity_sum", "discount_value_sum", "cogs_sum", "shipping_cost_per_unit", "shipping_cost_total", "regional_owner", "delivery_duration"]

## Public description

Competition: Amazon Order Delivery Duration (ETA) Prediction

Problem statement
Accurate delivery time estimates are crucial for customer satisfaction and logistics planning. You are provided with order-level records capturing ship mode, geography, customer segment, product mix, pricing signals, and dates. Your task is to predict the delivery duration in days (from order placement to delivery) using only order-at-booking attributes.

Files
- train.csv: Order-level records with features and the target column delivery_duration.
- test.csv: Order-level records with the same feature columns as train.csv but without delivery_duration.
- sample_submission.csv: A sample file showing the required submission format.

Target
- delivery_duration: Real-valued prediction of days between order and delivery. The observed target is integer in [0, 7], with distribution varying by ship mode and geography.

Features
Each row represents one customer order aggregated from line items. Columns include:
- order_id: Unique order identifier (string)
- order_date: Order placement date in ISO format (YYYY-MM-DD)
- ship_mode: Shipping service level (categorical)
- segment: Customer segment (categorical)
- country, city, state, postal_code, region: Geography (mixed types)
- product_category_mode, product_subcategory_mode: Most frequent product category and sub-category in the order (categorical)
- product_count: Number of distinct products in the order (integer)
- sales_sum, quantity_sum, discount_value_sum, cogs_sum: Aggregated numeric signals from line items (floats/integers)
- shipping_cost_per_unit: State-level shipping cost per unit (numeric)
- shipping_cost_total: shipping_cost_per_unit multiplied by quantity_sum (numeric)
- regional_owner: Regional owner mapped from region (categorical)
Only train.csv contains the target column delivery_duration. test.csv has identical feature columns without the target.

Evaluation
Submissions are evaluated using Root Mean Squared Error (RMSE) between your predictions and the hidden ground truth delivery_duration on the test set.
- Lower RMSE is better.
- Submission requirements:
  - CSV file with exactly two columns in this order: order_id, delivery_duration
  - The set of order_id must match test.csv exactly (no duplicates, no missing/extra IDs).
  - delivery_duration must be numeric and finite.

Submission format example
order_id,delivery_duration
CA-2017-123456,3.2
CA-2017-987654,4.0
...
