# OpenMLE-fast task

Task ID: `united-state-superstore-sales@1`

Native metric: `SuperstoreLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3529 bytes)
- `data/sample_submission.csv` (79922 bytes); columns: ["row_id", "loss_probability"]
- `data/test.csv` (671363 bytes); columns: ["row_id", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount"]
- `data/train.csv` (1365181 bytes); columns: ["row_id", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "loss_flag"]

## Public description

Competition title: Superstore Margin Risk — Loss-Making Line Prediction

Problem statement
Given historical order-line records from a United States superstore, predict for each order line the probability that it will be loss-making (Profit < 0) at the time the order is placed. Your task is to build a model that outputs calibrated probabilities for loss, not just class labels.

Files provided
- train.csv: Training set with features and the binary target column loss_flag.
- test.csv: Test set with the same features as train.csv (no loss_flag). Includes an identifier column row_id.
- sample_submission.csv: Example submission with columns row_id and loss_probability.

Target definition
- loss_flag = 1 if Profit < 0, else 0. The numeric Profit is not provided in the competition files; only the derived binary label is present in train.csv.

Features available (columns in train/test)
These are the columns available to build your model. All represent information available at or before order time.
- row_id: Unique identifier for each row (present in both train and test). Use this to align your predictions.
- Order ID, Order Date, Ship Mode, Customer ID, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount
Notes:
- The following columns are intentionally excluded to avoid leakage or because they are non-informative: Profit (used only to derive the target), Ship Date (not guaranteed known at order time), Row ID (surrogate key from the source), Customer Name (redundant with Customer ID).

Split and scale
- The data is split strictly by time to reflect real deployment: train consists of orders dated from 2014-01-01 through 2016-12-31; test consists of orders dated from 2017-01-01 through 2017-12-31.
- All original rows are used; no subsampling.

Submission format
- A valid submission is a CSV file with exactly two columns and header:
  - row_id: Must match the row_id values in test.csv.
  - loss_probability: A float in [0, 1] representing P(Profit < 0) for that row.
- The order of rows in your submission does not matter; we will align on row_id.

Evaluation metric
- Submissions are evaluated using binary log loss (cross-entropy):
  logloss = - (1/N) * sum_i [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]
  where y_i ∈ {0,1} is the ground truth loss_flag and p_i ∈ [0,1] is your predicted probability. Predictions will be clipped to a safe range to avoid numerical issues.

Guidance and cautions
- Time matters: ensure any historical aggregates (e.g., per Product ID mean margin, customer discount history) are computed only from training data to avoid target leakage into the test period.
- High-cardinality categoricals: IDs and names have many unique values; consider regularization, target or impact encoding with proper cross-validation, and tree-based models that handle categorical splits.
- Interactions drive risk: Losses arise from interactions among Discount, Quantity, Sales, product/category effects, region, and seasonality. Feature engineering can help.
- Calibration counts: Since the metric is log loss, focus on calibrated probabilities (e.g., isotonic/Platt scaling or cross-validation ensembling).

What to submit
- One CSV named however you like, with columns row_id and loss_probability as defined above.

Ethics and fairness
- The dataset represents transactional retail behavior in the United States; avoid sensitive inferences beyond the provided business features.

Good luck and have fun modeling!
