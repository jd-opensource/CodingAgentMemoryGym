# OpenMLE-fast task

Task ID: `ecommerce-customer-churn-analysis-and-prediction@1`

Native metric: `EcommerceChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (633 bytes)
- `data/sample_submission.csv` (35625 bytes); columns: ["CustomerID", "Churn"]
- `data/test.csv` (140856 bytes); columns: ["CustomerID", "Tenure", "PreferredLoginDevice", "CityTier", "WarehouseToHome", "PreferredPaymentMode", "Gender", "HourSpendOnApp", "NumberOfDeviceRegistered", "PreferedOrderCat", "SatisfactionScore", "MaritalStatus", "NumberOfAddress", "Complain", "OrderAmountHikeFromlastYear", "CouponUsed", "OrderCount", "DaySinceLastOrder", "CashbackAmount"]
- `data/train.csv` (404933 bytes); columns: ["Tenure", "PreferredLoginDevice", "CityTier", "WarehouseToHome", "PreferredPaymentMode", "Gender", "HourSpendOnApp", "NumberOfDeviceRegistered", "PreferedOrderCat", "SatisfactionScore", "MaritalStatus", "NumberOfAddress", "Complain", "OrderAmountHikeFromlastYear", "CouponUsed", "OrderCount", "DaySinceLastOrder", "CashbackAmount", "Churn"]

## Public description

Competition: E-commerce Customer Churn Prediction (Tabular, Imbalanced)

Final files provided:
- train.csv: Training data with all features and a binary label column Churn.
- test.csv: Test data with all features and an identifier column CustomerID. The label is withheld.
- sample_submission.csv: Example submission with columns [CustomerID, Churn], where Churn is a probability in [0, 1].

Submission format:
- CSV with exactly two columns: CustomerID, Churn.
- CustomerID values must exactly match those in test.csv (one row per test customer, no duplicates, no extras).
- Churn is a probability in [0, 1] for the positive class.
