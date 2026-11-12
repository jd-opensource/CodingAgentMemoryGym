# OpenMLE-fast task

Task ID: `united-state-superstore-sales@2`

Native metric: `SuperstoreShipLagRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3256 bytes)
- `data/sample_submission.csv` (29522 bytes); columns: ["row_id", "ship_lag_days"]
- `data/test.csv` (624987 bytes); columns: ["row_id", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount"]
- `data/train.csv` (1271632 bytes); columns: ["row_id", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "ship_lag_days"]

## Public description

Superstore Shipment ETA (Days-to-Ship Regression)

Problem statement
Predict the number of days between order placement and shipment for each order line. Using the tabular order details available at order time, your task is to estimate ship_lag_days (integer days from Order Date to Ship Date). This enables better customer expectation setting and fulfillment planning.

Files
- train.csv: Training data with features and the target ship_lag_days.
- test.csv: Test data with the same features as train.csv but without the target.
- sample_submission.csv: A valid-format sample submission containing example predictions.

Target
- ship_lag_days: Integer number of days between Order Date and Ship Date.

Features
All features are provided at order time. The following columns are included:
- row_id: Unique row identifier for joining and submissions.
- Order ID: Order identifier (multiple rows can share an order).
- Order Date: Date the order was placed.
- Ship Mode: Shipping service level chosen.
- Customer ID: Unique customer identifier.
- Segment: Customer segment.
- City, State, Postal Code, Region: Customer geography.
- Product ID: Unique product identifier.
- Category, Sub-Category: Product taxonomy.
- Product Name: Product description.
- Sales, Quantity, Discount: Transactional attributes.

Notes
- Profit and Ship Date are not included to avoid leakage.
- Country is constant and omitted.
- row_id should be treated as an identifier only, not as a signal.

Evaluation
- Metric: RMSLE (root mean squared log error) between your predictions and the true ship_lag_days.
- Predictions must be non-negative real numbers. The metric is computed as sqrt(mean((log1p(pred) - log1p(true))^2)).
- Submissions must be a CSV with exactly two columns in this order: [row_id, ship_lag_days]. You may submit rows in any order; row_id must match test.csv exactly and be unique.

Train/test split
- The split is strictly time-based by Order Date to test temporal generalization.
- Train period: 2014-01-01 to 2016-12-31 (inclusive).
- Test period: 2017-01-01 to 2017-12-31 (inclusive).

Modeling guidance
- Calendar features from Order Date (e.g., year, month, day-of-week, week-of-year, holiday/weekend flags) can be informative.
- Ship Mode, geography, product taxonomy, and order-level effects interact with seasonality; consider non-linear models (e.g., gradient boosting), regularized linear models, or tree ensembles.
- For high-cardinality categorical variables (e.g., City, Product ID), target encoding with proper cross-validation or frequency encoding can help. Derive aggregates only from the training data to prevent leakage.
- Consider per-order aggregation (e.g., order-level cart size, total discount) using Order ID, computed only on training data and applied to test by left-join.

Rules
- Use only the provided features; do not use labels or future information beyond the training period to build features.
- External public resources (e.g., holiday calendars) are allowed if they do not exploit test labels.

Submission
- Create a CSV named submission.csv with two columns: row_id, ship_lag_days. The ship_lag_days values can be any non-negative real numbers.
- Sample predictions in sample_submission.csv illustrate the required format.
