# OpenMLE-fast task

Task ID: `retail-insights-a-comprehensive-sales-dataset@1`

Native metric: `RetailLeadTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3873 bytes)
- `data/sample_submission.csv` (9028 bytes); columns: ["Id", "LeadTimeDays"]
- `data/test.csv` (148833 bytes); columns: ["Id", "Order Date", "City", "State", "Customer Type", "Account Manager", "Order Priority", "Product Name", "Product Category", "Product Container", "Ship Mode", "Cost Price", "Retail Price", "Profit Margin", "Order Quantity"]
- `data/train.csv` (602901 bytes); columns: ["Id", "Order Date", "City", "State", "Customer Type", "Account Manager", "Order Priority", "Product Name", "Product Category", "Product Container", "Ship Mode", "Cost Price", "Retail Price", "Profit Margin", "Order Quantity", "LeadTimeDays"]

## Public description

Retail Shipping Lead Time Prediction

Problem statement
Given an order’s attributes known at the time the order is placed, predict the shipping lead time in days, defined as the number of days between Order Date and Ship Date. Accurate lead time prediction is critical for customer satisfaction, operations planning, and inventory management.

Data overview
The dataset contains 5,000 retail order lines spanning multiple years (2013–2015) with a mix of categorical, temporal, and numeric variables. The host provides split files ready for modeling:
- train.csv: Feature matrix with the target column LeadTimeDays included.
- test.csv: Feature matrix without the target column.
- sample_submission.csv: Template submission file with the correct column names and example predictions.

Target
- LeadTimeDays: non-negative integer days between Ship Date and Order Date as computed by the organizer.

Features provided (at order time)
The feature set is curated to reflect information available when the order is placed. The following columns are included in train.csv/test.csv:
- Id: Unique row identifier.
- Order Date: Date when the order was placed.
- City, State: Customer location at city/state granularity.
- Customer Type: Customer segment (e.g., Consumer, Corporate, Small Business, etc.).
- Account Manager: Account manager associated with the order.
- Order Priority: Priority level set at order time.
- Product Name, Product Category, Product Container: Product-level descriptors and packaging.
- Ship Mode: Chosen shipping mode.
- Cost Price, Retail Price, Profit Margin: Per-unit economics, numerically cleaned by the organizer.
- Order Quantity: Quantity ordered.

Notes:
- Columns that directly or indirectly encode post-order outcomes (e.g., Ship Date itself, Sub Total, Order Total, Shipping Cost, Discount fields, and overall Total), as well as highly identifying fields (Order No, Customer Name, Address), are excluded from the released features to avoid leakage and overfitting.
- Dates are parsed with day-first format; LeadTimeDays is computed as max(0, floor((Ship Date − Order Date).days)).

Train/test split
- The split is chronological to emulate real-world forecasting: training contains earlier orders, and testing contains later orders. This encourages models that generalize across time and seasonality.

Submission format
- A CSV file with exactly two columns and a header:
  - Id: Must match the Id values provided in test.csv.
  - LeadTimeDays: Your predicted shipping lead time in days (numeric; integers or floats allowed).
- Each Id must appear exactly once. Extra/missing Ids or malformed values will be rejected.

Evaluation
- Metric: Mean Absolute Error (MAE) in days between your predictions and the ground truth LeadTimeDays.
- MAE is chosen for robustness and interpretability: it reflects the average absolute error in days, balancing occasional long delays without over-penalizing rare extremes.

Modeling guidance
- Expect heterogeneous features: categorical (many levels), temporal (seasonality, day-of-week, month), and numeric (prices, quantities). Thoughtful preprocessing and feature engineering are rewarded.
- Recommended techniques include:
  - Categorical encoders (target-agnostic), frequency/count encodings, or learned embeddings.
  - Calendar features derived from Order Date (dow, week, month, year, proximity to holidays).
  - Gradient-boosted trees, regularized linear models, and stacking/blending.
  - Rigorous cross-validation that respects time (e.g., time-based folds).
- Handle missing values and textual cleanliness (e.g., stray symbols in currency) gracefully.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Your goal
Train a model on train.csv to predict LeadTimeDays for test.csv and submit your predictions in the required format. The leaderboard is based on MAE; lower is better.
