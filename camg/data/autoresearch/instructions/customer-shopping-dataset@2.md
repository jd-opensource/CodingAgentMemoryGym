# OpenMLE-fast task

Task ID: `customer-shopping-dataset@2`

Native metric: `CustomerPaymentMethodMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (558 bytes)
- `data/sample_submission.csv` (1272558 bytes); columns: ["row_id", "Cash", "Credit Card", "Debit Card"]
- `data/test.csv` (1106973 bytes); columns: ["row_id", "gender", "age", "category", "quantity", "price", "invoice_date", "shopping_mall"]
- `data/train.csv` (4689933 bytes); columns: ["gender", "age", "category", "quantity", "price", "shopping_mall", "invoice_date", "payment_method"]

## Public description

Title: Predict Customer Payment Method from Transaction Context

Data description:
- Training data (train.csv): Contains transaction features and the target column payment_method.
- Test data (test.csv): Contains transaction features and a unique row_id column identifying each test row.
- Features: gender, age, category, quantity, price, invoice_date, shopping_mall.

Submission format:
- CSV with columns: row_id, Cash, Credit Card, Debit Card.
- Values should be non-negative probabilities per row.

Files:
- train.csv
- test.csv
- sample_submission.csv
