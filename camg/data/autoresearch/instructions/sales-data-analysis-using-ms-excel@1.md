# OpenMLE-fast task

Task ID: `sales-data-analysis-using-ms-excel@1`

Native metric: `ProfitabilityPredictionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3258 bytes)
- `data/sample_submission.csv` (443066 bytes); columns: ["id", "is_profitable"]
- `data/test.csv` (2351320 bytes); columns: ["id", "Order Date", "Ship Mode", "Segment", "City", "State", "Country", "Region", "Market", "Category", "Sub-Category", "Order Priority", "Quantity", "Discount", "Shipping Cost"]
- `data/train.csv` (4578475 bytes); columns: ["id", "Order Date", "Ship Mode", "Segment", "City", "State", "Country", "Region", "Market", "Category", "Sub-Category", "Order Priority", "Quantity", "Discount", "Shipping Cost", "is_profitable"]

## Public description

Competition: Order-level Profitability Prediction on Global Superstore 2012–2015

Problem statement
Given information available at the time of order placement, predict the probability that an individual order line will be profitable (Profit > 0). Build a model that ranks orders by their likelihood of being profitable.

Data description
You are provided with transactional order-line data from a global retailer spanning 2012-01-01 to 2015-12-31 across multiple markets and product categories.

Files
- train.csv: Training data with features and the target column is_profitable.
- test.csv: Test data with the same feature columns as train.csv (no target).
- sample_submission.csv: Example submission format with random probabilities.

Columns
Each row corresponds to an order line. Columns included in train.csv and test.csv:
- id: Unique row identifier for joining with submissions (do not use as a feature).
- Order Date: Order placement date (you may derive calendar features from this field).
- Ship Mode: Shipping service level chosen at order time.
- Segment: Customer segment.
- City, State, Country, Region, Market: Geography information.
- Category, Sub-Category: Product taxonomy at order time.
- Order Priority: Operational priority at order time.
- Quantity: Number of units ordered.
- Discount: Discount fraction applied to the order line (0–1).
- Shipping Cost: Absolute shipping cost for the order line.

Target
- is_profitable: Binary label in train.csv only; 1 if the order line’s Profit > 0, else 0.

Split
- Chronological split: train covers 2012-01-01 to 2014-12-31; test covers 2015-01-01 to 2015-12-31.
- Class balance: About 74% of order lines are profitable, so use techniques robust to moderate imbalance.

Important constraints
- Some columns are intentionally not provided to prevent leakage and ID memorization (e.g., Profit, Sales, Ship Date, product/customer identifiers). Only use the columns listed above.
- Feature engineering is encouraged. Any aggregate/statistical encodings must be derived using training data only to avoid peeking into test.
- Time-aware features must use information available at order time. Do not use any fields that reflect post-order outcomes.

Submission format
- A CSV file with exactly the following two columns:
  - id: Must match the ids in test.csv exactly (unique, no duplicates, no missing ids).
  - is_profitable: A probability (float in [0, 1]) indicating the likelihood that the order line is profitable.

Evaluation
- Metric: ROC AUC (Area Under the Receiver Operating Characteristic Curve) computed on the test set. The metric evaluates how well your predicted probabilities rank profitable vs. unprofitable orders. It is threshold-independent and robust to moderate class imbalance.

Starter ideas
- Encode categorical variables (one-hot, target/frequency encoding fit on train only).
- Derive calendar features from Order Date (day-of-week, week-of-year, month, quarter, year).
- Explore interactions such as Discount × Quantity or Shipping Cost per unit.
- Consider robust scaling/winsorization for heavy-tailed numeric features.

Reproducibility
- The provided split and files are deterministic. Use train.csv for model development and test.csv for generating predictions.
