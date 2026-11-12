# OpenMLE-fast task

Task ID: `europe-bike-store-sales@1`

Native metric: `BikeStoreRevenueMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3042 bytes)
- `data/sample_submission.csv` (1311346 bytes); columns: ["row_id", "Revenue"]
- `data/test.csv` (6945464 bytes); columns: ["row_id", "Date", "Day", "Month", "Year", "Customer_Age", "Age_Group", "Customer_Gender", "Country", "State", "Product_Category", "Sub_Category", "Product", "Order_Quantity", "Unit_Cost", "Unit_Price"]
- `data/train.csv` (7860141 bytes); columns: ["row_id", "Date", "Day", "Month", "Year", "Customer_Age", "Age_Group", "Customer_Gender", "Country", "State", "Product_Category", "Sub_Category", "Product", "Order_Quantity", "Unit_Cost", "Unit_Price", "Revenue"]

## Public description

Competition: Realized Revenue Prediction for Multi-Country Bike Store Orders

Problem statement:
Predict the realized Revenue for each order line using transactional attributes at the time of sale. Revenue deviates from simple price × quantity due to discounts, promotions, seasonality, and regional strategies. Model these effects across time, geography, product hierarchy, and customer demographics.

Files provided:
- train.csv: Training data containing features and the target column Revenue.
- test.csv: Test data with the same feature columns; no labels provided.
- sample_submission.csv: Example submission file in the required format.

Input feature columns (present in both train.csv and test.csv):
- row_id: Unique identifier per row.
- Date, Day, Month, Year: Transaction date fields (Day is day-of-month; Month is string).
- Customer_Age, Age_Group, Customer_Gender: Customer demographics.
- Country, State: Geography.
- Product_Category, Sub_Category, Product: Product hierarchy.
- Order_Quantity: Units purchased.
- Unit_Cost, Unit_Price: Cost and list price per unit.

Target label (train.csv only):
- Revenue: Realized revenue of the order line.

Leakage control:
- The columns Profit and Cost are intentionally excluded from train.csv and test.csv. Do not attempt to derive Revenue via Profit or Cost.

Train/Test split design:
- Train contains earlier years and test contains later years to assess temporal generalization and avoid duplicate leakage across years (e.g., train ≤ 2014, test ≥ 2015).

Modeling guidance:
- Parse Date as datetime and consider time-derived features such as day-of-week, week-of-year, quarter, and season.
- Handle high-cardinality categorical variables (Country, State, Product hierarchy) with robust encodings (e.g., frequency encoding, regularized one-hot, or other target-agnostic encodings).
- Engineer interactions (e.g., Unit_Price × Order_Quantity, Unit_Price − Unit_Cost, Unit_Price / Unit_Cost) without using Profit or Cost.
- Consider heteroscedasticity due to varying quantities; gradient-boosted trees, regularized linear models, and tabular neural networks are viable.

Evaluation:
- Metric: Root Mean Squared Error (RMSE) on Revenue.
- Submission format: A CSV with columns [row_id, Revenue], one prediction per row_id appearing in test.csv.
- RMSE is computed as sqrt(mean((prediction − ground_truth)^2)) after aligning row_id between the submission and the hidden test labels. It penalizes larger errors appropriately and measures error in business units.

Submission notes:
- Submit a single CSV (name arbitrary) that matches the sample_submission.csv format: two columns [row_id, Revenue] and one row per test example.
- Ensure numerical stability in predictions (avoid NaN/Inf).

Scope and expectations:
- Use the entire dataset; runtime constraints are not enforced here.
- No external data is required; focus on extracting patterns from the provided fields.
- Advanced feature engineering and robust encoding strategies are encouraged for competitive performance.
