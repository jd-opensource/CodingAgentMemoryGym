# OpenMLE-fast task

Task ID: `cryptocurrency-transaction-analytics-btc-and-eth@1`

Native metric: `CryptoFeeRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3556 bytes)
- `data/sample_submission.csv` (360448 bytes); columns: ["Transaction_ID", "Transaction_Fee"]
- `data/test.csv` (2021987 bytes); columns: ["Transaction_ID", "Sender_Address", "Receiver_Address", "Amount", "Timestamp", "Block_ID", "Mining_Pool", "Currency", "Transaction_Type", "Transaction_Status", "Gas_Price_Gwei"]
- `data/train.csv` (8514835 bytes); columns: ["Transaction_ID", "Sender_Address", "Receiver_Address", "Amount", "Timestamp", "Block_ID", "Mining_Pool", "Currency", "Transaction_Type", "Transaction_Status", "Gas_Price_Gwei", "Transaction_Fee"]

## Public description

Title: Universal Crypto Transaction Fee Prediction (BTC + ETH)

Problem statement:
Predict the Transaction_Fee for individual blockchain transactions across Bitcoin (BTC) and Ethereum (ETH). Your model should learn cross-chain fee dynamics driven by network conditions, mining pools, addresses, and temporal patterns.

Data description:
Final files provided:
- train.csv: Features plus the target column Transaction_Fee.
- test.csv: Same features but without Transaction_Fee.

Columns:
- Transaction_ID: Unique identifier for the transaction.
- Sender_Address: Sender blockchain address.
- Receiver_Address: Receiver blockchain address.
- Amount: Amount transferred (BTC or ETH depending on Currency).
- Timestamp: ISO 8601 datetime when the transaction was processed.
- Block_ID: Identifier of the block that included the transaction.
- Mining_Pool: Name of the mining pool confirming the transaction.
- Currency: Cryptocurrency type (BTC or ETH).
- Transaction_Type: Type of transaction (primarily “Transfer”).
- Transaction_Status: Status of the transaction (primarily “Confirmed”).
- Gas_Price_Gwei: Gas price in Gwei (applicable to ETH; missing for BTC).
- Transaction_Fee: Target variable (present only in train.csv; held-out in test.csv).

Train/test split:
A chronological split simulates realistic drift: training contains earlier timestamps and testing contains later timestamps. This encourages generalization across time and networks. Perform your own validation using time-based splits or folds on the training set.

Recommended processing and feature engineering:
- Parse Timestamp and derive time features: year, month, day, day-of-week, hour; consider cyclical encodings (sin/cos) for hour or day-of-week.
- Model Currency differences explicitly (ETH vs BTC), including interactions.
- Encode Mining_Pool via robust categorical strategies (one-hot, target/mean encoding, or regularized approaches).
- Address features (to leverage signal without exploding cardinality): address format/type (ETH 0x vs BTC legacy/bech32), string length, hex character ratio, checksum case pattern (for ETH), short prefix buckets, equality flag (sender == receiver), and simple similarity metrics (e.g., common prefix length).
- Gas_Price_Gwei handling: numeric for ETH; treat as missing for BTC with a missing-indicator feature; consider Currency × Gas_Price_Gwei and Pool × Gas_Price_Gwei interactions.
- Amount stabilization: use log(Amount + 1); consider interactions with Currency and Mining_Pool.
- Derive compact Block_ID features (length, hex share, case ratio, short prefix) instead of using high-cardinality IDs directly.

Submission format:
Submit a CSV file with exactly these columns, in the same row order as test.csv:
- Transaction_ID
- Transaction_Fee
Predicted Transaction_Fee values must be non-negative real numbers.

Evaluation metric:
Root Mean Squared Logarithmic Error (RMSLE) on Transaction_Fee.
- Definition: RMSLE(y_true, y_pred) = sqrt(mean((log1p(y_pred_clipped) − log1p(y_true_clipped))²)))
- y_pred_clipped and y_true_clipped are clipped at 0 to avoid invalid logs.
- Rationale: Transaction fees vary multiplicatively and can be heavy-tailed. RMSLE fairly penalizes proportional errors and is robust to outliers across BTC and ETH.

Notes:
- Robust preprocessing is essential: handle missing values (e.g., Gas_Price_Gwei for BTC), numeric coercions, and datetime parsing.
- Avoid label leakage: compute any statistics solely on training data.
- A sample_submission.csv is provided to illustrate the required format.
