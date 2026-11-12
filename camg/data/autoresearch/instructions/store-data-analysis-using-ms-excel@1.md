# OpenMLE-fast task

Task ID: `store-data-analysis-using-ms-excel@1`

Native metric: `VrindaStoreOrderOutcomeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2616 bytes)
- `data/sample_submission.csv` (94140 bytes); columns: ["id", "Status"]
- `data/test.csv` (909060 bytes); columns: ["id", "index", "Order ID", "Cust ID", "Gender", "Age", "Age Group", "Date", "Channel", "SKU", "Category", "Size", "Qty", "currency", "Amount", "ship-city", "ship-state", "ship-postal-code", "B2B", "month_from_date", "day_of_week", "week_of_year"]
- `data/train.csv` (3884513 bytes); columns: ["id", "index", "Order ID", "Cust ID", "Gender", "Age", "Age Group", "Date", "Status", "Channel", "SKU", "Category", "Size", "Qty", "currency", "Amount", "ship-city", "ship-state", "ship-postal-code", "B2B", "month_from_date", "day_of_week", "week_of_year"]

## Public description

Task: Predict the final order outcome for Vrinda (VAStra) Store orders.

Problem statement
You are given historical, row-level order-line data from an Indian fashion retailer across multiple e-commerce channels in 2022. Your task is to predict the final fulfillment outcome (Delivered, Returned, Cancelled, or Refunded) for each order line based on the order-at-checkout attributes (customer demographics, product details, channel, and shipping information).

Files
- train.csv: Training set with features and the target column Status.
- test.csv: Test set with the same features only (without Status). Each row has a unique id.
- sample_submission.csv: Example submission file with columns id and Status.

Target
- Status: One of the four classes: Delivered, Returned, Cancelled, Refunded.

Data description
Each row corresponds to an order line. Key fields include:
- id: Row identifier. Unique within train/test.
- Order ID: Group identifier for multi-line orders.
- Cust ID: Customer identifier.
- Gender, Age, Age Group: Customer demographics.
- Date: Order date (calendar day in 2022).
- Qty, Amount, B2B: Order-line quantity, paid amount, and a B2B flag.
- Channel: E-commerce channel (Amazon, Myntra, Ajio, etc.).
- SKU, Category, Size: Product attributes.
- ship-city, ship-state, ship-postal-code: Shipping destination.
- month_from_date, day_of_week, week_of_year: Derived calendar features.
Note: Fields present in train.csv are exactly those to use; test.csv has the same fields except Status.

Evaluation
- Metric: Macro-averaged F1 across the four classes (Delivered, Returned, Cancelled, Refunded).
- The macro F1 treats all classes equally and is robust to class imbalance.
- Submissions must be a CSV with columns: id, Status. The id set must exactly match test.csv.

Rules and tips
- You may use any ML approach. Typical steps include data cleaning, feature engineering (categorical encodings, calendar features, geography bucketization), model training (e.g., gradient boosting, linear models), and validation.
- Multi-line orders appear under the same Order ID. The split ensures all lines from the same order are in the same set. You are free to use Order ID as a feature or derive aggregate features.
- Beware of high-cardinality fields (SKU, ship-city). Consider target/frequency encodings and regularization.
- Consider class imbalance strategies (class weights, focal loss, resampling). Evaluation reflects the natural distribution.

Submission format
- CSV with two columns: id, Status. Status values must be one of: Delivered, Returned, Cancelled, Refunded.

Good luck and happy modeling!
