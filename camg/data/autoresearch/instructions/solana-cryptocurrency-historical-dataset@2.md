# OpenMLE-fast task

Task ID: `solana-cryptocurrency-historical-dataset@2`

Native metric: `SolanaDirectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3449 bytes)
- `data/sample_submission.csv` (4666 bytes); columns: ["Id", "y"]
- `data/test.csv` (10482 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Volume"]
- `data/train.csv` (41318 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Volume", "y"]

## Public description

Competition: SOL Next‑Day Direction – Probabilistic Forecasting

Problem statement
Predict, for each day t in the test set, the probability that Solana’s closing price on day t+1 will be higher than on day t. Formally, the target y_t equals 1 if Close_{t+1} > Close_t, else 0. You must output well‑calibrated probabilities in [0,1]. This is a challenging single‑asset daily classification problem with regime shifts, noise, and non‑stationarity.

Files
- train.csv: columns [Id, Date, Open, High, Low, Close, Volume, y]. Date is ascending. y is the binary target defined above.
- test.csv: columns [Id, Date, Open, High, Low, Close, Volume]. Same schema as train without y. Date is strictly later than all dates in train.
- sample_submission.csv: columns [Id, y] containing example probabilistic predictions in [0,1] for the test Ids.

Target definition and scope
- Use only information available up to and including day t to predict whether Close_{t+1} > Close_t.
- y is provided only in train.csv. The test set’s y is hidden and evaluated on the server.

Data description
- Daily OHLCV for SOL (Solana) spanning from mid‑2020 through early‑2023.
- Columns:
  - Date: Calendar date (ascending order)
  - Open, High, Low, Close: Daily OHLC prices (USD)
  - Volume: Parsed to numeric; early history may contain missing values ("-")
- The raw “Change %” column has been excluded to avoid trivial leakage; compute any returns yourself from prices.

Important constraints and guidance
- Time‑series discipline: Do not use future information (no peeking past day t when engineering features for day t). Rolling/statistical features must be computed strictly from historical data up to day t.
- External data: To keep the leaderboard comparable and leakage‑free, use only the provided files.
- Non‑IID nature: Expect distribution shifts. Prefer robust models/regularization and time‑series‑aware validation (e.g., expanding-window CV).

Evaluation metric
- Binary Log Loss (cross‑entropy) on the predicted probabilities ŷ in [0,1].
  logloss = −(1/N) * Σ [ y*log(ŷ) + (1−y)*log(1−ŷ) ]
- Predictions are clipped for numerical stability; smaller is better. This strictly proper scoring rule rewards both accuracy and calibration.

Submission format
- A single CSV with columns [Id, y], where:
  - Id matches exactly the Ids in test.csv (order does not matter; we align by Id)
  - y is a probability in [0,1]
- Any missing, non‑finite, or out‑of‑range predictions will be rejected.

Suggested baseline features (not exhaustive)
- Returns: close‑to‑close log return, open‑to‑close return, overnight gaps
- Rolling stats: moving averages, EMAs, rolling volatility, ATR, z‑scores of returns/volume
- Range/shape: (High−Low)/Close, (Close−Open)/(High−Low), tail ratios
- Volume: level, change, rolling z‑score, price‑volume interactions
- Calendar: day‑of‑week effects

Final data split
- Chronological split. All training dates strictly precede all test dates to prevent leakage. The entire dataset is used; the final day is dropped from labeling in the raw timeline by construction (since its next-day outcome is undefined), which is standard for next‑day targets.

What to build
- A pipeline that parses the data, engineers time‑series‑safe features, trains a probabilistic classifier, and outputs calibrated probabilities for test Ids.

Good luck, and mind the regime shifts!
