# OpenMLE-fast task

Task ID: `cleaned-brazilian-ecommerce-data@1`

Native metric: `BrazilianEcommerceDeliveryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3761 bytes)
- `data/sample_submission.csv` (493927 bytes); columns: ["row_id", "is_late"]
- `data/test.csv` (6405204 bytes); columns: ["row_id", "order_id", "order_purchase_timestamp", "order_approved_at", "order_estimated_delivery_date", "geolocation_city_customer", "geolocation_state_customer", "product_id", "price", "freight_value", "shipping_limit_date", "product_category_name_english", "payment_type", "payment_value", "customer_zip_code_prefix", "geolocation_lat_customer", "geolocation_lng_customer", "seller_id", "seller_zip_code_prefix", "geolocation_lat_seller", "geolocation_lng_seller"]
- `data/train.csv` (25808928 bytes); columns: ["row_id", "order_id", "order_purchase_timestamp", "order_approved_at", "order_estimated_delivery_date", "geolocation_city_customer", "geolocation_state_customer", "product_id", "price", "freight_value", "shipping_limit_date", "product_category_name_english", "payment_type", "payment_value", "customer_zip_code_prefix", "geolocation_lat_customer", "geolocation_lng_customer", "seller_id", "seller_zip_code_prefix", "geolocation_lat_seller", "geolocation_lng_seller", "is_late"]

## Public description

Brazilian E‑Commerce: On‑Time Delivery Risk Prediction

Problem statement
Given only information known at purchase/approval time, predict the probability that an order‑item will be delivered late (after the marketplace’s estimated delivery date). Produce a probability score per order‑item to rank lateness risk.

Target
- is_late: binary target in train.csv where 1 = delivered after the estimated delivery date, 0 = delivered on/before the estimated date.

Files provided
- train.csv: Training data containing the features listed below plus the target is_late.
- test.csv: Test data with the same feature columns as train.csv and an identifier row_id, but without is_late.
- sample_submission.csv: Example submission with columns [row_id, is_late], where is_late is a probability in [0, 1].

Feature columns (present in both train.csv and test.csv)
- row_id: Unique row identifier for submission alignment.
- order_id: Order identifier (note: multiple items can share an order_id).
- order_purchase_timestamp: Purchase timestamp (string; parse to datetime for modeling).
- order_approved_at: Payment approval timestamp.
- order_estimated_delivery_date: Estimated delivery date provided to the customer.
- geolocation_city_customer: Customer city.
- geolocation_state_customer: Customer state.
- product_id: Product identifier.
- price: Item price.
- freight_value: Shipping cost.
- shipping_limit_date: Seller’s shipping deadline for the item.
- product_category_name_english: Product category.
- payment_type: Payment method (e.g., credit_card, boleto).
- payment_value: Total payment amount for the order.
- customer_zip_code_prefix: Customer ZIP prefix.
- geolocation_lat_customer: Customer latitude.
- geolocation_lng_customer: Customer longitude.
- seller_id: Seller identifier.
- seller_zip_code_prefix: Seller ZIP prefix.
- geolocation_lat_seller: Seller latitude.
- geolocation_lng_seller: Seller longitude.

Notes
- Labels are computed from realized delivery vs estimated dates, but realized timestamps are not included in train/test to prevent leakage.
- All rows correspond to delivered items. Non‑delivered orders are excluded.
- Expect class imbalance (late deliveries are a minority). Techniques for imbalanced learning are encouraged.

Evaluation
- Metric: Average Precision (area under the Precision‑Recall curve) on the positive class (is_late = 1). Higher is better.
- Submission format: A CSV with exactly two columns in this order: [row_id, is_late]. The is_late column must contain probabilities in [0, 1]. The set of row_id values must match those in test.csv (order does not matter).

Train/test split
- The data is pre‑split using a time‑based boundary on order_purchase_timestamp to emulate realistic deployment and avoid temporal leakage. Train on train.csv and predict on test.csv.

Modeling suggestions (optional)
- Temporal features: Parse timestamps; create day‑of‑week, hour‑of‑day, month/season; compute lead times (estimated minus purchase) and ship windows (shipping_limit minus approved_at).
- Geospatial features: Customer‑seller distance (e.g., haversine), regional indicators.
- High‑cardinality handling: For product_id and seller_id, consider target/hashing encoding or embeddings with regularization.
- Calibration and class imbalance: Use calibrated probabilities, class weights, resampling, or focal loss; tune decision thresholds for downstream use.

Rules and expectations
- Use only information available at or before purchase/approval time. External data may be used if it does not leak post‑purchase outcomes.
- Submissions must be deterministic and reproducible.
- Do not rely on private test labels; only submit probabilities for the provided row_id identifiers in test.csv.
