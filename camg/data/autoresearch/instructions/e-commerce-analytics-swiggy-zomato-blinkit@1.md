# OpenMLE-fast task

Task ID: `e-commerce-analytics-swiggy-zomato-blinkit@1`

Native metric: `GroceryDeliveryTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2707 bytes)
- `data/sample_submission.csv` (588366 bytes); columns: ["row_id", "Delivery Time (Minutes)"]
- `data/test.csv` (898975 bytes); columns: ["row_id", "Platform", "Product Category", "Order Value (INR)", "Order Date & Time"]
- `data/train.csv` (3833759 bytes); columns: ["row_id", "Platform", "Product Category", "Order Value (INR)", "Order Date & Time", "Delivery Time (Minutes)"]

## Public description

Title: ETA Minutes Prediction for Instant-Grocery Orders

Problem statement
You are given historical order records from instant-grocery platforms (Blinkit, Swiggy Instamart, and JioMart). Your task is to predict Delivery Time (Minutes) at the moment an order is placed, using only information available at/near order placement.

Build a regression model that minimizes the difference between your predicted delivery time and the actual delivery time.

Files provided
- train.csv — Training data with features and the target column Delivery Time (Minutes).
- test.csv — Test data with the same feature columns as train.csv but without the target.
- sample_submission.csv — A sample submission file with the correct format.

Target
- Delivery Time (Minutes): numeric, minutes from order placement to delivery completion.

Features
The following columns are provided for both train and test:
- row_id: unique identifier for a row. Use only for joining/identification, not as a predictive feature.
- Platform: categorical (Blinkit, Swiggy Instamart, JioMart).
- Product Category: categorical (e.g., Fruits & Vegetables, Dairy, Beverages, Snacks, Personal Care, Grocery, etc.).
- Order Value (INR): numeric order amount in Indian Rupees.
- Order Date & Time: string timestamp-like value from the original logs. You may engineer useful temporal features (e.g., minute-of-hour, second-of-minute, cyclic encodings) from this field.

Note: Columns that occur post-delivery (e.g., customer feedback, service rating, refunds) are intentionally excluded to avoid target leakage. Identifiers other than row_id are removed.

Submission format
- A CSV file with exactly two columns and a header:
  - row_id
  - Delivery Time (Minutes)
- Include a row for every row_id in test.csv exactly once.

Evaluation
- Primary metric: Mean Absolute Error (MAE) in minutes between your predictions and the ground truth.
  - MAE = mean(|y_true − y_pred|)
- Lower is better.

Modeling guidance (non-exhaustive)
- Recommended preprocessing/feature engineering ideas:
  - Parse Order Date & Time into numerical time components (e.g., minute-of-hour and seconds) and consider cyclic encodings (sine/cosine).
  - One-hot or target encode Platform and Product Category.
  - Scale/standardize Order Value (INR) where appropriate.
- Suggested models: gradient boosting (e.g., LightGBM, XGBoost, CatBoost), regularized linear models, neural nets for tabular data, etc.

Integrity rules
- Use only the columns present in train.csv/test.csv for modeling.
- Do not infer labels from any file names or external resources.

Deliverables
- Submit predictions for all rows in test.csv in the specified format. The leaderboard is based on MAE.
