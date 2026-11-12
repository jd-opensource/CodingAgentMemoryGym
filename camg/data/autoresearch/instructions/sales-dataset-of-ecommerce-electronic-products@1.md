# OpenMLE-fast task

Task ID: `sales-dataset-of-ecommerce-electronic-products@1`

Native metric: `SalesDemandRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2626 bytes)
- `data/sample_submission.csv` (336395 bytes); columns: ["row_id", "qty"]
- `data/test.csv` (2346975 bytes); columns: ["row_id", "product", "city", "state", "timestamp_hour", "month", "dow", "hour"]
- `data/train.csv` (7843605 bytes); columns: ["product", "city", "state", "timestamp_hour", "month", "dow", "hour", "qty"]

## Public description

Competition: Hourly Product-by-City Demand Forecasting (Electronics E‑commerce, 2019)

Problem statement
Participants must forecast the number of items ordered at an hourly granularity for each product–city pair in a US electronics e‑commerce store. The training data covers January through October 2019, and the test data covers November through December 2019. Each row represents the total quantity ordered for a specific hour, product, and city, with calendar features provided.

Files provided
- train.csv: Training set with features and target.
- test.csv: Test set with the same features but without target.
- sample_submission.csv: Example submission file aligned to test rows.

Data description
Each row corresponds to a single time point at hourly resolution for a product and city.
Columns:
- row_id: Unique identifier only in test.csv and sample_submission.csv (defines the prediction order).
- product: Product name (string).
- city: City name parsed from purchase address.
- state: Two-letter US state abbreviation.
- timestamp_hour: Timestamp of the hour (YYYY-MM-DD HH:00:00).
- month: Month number (1–12).
- dow: Day of week (0=Monday, 6=Sunday).
- hour: Hour of day (0–23).
- qty: Target variable (integer count of items ordered in that hour). Present only in train.csv.

Task
Predict qty for every row in test.csv, providing one non-negative numeric value per row_id in sample_submission.csv. The test rows align exactly with the row_id ordering.

Evaluation
Submissions are evaluated using RMSLE (Root Mean Squared Log Error) on qty with a log1p transformation:
- RMSLE = sqrt(mean((log1p(q_true) - log1p(q_pred))^2))
- q_pred values are clipped to be non-negative before scoring.
RMSLE is appropriate for count data with heavy tails and zeros, rewarding accurate relative error across demand levels.

Train/test split
- Training period: January–October 2019.
- Test period: November–December 2019.
- All products and cities that appear in test also appear in train at least once.

Submission format
- A CSV with columns exactly: row_id, qty.
- row_id must match the order in test.csv.
- qty must be numeric, finite, and non-negative.

Notes and guidance
- Use calendar features (month, dow, hour) to model seasonality and weekly patterns.
- Consider interactions among product, city, and hour; demand spikes around holidays and weekends are prominent.
- Methods such as gradient-boosted trees, generalized linear models, or time-series models per (product, city) can perform well. Feature engineering can incorporate lag features, rolling statistics, holiday flags, and cross-entity pooling.
