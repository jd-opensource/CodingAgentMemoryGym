# OpenMLE-fast task

Task ID: `customer360insights@2`

Native metric: `Customer360InsightsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (667 bytes)
- `data/sample_submission.csv` (12496 bytes); columns: ["order_id", "OrderReturn"]
- `data/test.csv` (65294 bytes); columns: ["order_id", "Gender", "Age", "CreditScore", "MonthlyIncome", "Country", "State", "City", "Category", "Product", "Cost", "Price", "Quantity", "CampaignSchema", "SessionStart", "CartAdditionTime", "OrderConfirmationTime", "SessionEnd", "PaymentMethod"]
- `data/train.csv` (264271 bytes); columns: ["order_id", "Gender", "Age", "CreditScore", "MonthlyIncome", "Country", "State", "City", "Category", "Product", "Cost", "Price", "Quantity", "CampaignSchema", "SessionStart", "CartAdditionTime", "OrderConfirmationTime", "SessionEnd", "PaymentMethod", "OrderReturn"]

## Public description

Post-Purchase Return Risk Prediction

Files in this directory:
- train.csv: Labeled confirmed orders with features and target OrderReturn.
- test.csv: Unlabeled confirmed orders with the same feature schema as train.csv (without OrderReturn).
- sample_submission.csv: Example submission with random probabilities.

Target
- OrderReturn ∈ {0,1}; submit probabilities for each order_id in test.csv.

Submission format
- CSV with columns: order_id, OrderReturn (probability in [0,1]).

Evaluation
- Binary Log Loss (lower is better). Probabilities are clipped to [1e-15, 1-1e-15].

Split
- Deterministic temporal split by the 80th percentile of OrderConfirmationTime.
