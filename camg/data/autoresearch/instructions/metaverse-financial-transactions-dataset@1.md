# OpenMLE-fast task

Task ID: `metaverse-financial-transactions-dataset@1`

Native metric: `MetaverseFraudDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3581 bytes)
- `data/sample_submission.csv` (413014 bytes); columns: ["transaction_id", "is_fraud"]
- `data/test.csv` (2688879 bytes); columns: ["transaction_id", "timestamp", "hour_of_day", "sending_address", "receiving_address", "amount", "location_region", "ip_prefix", "login_frequency", "session_duration", "purchase_pattern", "age_group"]
- `data/train.csv` (10885028 bytes); columns: ["transaction_id", "timestamp", "hour_of_day", "sending_address", "receiving_address", "amount", "location_region", "ip_prefix", "login_frequency", "session_duration", "purchase_pattern", "age_group", "is_fraud"]

## Public description

Metaverse Fraudulent Transaction Detection

Problem statement
Given metadata for blockchain transactions in the open metaverse, predict the probability that a transaction is fraudulent. Fraudulent transactions are those categorized as scam or phishing; all other transaction types are legitimate. Your goal is to build a model that ranks transactions by risk and outputs calibrated fraud probabilities.

Data description
Each row is a unique transaction with temporal, behavioral, network, and regional attributes.
- Training file: train.csv
  - Columns: transaction_id, timestamp, hour_of_day, sending_address, receiving_address, amount, location_region, ip_prefix, login_frequency, session_duration, purchase_pattern, age_group, is_fraud
  - Target: is_fraud ∈ {0,1}
- Test file: test.csv
  - Columns: transaction_id, timestamp, hour_of_day, sending_address, receiving_address, amount, location_region, ip_prefix, login_frequency, session_duration, purchase_pattern, age_group
  - No target column provided.
- Sample submission: sample_submission.csv
  - Columns: transaction_id, is_fraud
  - is_fraud is a predicted probability in [0,1].

Field notes
- timestamp: ISO datetime string of the transaction
- hour_of_day: integer hour (0–23)
- sending_address, receiving_address: blockchain addresses (high-cardinality categorical)
- amount: transaction amount (continuous, heavy-tailed)
- location_region: simulated geographical region
- ip_prefix: simulated IP prefix (categorical)
- login_frequency: login sessions per period (integer)
- session_duration: minutes per session (integer)
- purchase_pattern: behavioral type (e.g., focused, random, high_value)
- age_group: new, established, veteran (categorizes activity history)

Split protocol
- Temporal split: earlier transactions form the training set and later transactions form the test set. This simulates real deployment and reduces identity leakage through address memorization.
- The target was derived from internal labels and is not present as a feature in either split.

Evaluation
- Submissions are evaluated with Average Precision (area under the precision–recall curve) on the positive (fraud) class.
- Submit a CSV with exactly two columns and a header: transaction_id,is_fraud
  - Must contain a prediction for every transaction_id in test.csv, and only those IDs.
  - is_fraud must be a finite numeric probability in [0,1].

Modeling guidelines (non-binding)
- Handle class imbalance (e.g., class weights, calibrated probabilities, threshold tuning for validation).
- Time features: derive day-of-week, month, weekend/holiday flags; interact hour with region/age_group.
- Amount features: log-transform, winsorize extremes, and build aggregation stats (by sender/receiver) using training data only.
- High-cardinality addresses: use hashing, frequency/target-free encodings, or graph-context features (e.g., degrees, unique counterparties, past fraud rates computed without test leakage).
- Categorical encoding: one-hot, impact coding with proper cross-validation, or tree-based models.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Important leakage warning
- Some internal columns (e.g., transaction_type, risk_score, anomaly) exist in the raw source but are intentionally excluded from the released files to prevent target leakage. Build features using only columns present in train.csv and test.csv.

Objective
Build a robust fraud detector that generalizes across time, recognizes subtle behavioral signals, and ranks risky transactions accurately under class imbalance. Good luck!
