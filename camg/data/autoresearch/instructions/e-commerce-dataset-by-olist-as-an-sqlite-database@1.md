# OpenMLE-fast task

Task ID: `e-commerce-dataset-by-olist-as-an-sqlite-database@1`

Native metric: `OlistLateDeliveryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4279 bytes)
- `data/sample_submission.csv` (1090172 bytes); columns: ["order_id", "late_delivery_probability"]
- `data/test.csv` (5640740 bytes); columns: ["order_id", "temporal_purchase_weekday", "temporal_purchase_hour", "temporal_purchase_month", "promised_lead_days", "shipping_limit_delta_days_min", "shipping_limit_delta_days_max", "basket_item_count", "basket_total_item_price", "basket_total_freight_value", "basket_avg_item_price", "basket_max_item_price", "payment_value_total", "payment_installments_sum", "payment_installments_max", "payment_type_primary", "payment_method_count", "product_weight_g_sum", "product_weight_g_mean", "product_volume_cm3_sum", "product_volume_cm3_mean", "product_photos_qty_sum", "product_photos_qty_mean", "product_name_length_mean", "product_description_length_mean", "product_category_count", "product_top_category_english", "geo_distance_km_mean", "geo_distance_km_min", "geo_distance_km_max", "geo_same_state_share", "customer_state", "majority_seller_state"]
- `data/train.csv` (15974774 bytes); columns: ["order_id", "temporal_purchase_weekday", "temporal_purchase_hour", "temporal_purchase_month", "promised_lead_days", "shipping_limit_delta_days_min", "shipping_limit_delta_days_max", "basket_item_count", "basket_total_item_price", "basket_total_freight_value", "basket_avg_item_price", "basket_max_item_price", "payment_value_total", "payment_installments_sum", "payment_installments_max", "payment_type_primary", "payment_method_count", "product_weight_g_sum", "product_weight_g_mean", "product_volume_cm3_sum", "product_volume_cm3_mean", "product_photos_qty_sum", "product_photos_qty_mean", "product_name_length_mean", "product_description_length_mean", "product_category_count", "product_top_category_english", "geo_distance_km_mean", "geo_distance_km_min", "geo_distance_km_max", "geo_same_state_share", "customer_state", "majority_seller_state", "late_delivery"]

## Public description

Competition: Predict late deliveries at purchase-time in Brazilian e-commerce

Background
Logistics delays drive customer churn and costs. This competition uses a comprehensive marketplace dataset to challenge participants to predict, at the moment of purchase, whether an order will be delivered later than the promised date. The data includes order-level signals, basket composition, payments, product attributes, and approximate customer–seller geography inferred from ZIP codes.

Problem statement
Given features that are available at purchase-time, build a model to estimate the probability that an order will be delivered after its estimated delivery date. Outputs should be calibrated probabilities per order.

Provided data files
- train.csv: Tabular features for each order and the target label late_delivery (1 if late, 0 otherwise).
- test.csv: Same features as train.csv but without the target label.
- sample_submission.csv: Example of the required submission format.

Target and split
- Target: late_delivery (binary), defined from delivered orders as 1 when actual delivery occurs after the estimated date.
- Split: Strict time-based split on the order purchase timestamp (training earlier period, test later period) to emulate real-world deployment and prevent look-ahead.

Feature overview (columns in train/test)
Each row represents one order (order_id is the identifier; do not use it as a feature).
- order_id: Unique order identifier, required for submission mapping.
- temporal_purchase_weekday: Purchase day of week [0-6].
- temporal_purchase_hour: Purchase hour [0-23].
- temporal_purchase_month: Purchase calendar month [1-12].
- promised_lead_days: Days between purchase time and the promised (estimated) delivery date.
- shipping_limit_delta_days_min: Minimum days between purchase and the seller’s shipping limit date across items in the basket.
- shipping_limit_delta_days_max: Maximum days between purchase and the seller’s shipping limit date across items in the basket.
- basket_item_count: Number of items in the order.
- basket_total_item_price: Sum of item prices.
- basket_total_freight_value: Sum of freight values.
- basket_avg_item_price: Average item price.
- basket_max_item_price: Maximum item price.
- payment_value_total: Sum of payment values across payment records.
- payment_installments_sum: Sum of installments.
- payment_installments_max: Maximum number of installments.
- payment_type_primary: Most frequent payment type for the order.
- payment_method_count: Number of distinct payment methods used.
- product_weight_g_sum, product_weight_g_mean: Aggregated product weights.
- product_volume_cm3_sum, product_volume_cm3_mean: Aggregated volumetric size (L*W*H) of products.
- product_photos_qty_sum, product_photos_qty_mean: Aggregated product photo counts.
- product_name_length_mean, product_description_length_mean: Aggregated text length proxies.
- product_category_count: Number of distinct product categories in the basket.
- product_top_category_english: Dominant product category (English translation when available; otherwise original or "unknown").
- geo_distance_km_mean, geo_distance_km_min, geo_distance_km_max: Great-circle distance between customer and sellers aggregated over items.
- geo_same_state_share: Share of items where seller_state equals customer_state.
- customer_state: Customer state.
- majority_seller_state: Most frequent seller state in the basket.

Evaluation
Primary metric: Average Precision (area under the precision–recall curve, AP) for the positive class (late deliveries). AP focuses on ranking performance and is well-suited for imbalanced data. Submissions must provide a probability for each order in the test set.

Submission format
- A CSV file with two columns: order_id and late_delivery_probability.
- Each order_id must appear exactly once, matching those in test.csv.
- Probabilities must be numeric in [0, 1].

Notes
- Features strictly respect the purchase-time constraint; any post-purchase information (e.g., actual delivery dates, reviews) is excluded from the features.
- Participants are encouraged to engineer additional features, handle class imbalance, and calibrate predictions.
- Ensure robust cross-validation using time-aware strategies to avoid leakage.
