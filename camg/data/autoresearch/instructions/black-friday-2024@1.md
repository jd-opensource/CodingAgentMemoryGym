# OpenMLE-fast task

Task ID: `black-friday-2024@1`

Native metric: `BlackFridayPurchaseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (597 bytes)
- `data/sample_submission.csv` (9151 bytes); columns: ["Row_ID", "Purchase"]
- `data/test.csv` (24010 bytes); columns: ["User_ID", "Lat", "Long", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3", "Row_ID"]
- `data/train.csv` (103025 bytes); columns: ["User_ID", "Lat", "Long", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3", "Purchase", "Row_ID"]

## Public description

Black Friday 2024: Personalized Purchase Amount Prediction

Files
- train.csv: Labeled training data.
- test.csv: Unlabeled test data (same columns as train.csv except Purchase is withheld).
- sample_submission.csv: Example submission file with the required format.

Target
- Purchase: The amount spent for the interaction (positive numeric).

Submission format
- A single CSV with exactly two columns and a header:
  - Row_ID: Must match the identifiers provided in test.csv (unique and complete).
  - Purchase: Your predicted purchase amount for the corresponding Row_ID (non-negative numeric).
