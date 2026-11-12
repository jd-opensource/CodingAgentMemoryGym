# OpenMLE-fast task

Task ID: `transactional-retail-dataset-of-electronics-store@1`

Native metric: `RetailDeliveryChargesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3615 bytes)
- `data/sample_submission.csv` (7056 bytes); columns: ["order_id", "delivery_charges"]
- `data/test.csv` (60957 bytes); columns: ["order_id", "customer_id", "date", "nearest_warehouse", "shopping_cart", "order_price", "coupon_discount", "customer_lat", "customer_long", "season", "is_expedited_delivery", "distance_to_nearest_warehouse", "dist_nickolson", "dist_thompson", "dist_bakers", "distance_to_nearest_warehouse_recomputed", "nearest_warehouse_recomputed", "chosen_warehouse_is_true_nearest"]
- `data/train.csv` (187274 bytes); columns: ["order_id", "customer_id", "date", "nearest_warehouse", "shopping_cart", "order_price", "coupon_discount", "customer_lat", "customer_long", "season", "is_expedited_delivery", "distance_to_nearest_warehouse", "dist_nickolson", "dist_thompson", "dist_bakers", "distance_to_nearest_warehouse_recomputed", "nearest_warehouse_recomputed", "chosen_warehouse_is_true_nearest", "delivery_charges"]

## Public description

Title: Geospatial Retail Pricing — Predict Delivery Charges for an Online Electronics Store

Problem statement
You are given transactional records from an online electronics retailer that fulfills orders from three warehouses. Your task is to predict the delivery_charges (USD) for future orders using order attributes, customer location, and warehouse information. This is a tabular regression challenge that rewards robust preprocessing, feature engineering (especially geospatial), and generalization across time.

Data description
Final competition files:
- train.csv: Training rows with features and the target column delivery_charges.
- test.csv: Test rows with features only; delivery_charges is withheld.
- sample_submission.csv: A sample submission showing the required format.

Columns (typical fields)
- order_id: Unique identifier for each order.
- customer_id: Unique identifier for the customer.
- date: Order date (ISO format). Chronology matters.
- nearest_warehouse: Cleaned warehouse name for fulfillment (Nickolson, Thompson, Bakers).
- shopping_cart: Stringified list of (item_name, quantity) tuples for basket composition.
- order_price: Pre-discount item total (USD).
- coupon_discount: Percentage discount applied to order_price.
- customer_lat, customer_long: Customer location.
- season: Season when the order was placed (Winter, Spring, Summer, Autumn).
- is_expedited_delivery: Whether expedited delivery was requested.
- distance_to_nearest_warehouse: Provided arc distance in km (may contain anomalies).
- dist_nickolson, dist_thompson, dist_bakers: Recomputed haversine distances to each warehouse (km).
- distance_to_nearest_warehouse_recomputed: Minimum of recomputed distances.
- nearest_warehouse_recomputed: The truly nearest warehouse based on recomputed distances.
- chosen_warehouse_is_true_nearest: Indicator whether the chosen warehouse equals the recomputed nearest.

Notes and guidance
- Participants are expected to parse and engineer shopping_cart features (e.g., total quantity, diversity, bulky vs compact items) and explore interactions between distance, seasonality, and expedited delivery.
- Geospatial features are central. The provided recomputed distances help mitigate anomalies; further distance features and checks are encouraged.
- Text fields (latest_customer_review) and customer satisfaction (is_happy_customer) are unrelated to delivery pricing and may introduce noise.
- order_total can be inconsistent; prefer deriving totals from order_price and coupon_discount if needed.

Train/test split
- The split is strictly chronological to simulate predicting future orders: approximately the last quarter of the timeline is reserved for test.

Evaluation
- Metric: Mean Absolute Error (MAE) between submitted delivery_charges and ground truth on the test set.
- Rationale: MAE is robust to outliers and directly measures error in USD, aligning with business impact.

Submission format
- CSV with two columns: order_id and delivery_charges.
- Each order_id in test.csv must appear exactly once. delivery_charges must be numeric and finite.

What is provided
- All rows with valid delivery_charges are preserved to maximize task scale.
- Warehouse coordinates have been used to recompute distances and cross-check nearest_warehouse.

Challenge highlights
- Requires consistent cleaning of date formats and categorical casing, robust geospatial computations, careful basket parsing, and modeling non-linear price determinants.
- Tabular ML models (GBMs, regularized linear models, neural nets) can perform well with thoughtful features and temporal awareness.
