# OpenMLE-fast task

Task ID: `walmart-customer-purchase-behavior-dataset@1`

Native metric: `WalmartPurchaseAmountMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (578 bytes)
- `data/sample_submission.csv` (299963 bytes); columns: ["row_id", "Purchase_Amount"]
- `data/test.csv` (753945 bytes); columns: ["row_id", "Age", "Gender", "City", "Category", "Product_Name", "Purchase_Date", "Payment_Method", "Discount_Applied"]
- `data/train.csv` (3284689 bytes); columns: ["row_id", "Age", "Gender", "City", "Category", "Product_Name", "Purchase_Date", "Payment_Method", "Discount_Applied", "Purchase_Amount"]

## Public description

Title: Predicting Walmart Purchase Amounts from Checkout Context

Files in this competition (under public/):
- train.csv: Training data with features and Purchase_Amount.
- test.csv: Test data with the same features (no Purchase_Amount).
- sample_submission.csv: Example submission file with columns [row_id, Purchase_Amount].

Columns:
- row_id: Unique identifier for each transaction.
- Age, Gender, City, Category, Product_Name, Purchase_Date, Payment_Method, Discount_Applied: Features available at checkout.
- Purchase_Amount: Target value (USD) present only in train.csv.
