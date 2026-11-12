# OpenMLE-fast task

Task ID: `superstore-dataset@1`

Native metric: `SuperstoreReturnPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2749 bytes)
- `data/sample_submission.csv` (57874 bytes); columns: ["Order ID", "return_probability"]
- `data/test.csv` (391488 bytes); columns: ["Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Sales", "Quantity", "Discount", "unique_product_count", "line_item_count", "catcnt_Furniture", "catcnt_Office_Supplies", "catcnt_Technology", "subcatcnt_Accessories", "subcatcnt_Appliances", "subcatcnt_Art", "subcatcnt_Binders", "subcatcnt_Bookcases", "subcatcnt_Chairs", "subcatcnt_Copiers", "subcatcnt_Envelopes", "subcatcnt_Fasteners", "subcatcnt_Furnishings", "subcatcnt_Labels", "subcatcnt_Machines", "subcatcnt_Paper", "subcatcnt_Phones", "subcatcnt_Storage", "subcatcnt_Supplies", "subcatcnt_Tables", "order_year", "order_month", "order_dayofweek", "Region Manager"]
- `data/train.csv` (776615 bytes); columns: ["Order ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Sales", "Quantity", "Discount", "unique_product_count", "line_item_count", "catcnt_Furniture", "catcnt_Office_Supplies", "catcnt_Technology", "subcatcnt_Accessories", "subcatcnt_Appliances", "subcatcnt_Art", "subcatcnt_Binders", "subcatcnt_Bookcases", "subcatcnt_Chairs", "subcatcnt_Copiers", "subcatcnt_Envelopes", "subcatcnt_Fasteners", "subcatcnt_Furnishings", "subcatcnt_Labels", "subcatcnt_Machines", "subcatcnt_Paper", "subcatcnt_Phones", "subcatcnt_Storage", "subcatcnt_Supplies", "subcatcnt_Tables", "order_year", "order_month", "order_dayofweek", "Region Manager", "Returned"]

## Public description

Competition: Superstore Returns Prediction

Problem statement
- Predict whether a customer order will be returned using only information available at order time. For each order in the test set, participants must output the probability that the order will be returned.

Data description
- Unit of prediction: one row per Order ID.
- Training file: train.csv
  - Contains order-level features and the target column Returned (0/1).
- Test file: test.csv
  - Contains the same order-level features but without the target column.

Features (order-time only)
- Categorical: Ship Mode, Segment, Country, City, State, Postal Code, Region, Customer ID, Region Manager.
- Numerical aggregates per order: line_item_count, sales_sum, quantity_sum, discount_mean, unique_product_count.
- Category mix: counts per Category and per Sub-Category within the order.
- Time features derived from the earliest Order Date within the order: order_year, order_month, order_dayofweek.
- Notes:
  - Profit and Ship Date are excluded to prevent leakage (they are post-order outcomes or fulfillment signals).
  - Names (Customer Name, Product Name) are excluded; IDs are provided instead.

Split strategy
- Chronological split to emulate forward-looking deployment:
  - Train: all orders before 2017-01-01
  - Test: all orders from 2017-01-01 to 2017-12-31
- No Order ID appears in both sets.
- Both classes (Returned=0 and Returned=1) appear in the training set.

Submission format
- File: submission.csv
- Columns:
  - Order ID: string identifier matching test.csv
  - return_probability: predicted probability that the order is returned (float between 0 and 1)
- Each Order ID in test.csv must appear exactly once in the submission. No extra or missing IDs.

Evaluation metric
- Binary Log Loss (cross-entropy) computed on the returned label.
- Definition: mean over test orders of [-y*log(p) - (1-y)*log(1-p)], where y ∈ {0,1}, p ∈ [0,1]. Numerical stability is ensured by clipping probabilities to [1e-9, 1-1e-9].
- Why Log Loss: encourages calibrated probabilities, is robust to class imbalance, and evaluates the full distribution rather than just thresholds.

Modeling guidance
- Expected challenge drivers: class imbalance, high-cardinality categorical variables (e.g., Product/Customer/City), and temporal drift. Effective solutions will typically involve:
  - Careful preprocessing and categorical encoding
  - Feature engineering from order composition and discounts
  - Regularized linear models or gradient-boosted decision trees with calibration
  - Proper handling of class imbalance (e.g., class weights or focal loss)

Final data files
- train.csv
- test.csv

Good luck and build models that generalize across time without leaking post-order information!
