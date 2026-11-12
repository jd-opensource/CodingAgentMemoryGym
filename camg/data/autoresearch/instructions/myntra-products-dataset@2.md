# OpenMLE-fast task

Task ID: `myntra-products-dataset@2`

Native metric: `MyntraPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (393 bytes)
- `data/sample_submission.csv` (388276 bytes); columns: ["id", "price"]
- `data/test.csv` (1161102 bytes); columns: ["id", "name", "seller", "mrp", "rating", "ratingTotal", "img_count", "category"]
- `data/train.csv` (5053313 bytes); columns: ["id", "name", "seller", "mrp", "rating", "ratingTotal", "img_count", "category", "price"]

## Public description

Myntra Price Prediction Challenge

Files in this folder
- train.csv: Training data with features and target price.
- test.csv: Test data with features only.
- sample_submission.csv: Example submission file (id,price).

Target
- price: Selling price of the product (numeric, INR).

Submission format
- CSV with two columns: id, price.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE).
