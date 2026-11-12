# OpenMLE-fast task

Task ID: `telco-customer-churn-analysis-dashboard@2`

Native metric: `TelcoChurnReasonMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (442 bytes)
- `data/sample_submission.csv` (16937 bytes); columns: ["CustomerID", "Churn Reason"]
- `data/test.csv` (113935 bytes); columns: ["CustomerID", "Count", "Country", "State", "City", "Zip Code", "Lat Long", "Latitude", "Longitude", "Gender", "Senior Citizen", "Partner", "Dependents", "Tenure Months", "Phone Service", "Multiple Lines", "Internet Service", "Online Security", "Online Backup", "Device Protection", "Tech Support", "Streaming TV", "Streaming Movies", "Contract", "Paperless Billing", "Payment Method", "Monthly Charges", "Total Charges", "Total services used", "Senior citizen (Binary)", "Tenure group", "Average monthly spend"]
- `data/train.csv` (376815 bytes); columns: ["CustomerID", "Count", "Country", "State", "City", "Zip Code", "Lat Long", "Latitude", "Longitude", "Gender", "Senior Citizen", "Partner", "Dependents", "Tenure Months", "Phone Service", "Multiple Lines", "Internet Service", "Online Security", "Online Backup", "Device Protection", "Tech Support", "Streaming TV", "Streaming Movies", "Contract", "Paperless Billing", "Payment Method", "Monthly Charges", "Total Charges", "Churn Reason", "Total services used", "Senior citizen (Binary)", "Tenure group", "Average monthly spend"]

## Public description

Competition: Churn Reason Classification for Churned Telco Customers

Files provided (relative to public/):
- train.csv: Tabular data with features and the target column (Churn Reason).
- test.csv: Tabular data with features only (no target).
- sample_submission.csv: Example submission file with required format.

Target:
- Column: Churn Reason.

Submission format:
- CSV with columns [CustomerID, Churn Reason], one row per test.csv entry.
