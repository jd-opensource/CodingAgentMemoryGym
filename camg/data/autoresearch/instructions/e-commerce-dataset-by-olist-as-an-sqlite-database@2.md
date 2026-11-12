# OpenMLE-fast task

Task ID: `e-commerce-dataset-by-olist-as-an-sqlite-database@2`

Native metric: `OlistReviewKappaMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2797 bytes)
- `data/sample_submission.csv` (3395253 bytes); columns: ["order_id", "p1", "p2", "p3", "p4", "p5"]
- `data/test.csv` (6416280 bytes); columns: ["order_id", "purchase_weekday", "purchase_hour", "purchase_month", "promised_lead_days", "shipping_window_days", "number_of_items", "total_item_price", "avg_item_price", "max_item_price", "total_freight_value", "avg_freight_value", "freight_share", "sum_weight_g", "mean_weight_g", "sum_volume_cm3", "mean_volume_cm3", "sum_photos_qty", "mean_photos_qty", "mean_name_length", "mean_description_length", "mean_distance_km", "min_distance_km", "max_distance_km", "same_state_share", "distinct_categories", "total_payment_value", "max_installments", "payment_records", "pay_share_boleto", "pay_share_credit_card", "pay_share_debit_card", "pay_share_not_defined", "pay_share_voucher", "customer_state", "seller_state_mode"]
- `data/train.csv` (18320789 bytes); columns: ["order_id", "purchase_weekday", "purchase_hour", "purchase_month", "promised_lead_days", "shipping_window_days", "number_of_items", "total_item_price", "avg_item_price", "max_item_price", "total_freight_value", "avg_freight_value", "freight_share", "sum_weight_g", "mean_weight_g", "sum_volume_cm3", "mean_volume_cm3", "sum_photos_qty", "mean_photos_qty", "mean_name_length", "mean_description_length", "mean_distance_km", "min_distance_km", "max_distance_km", "same_state_share", "distinct_categories", "total_payment_value", "max_installments", "payment_records", "pay_share_boleto", "pay_share_credit_card", "pay_share_debit_card", "pay_share_not_defined", "pay_share_voucher", "customer_state", "seller_state_mode", "review_score"]

## Public description

Title: Predict post‑purchase customer ratings (1–5 stars) at checkout

Background
Customer satisfaction in marketplaces depends on product mix, shipping promise, payment experience, and logistics. Accurately forecasting ratings at checkout enables proactive interventions (e.g., setting realistic delivery promises, routing orders differently, or adjusting payment plans).

Problem statement
Given only information available at checkout, predict the star rating (1–5) a buyer will later leave for the order. This is an ordinal classification task with imbalanced classes.

Provided data
You will receive tabular order‑level data capturing signals available at purchase time, including:
- Temporal features: purchase weekday/hour/month; promised lead days; shipping window.
- Basket economics: number of items; total/average/max item price; freight value and freight share.
- Payment features: total payment value; installment count; average installment value; payment type shares.
- Product physicals (aggregated): weights; volumetric size; photos count; name/description length stats.
- Geo/logistics: approximate buyer–seller distance (aggregated mean/min/max); same‑state flag.
- Identifier: order_id is included to align predictions; do not use it as a feature.

Files
- train.csv: order_id, purchase‑time features, and the target column review_score (integer ∈ {1,2,3,4,5}).
- test.csv: order_id and the same purchase‑time features (no target).
- sample_submission.csv: demonstration of the required submission format.

Target and constraints
- Target: review_score ∈ {1,2,3,4,5} for orders that have a review.
- Use only purchase‑time signals; delivery outcomes, review texts, and post‑purchase timestamps are excluded to prevent leakage.
- Train/test are split by purchase timestamp to emulate deployment on future data.

Submission format
Submit a CSV with the following columns:
- order_id
- p1, p2, p3, p4, p5 (the predicted probabilities for each star rating 1–5)
Each row’s probabilities must be non‑negative and sum to 1. The leaderboard evaluation converts probabilities to a predicted class using argmax.

Evaluation metric
Quadratic Weighted Kappa (QWK) on 1–5 stars. QWK accounts for the ordinal nature of ratings and penalizes distant misclassifications more than near misses, while being robust to class imbalance. The leaderboard uses QWK exclusively.

Notes
- The dataset is sizable and rich; strong solutions will require careful data processing, feature engineering, and modeling (e.g., gradient boosting, calibrated ordinal classifiers, or cost‑sensitive training).
- Time awareness is important to avoid train–test contamination across seasonality.
- Review texts and post‑purchase delivery timestamps are intentionally not provided.
