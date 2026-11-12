# OpenMLE-fast task

Task ID: `wa-fnusec-telcocustomerchurn@1`

Native metric: `TelcoCustomerChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3590 bytes)
- `data/sample_submission.csv` (31712 bytes); columns: ["customerID", "Churn"]
- `data/test.csv` (284750 bytes); columns: ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"]
- `data/train.csv` (680482 bytes); columns: ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (2114 lines)
test.csv (2114 lines)
train.csv (4931 lines)```

-> sample_submission.csv has 2113 rows and 2 columns.
Here is some information about the columns:
Churn (float64) has 1 unique values: [0.5]
customerID (object) has 2113 unique values. Some example values: ['3678-MNGZX', '9170-ARBTB', '1212-GLHMD', '3999-WRNGR']

-> test.csv has 2113 rows and 20 columns.
Here is some information about the columns:
Contract (object) has 3 unique values: ['One year', 'Month-to-month', 'Two year']
Dependents (object) has 2 unique values: ['Yes', 'No']
DeviceProtection (object) has 3 unique values: ['No internet service', 'Yes', 'No']
InternetService (object) has 3 unique values: ['No', 'Fiber optic', 'DSL']
MonthlyCharges (float64) has range: 18.40 - 118.60, 0 nan values
MultipleLines (object) has 3 unique values: ['Yes', 'No', 'No phone service']
OnlineBackup (object) has 3 unique values: ['No internet service', 'No', 'Yes']
OnlineSecurity (object) has 3 unique values: ['No internet service', 'No', 'Yes']
PaperlessBilling (object) has 2 unique values: ['Yes', 'No']
Partner (object) has 2 unique values: ['Yes', 'No']
PaymentMethod (object) has 4 unique values: ['Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check']
PhoneService (object) has 2 unique values: ['Yes', 'No']
SeniorCitizen (int64) has 2 unique values: [0, 1]
StreamingMovies (object) has 3 unique values: ['No internet service', 'Yes', 'No']
StreamingTV (object) has 3 unique values: ['No internet service', 'Yes', 'No']
TechSupport (object) has 3 unique values: ['No internet service', 'No', 'Yes']
TotalCharges (float64) has range: 18.80 - 8564.75, 2 nan values
customerID (object) has 2113 unique values. Some example values: ['3678-MNGZX', '9170-ARBTB', '1212-GLHMD', '3999-WRNGR']
gender (object) has 2 unique values: ['Female', 'Male']
tenure (int64) has range: 0.00 - 72.00, 0 nan values

-> train.csv has 4930 rows and 21 columns.
Here is some information about the columns:
Churn (object) has 2 unique values: ['No', 'Yes']
Contract (object) has 3 unique values: ['Month-to-month', 'One year', 'Two year']
Dependents (object) has 2 unique values: ['No', 'Yes']
DeviceProtection (object) has 3 unique values: ['No internet service', 'Yes', 'No']
InternetService (object) has 3 unique values: ['No', 'Fiber optic', 'DSL']
MonthlyCharges (float64) has range: 18.25 - 118.75, 0 nan values
MultipleLines (object) has 3 unique values: ['No', 'Yes', 'No phone service']
OnlineBackup (object) has 3 unique values: ['No internet service', 'No', 'Yes']
OnlineSecurity (object) has 3 unique values: ['No internet service', 'Yes', 'No']
PaperlessBilling (object) has 2 unique values: ['No', 'Yes']
Partner (object) has 2 unique values: ['No', 'Yes']
PaymentMethod (object) has 4 unique values: ['Mailed check', 'Credit card (automatic)', 'Electronic check', 'Bank transfer (automatic)']
PhoneService (object) has 2 unique values: ['Yes', 'No']
SeniorCitizen (int64) has 2 unique values: [0, 1]
StreamingMovies (object) has 3 unique values: ['No internet service', 'No', 'Yes']
StreamingTV (object) has 3 unique values: ['No internet service', 'No', 'Yes']
TechSupport (object) has 3 unique values: ['No internet service', 'No', 'Yes']
TotalCharges (float64) has range: 18.85 - 8684.80, 9 nan values
customerID (object) has 4930 unique values. Some example values: ['5522-JBWMO', '5222-JCXZT', '5570-PTWEH', '2230-XTUWL']
gender (object) has 2 unique values: ['Male', 'Female']
tenure (int64) has range: 0.00 - 72.00, 0 nan values
