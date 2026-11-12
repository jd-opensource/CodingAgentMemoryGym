# OpenMLE-fast task

Task ID: `diwali-sales-dataset@1`

Native metric: `DiwaliSpendRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (339 bytes)
- `data/sample_submission.csv` (52394 bytes); columns: ["row_id", "Amount"]
- `data/test.csv` (182521 bytes); columns: ["row_id", "User_ID", "Product_ID", "Gender", "Age Group", "Age", "Marital_Status", "State", "Zone", "Occupation", "Product_Category", "Orders"]
- `data/train.csv` (795460 bytes); columns: ["row_id", "User_ID", "Product_ID", "Gender", "Age Group", "Age", "Marital_Status", "State", "Zone", "Occupation", "Product_Category", "Orders", "Amount"]

## Public description

Diwali Basket Spend Prediction

Files in this directory (relative paths):
- train.csv
- test.csv
- sample_submission.csv

Target
- Amount: total spend for the transaction (continuous, non-negative).

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE).
- Submission format: CSV with two columns and a header:
  row_id, Amount
