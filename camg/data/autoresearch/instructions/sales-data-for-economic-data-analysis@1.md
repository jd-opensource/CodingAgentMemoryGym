# OpenMLE-fast task

Task ID: `sales-data-for-economic-data-analysis@1`

Native metric: `SalesPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2789 bytes)
- `data/sample_submission.csv` (232078 bytes); columns: ["id", "Unit Price"]
- `data/test.csv` (873193 bytes); columns: ["id", "Date", "Year", "Month", "Customer Age", "Customer Gender", "Country", "State", "Product Category", "Sub Category", "Quantity", "Unit Cost"]
- `data/train.csv` (6056974 bytes); columns: ["id", "Date", "Year", "Month", "Customer Age", "Customer Gender", "Country", "State", "Product Category", "Sub Category", "Quantity", "Unit Cost", "Unit Price"]

## Public description

Sales Price Prediction Challenge: Transaction-Level Unit Price

Problem statement
Predict the Unit Price charged for each retail sales transaction using customer demographics, location, product category/subcategory, quantity, and temporal information. Build a robust regression model that generalizes to the most recent months.

Files provided
- train.csv: Features and the target Unit Price for historical transactions.
- test.csv: Features for future transactions; Unit Price is withheld.
- sample_submission.csv: Example submission file with the required format.

Target and features
- Target: Unit Price (positive real number) per transaction.
- Features include:
  - id: Unique identifier for each transaction (use to align predictions with test rows).
  - Date, Year, Month
  - Customer Age, Customer Gender
  - Country, State
  - Product Category, Sub Category
  - Quantity
  - Unit Cost
Notes:
- Revenue and Cost are excluded because they are deterministic functions of Unit Price, Unit Cost, and Quantity.
- Categorical columns are high-cardinality (e.g., State, Sub Category).

Split strategy
- Train set: transactions up to May 2016 (inclusive).
- Test set: transactions from June and July 2016.
This temporal split reflects real-world price prediction and prevents leakage from the future.

Submission format
- A CSV file with header and exactly two columns:
  - id: the transaction identifier (matches ids in test.csv; order is not required)
  - Unit Price: your predicted non-negative real number for the transaction’s unit price
- All test ids must be present exactly once; extra or missing ids are invalid.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Unit Price predictions.
  - RMSLE = sqrt(mean( (log(1 + y_pred) - log(1 + y_true))^2 ))
  - Properties: rewards correct proportional predictions, reduces the impact of extreme outliers, and is well-suited to prices spanning multiple orders of magnitude.
  - Requirements: predictions must be non-negative. Any negative or non-finite values will be clipped or treated as zero for scoring.

Modeling considerations
- Thorough data processing and feature engineering are critical:
  - Parse Date and derive calendar features (e.g., day-of-week, week-of-month).
  - Encode categorical variables (e.g., leave-one-out or CatBoost-style encoders) using only training data statistics.
  - Consider interaction features (e.g., State × Sub Category) and seasonality.
  - Unit Cost often correlates with Unit Price; model non-linear relationships and heteroskedasticity.
- Train a regression model and evaluate with RMSLE. Gradient boosting, regularized linear models, or deep tabular models are all reasonable starting points.

Final data files (names only)
- train.csv
- test.csv
- sample_submission.csv
