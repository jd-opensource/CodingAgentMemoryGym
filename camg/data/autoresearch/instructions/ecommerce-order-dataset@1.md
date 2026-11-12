# OpenMLE-fast task

Task ID: `ecommerce-order-dataset@1`

Native metric: `ECommerceDeliveryDelayMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (420 bytes)
- `data/sample_submission.csv` (472715 bytes); columns: ["order_id", "delay_days"]
- `data/test.csv` (367188 bytes); columns: ["order_id"]
- `data/test_customers.csv` (893447 bytes); columns: ["customer_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
- `data/test_order_items.csv` (1367198 bytes); columns: ["order_id", "product_id", "seller_id", "price", "shipping_charges"]
- `data/test_orders.csv` (2045744 bytes); columns: ["order_id", "customer_id", "order_purchase_timestamp", "order_approved_at", "order_estimated_delivery_date"]
- `data/test_payments.csv` (930610 bytes); columns: ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]
- `data/test_products.csv` (2876193 bytes); columns: ["product_id", "product_category_name", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
- `data/train.csv` (1102981 bytes); columns: ["order_id", "delay_days"]
- `data/train_customers.csv` (2084915 bytes); columns: ["customer_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
- `data/train_order_items.csv` (3189206 bytes); columns: ["order_id", "product_id", "seller_id", "price", "shipping_charges"]
- `data/train_orders.csv` (5019432 bytes); columns: ["order_id", "customer_id", "order_purchase_timestamp", "order_approved_at", "order_estimated_delivery_date", "delay_days"]
- `data/train_payments.csv` (2170285 bytes); columns: ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]
- `data/train_products.csv` (3527865 bytes); columns: ["product_id", "product_category_name", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]

## Public description

Predict E-commerce Delivery Delay (Days Beyond Estimate)

Files in this competition (under public/):
train_orders.csv
train_order_items.csv
train_customers.csv
train_payments.csv
train_products.csv
test_orders.csv
test_order_items.csv
test_customers.csv
test_payments.csv
test_products.csv
train.csv
test.csv
sample_submission.csv

Submit a CSV with columns [order_id, delay_days]. Evaluation uses MAE (lower is better).
