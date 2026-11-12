# OpenMLE-fast task

Task ID: `us-regional-sales-data@2`

Native metric: `FastShippingProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3103 bytes)
- `data/sample_submission.csv` (50679 bytes); columns: ["OrderNumber", "fast_ship"]
- `data/test.csv` (148199 bytes); columns: ["OrderNumber", "Sales Channel", "WarehouseCode", "ProcuredDate", "OrderDate", "CurrencyCode", "_SalesTeamID", "_CustomerID", "_StoreID", "_ProductID", "Order Quantity", "Discount Applied", "Unit Cost", "Unit Price"]
- `data/train.csv` (616089 bytes); columns: ["OrderNumber", "Sales Channel", "WarehouseCode", "ProcuredDate", "OrderDate", "CurrencyCode", "_SalesTeamID", "_CustomerID", "_StoreID", "_ProductID", "Order Quantity", "Discount Applied", "Unit Cost", "Unit Price", "fast_ship"]

## Public description

Competition: Fast-Shipping Probability (Ship within 7 Days)

Problem statement
Operations teams must decide at order creation whether an order will ship quickly. Your task is to predict, for each order, the probability that it will ship within 7 days of the OrderDate. This is a binary probabilistic classification problem: output well-calibrated probabilities, not hard labels.

Target definition
fast_ship = 1 if (ShipDate − OrderDate) ≤ 7 days, else 0.
Note: In the provided training data the target has already been computed and post-order fields have been removed to avoid leakage.

Files provided
- train.csv: Training rows with features available at order time and the target fast_ship.
- test.csv: Test rows with the same feature set as train.csv but without the target.
- sample_submission.csv: Sample submission showing the required format.

ID and submission format
- Use OrderNumber as the row identifier.
- Submission CSV must contain exactly two columns named: OrderNumber, fast_ship.
- fast_ship values must be valid probabilities in [0, 1].

Features available (order-time only)
Categorical/IDs:
- OrderNumber (identifier; do not use as a feature unless you engineer it safely)
- Sales Channel
- WarehouseCode
- _SalesTeamID
- _CustomerID
- _StoreID
- _ProductID
- CurrencyCode
Dates:
- ProcuredDate
- OrderDate
  (In the original raw data, dates are day-first. In train/test, dates are provided as ISO strings in the format YYYY-MM-DD.)
Numerical:
- Order Quantity
- Discount Applied
- Unit Cost
- Unit Price

What is excluded to prevent leakage
- ShipDate, DeliveryDate and any fields derived from them are not included in train/test.

Recommended feature engineering (optional)
- Calendar features from OrderDate (year, month, week-of-year, day-of-week, end-of-month/quarter flags).
- Inventory age in days: max(0, OrderDate − ProcuredDate).
- Pricing/margin: (Unit Price − Unit Cost)/Unit Cost, interactions with Discount Applied and Order Quantity.
- Encodings for high-cardinality IDs (target encoding with time-aware leakage prevention, regularized count encodings, or learned embeddings).

Evaluation
- Metric: Log Loss (binary cross-entropy) computed on fast_ship.
- Given N test rows with labels y_i ∈ {0,1} and your predictions p_i ∈ [0,1], the score is:
  LogLoss = −(1/N) * Σ [ y_i * log(p_i) + (1 − y_i) * log(1 − p_i) ]
- Lower is better. Predictions are clipped internally to avoid log(0).

Split policy and realism
- Temporal split mirrors real deployment: training consists of earlier orders; test consists of later orders. This setup introduces covariate shift and seasonality effects and requires careful validation (e.g., time-based folds) for strong solutions.

Rules and expectations
- Use only the provided train.csv and test.csv for modeling. External data (e.g., calendars) is allowed but not required.
- Ensure your submission exactly matches the required format and contains each OrderNumber in test.csv exactly once.

Deliverables for participants
- A single CSV file with columns: OrderNumber, fast_ship.
- Example: sample_submission.csv
