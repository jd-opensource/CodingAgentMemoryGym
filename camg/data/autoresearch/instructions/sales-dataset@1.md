# OpenMLE-fast task

Task ID: `sales-dataset@1`

Native metric: `SalesReturnRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2418 bytes)
- `data/sample_submission.csv` (57870 bytes); columns: ["order_id", "is_return_prob"]
- `data/test.csv` (313241 bytes); columns: ["order_id", "order_year", "order_month", "order_dayofweek", "sales_sum", "quantity_sum", "discount_value_sum", "profit_sum", "cogs_sum", "shipping_cost_total", "discount_mean", "delivery_duration_mean", "ship_mode_mode", "category_mode", "sub_category_mode", "state_mode", "region_mode", "owner_person", "discount_rate", "margin_rate"]
- `data/train.csv` (622292 bytes); columns: ["order_id", "order_year", "order_month", "order_dayofweek", "sales_sum", "quantity_sum", "discount_value_sum", "profit_sum", "cogs_sum", "shipping_cost_total", "discount_mean", "delivery_duration_mean", "ship_mode_mode", "category_mode", "sub_category_mode", "state_mode", "region_mode", "owner_person", "discount_rate", "margin_rate", "is_return"]

## Public description

Competition: Order Return Risk Prediction

Problem statement
Participants are challenged to predict the probability that an e-commerce order will be returned, using order-level transactional attributes available at the time of booking. The goal is to rank orders by return risk so that operations teams can prioritize mitigation.

Data description
- Train data (train.csv): Order-level aggregated features with the target label is_return (0/1). Each row represents one unique Order ID.
- Test data (test.csv): Same features as train.csv, without the label. Each row represents one unique Order ID.
- Sample submission (sample_submission.csv): Expected format of the predictions with two columns: order_id and is_return_prob.

Features are aggregated from line-level transactions into order-level signals. They include numerical totals and averages, categorical modes, and derived ratios known at order time:
- Totals: sales_sum, quantity_sum, discount_value_sum, profit_sum, cogs_sum, shipping_cost_total
- Averages: discount_mean, delivery_duration_mean
- Categorical modes: ship_mode_mode, category_mode, sub_category_mode, state_mode, region_mode, owner_person
- Date-derived: order_year, order_month, order_dayofweek
- Ratios: discount_rate = discount_value_sum / sales_sum, margin_rate = profit_sum / sales_sum

All features are computed from information available when the order is placed. Post-shipment or post-return information is excluded.

Evaluation
- Primary metric: Average Precision (Precision-Recall AUC) computed on order-level predicted probabilities. This metric is well-suited for class-imbalanced problems and rewards correct ranking of positive examples.

Submission format
- A single CSV file with exactly two columns:
  - order_id: the unique identifier of each order in the test set
  - is_return_prob: a probability score in [0, 1] indicating the likelihood of return

Train/test split
- The split is time-aware to simulate forward prediction: train includes earlier years, and test includes the most recent year. Both classes (returned vs non-returned) are present in the training set.

Files
- train.csv
- test.csv
- sample_submission.csv

Notes
- Participants are expected to perform data processing, feature engineering, model training, and evaluation with calibrated probability outputs.
- Metrics are calculated robustly to handle edge cases (e.g., ties) and ensure numerical stability.
