# OpenMLE-fast task

Task ID: `project-data-analysis-using-excel@1`

Native metric: `OrderReturnRiskMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3017 bytes)
- `data/sample_submission.csv` (79933 bytes); columns: ["Row ID", "Returned"]
- `data/test.csv` (720496 bytes); columns: ["Row ID", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Shipping cost per unit", "Estimated shipping cost for the line"]
- `data/train.csv` (1464980 bytes); columns: ["Row ID", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Shipping cost per unit", "Estimated shipping cost for the line", "Returned"]

## Public description

Project: Order Return Risk Prediction (Retail Superstore)

Problem statement
- Predict the probability that an order will be returned using information available at purchase time. Each row is an order line item; multiple rows can belong to the same order. Submit a probability for Returned for every Row ID in the test set.

Data description
- Each row contains purchase-time attributes only: order date, customer, location, product, line financials, shipping mode, and engineered shipping cost features.
- Columns provided in train/test:
  - Row ID
  - Order ID
  - Order Date
  - Ship Mode
  - Customer ID
  - Customer Name
  - Segment
  - Country
  - City
  - State
  - Postal Code
  - Region
  - Product ID
  - Category
  - Sub-Category
  - Product Name
  - Sales
  - Quantity
  - Discount
  - Shipping cost per unit (state-level)
  - Estimated shipping cost for the line (Shipping cost per unit × Quantity)
- Train includes the target column Returned (binary: 1 if the order was returned, 0 otherwise). Test excludes labels.
- Time-aware split: Train covers orders from 2014–2016; Test covers 2017. This simulates generalization to future data and prevents leakage.

Files provided
- train.csv: training data with features and Returned.
- test.csv: test data with features only.
- sample_submission.csv: example submission with Row ID and valid probabilities.

Submission format
- CSV with columns:
  - Row ID: identifier for each test line item.
  - Returned: probability in [0, 1] that the order will be returned.
- Exactly one prediction per Row ID; no extra/missing rows.

Evaluation metric
- Leaderboard metric: Area Under the Precision-Recall Curve (PR-AUC) computed at the line level on the test set.
- Rationale: Returns are relatively rare; PR-AUC emphasizes the positive class and rewards accurate ranking under imbalance.
- Submissions with invalid values (NaN/Inf/out-of-range) or non-matching Row IDs will be rejected.

Modeling guidance
- Use purchase-time information only. The following columns are excluded to prevent leakage or redundancy: Ship Date, Shipping time range, Profit, COGS, Discount value, Year sales.
- Feature engineering is encouraged:
  - Date-derived features from Order Date (e.g., month, weekday).
  - Categorical encodings for high-cardinality fields (Product ID, Customer ID, City, Product Name).
  - Order-level aggregations computed from contemporaneous line items (e.g., order total sales, item count, average discount) are allowed.
  - Class imbalance techniques (class weights, sampling, calibrated probabilities) can improve PR-AUC.

Notes
- Multiple rows can share an Order ID; all those rows share the same label during evaluation.
- The test set contains all classes observed in train.
- Do not include any file paths in your submission.

Challenge characteristics
- Medium-to-hard difficulty driven by class imbalance, high-cardinality categorical variables, and time-based generalization. Solvable with standard ML techniques and careful feature engineering.
