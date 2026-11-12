# OpenMLE-fast task

Task ID: `black-friday-sales-data@1`

Native metric: `BlackFridayPurchaseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (598 bytes)
- `data/sample_submission.csv` (2728180 bytes); columns: ["Row_ID", "Purchase"]
- `data/test.csv` (5157728 bytes); columns: ["Row_ID", "User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3"]
- `data/train.csv` (23852114 bytes); columns: ["Row_ID", "User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3", "Purchase"]

## Public description

Black Friday Purchase Prediction Challenge

Files:
- train.csv: Training rows with features and target Purchase (includes Row_ID).
- test.csv: Test rows with the same features as training, without Purchase (includes Row_ID).
- sample_submission.csv: Required submission format with columns Row_ID and Purchase.

Submission format
- CSV with two columns: Row_ID, Purchase.
- Row_ID must exactly match the identifiers in test.csv (no duplicates, no missing rows).
- Purchase must be numeric and finite for every row.

Evaluation
- Root Mean Squared Error (RMSE) on Purchase over the hidden test set.
