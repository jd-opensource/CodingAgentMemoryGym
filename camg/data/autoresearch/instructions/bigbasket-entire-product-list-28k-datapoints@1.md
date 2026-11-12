# OpenMLE-fast task

Task ID: `bigbasket-entire-product-list-28k-datapoints@1`

Native metric: `BigBasketProductClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (257 bytes)
- `data/sample_submission.csv` (127405 bytes); columns: ["id", "type"]
- `data/test.csv` (3011352 bytes); columns: ["id", "product", "description", "brand", "sale_price", "market_price"]
- `data/train.csv` (12424764 bytes); columns: ["product", "description", "brand", "sale_price", "market_price", "type"]

## Public description

Files in this directory:

- train.csv
- test.csv
- sample_submission.csv

Train columns: product, description, brand, sale_price, market_price, type
Test columns: id, product, description, brand, sale_price, market_price
Sample submission columns: id, type
