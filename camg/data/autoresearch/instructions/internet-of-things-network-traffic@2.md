# OpenMLE-fast task

Task ID: `internet-of-things-network-traffic@2`

Native metric: `IoTNetworkLatencyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3666 bytes)
- `data/sample_submission.csv` (440648 bytes); columns: ["id", "target"]
- `data/test.csv` (1081464 bytes); columns: ["id", "device_id", "timestamp", "temperature", "humidity(%)", "latency(ms)", "rssi(dBm)"]
- `data/train.csv` (4452842 bytes); columns: ["id", "device_id", "timestamp", "temperature", "humidity(%)", "latency(ms)", "rssi(dBm)", "target"]

## Public description

Competition: IoT High-Latency Spike Early Warning

Problem statement
In constrained IoT networks, rare latency spikes can break SLAs and disrupt control loops. Given per-timestamp telemetry from two ESP32 devices, predict the probability that a high-latency spike will occur within the next 30 seconds. For each row (timestamp, device), the target is 1 if any observation for the same device occurs in the next 30 seconds whose latency exceeds 0.5, otherwise 0. Participants should build a model that assigns P(target=1) for each row in the test set.

Files provided
- train.csv: Labeled training rows.
- test.csv: Unlabeled test rows for which you must predict target probabilities.
- sample_submission.csv: Example submission format with random probabilities.

Columns
- id: Unique identifier of the row (use this to align your predictions).
- device_id: Categorical device identifier (two devices in this dataset).
- timestamp: Local timestamp string in the format YYYY-MM-DD HH:MM:SS.
- temperature: Degrees Celsius.
- humidity(%): Relative humidity percentage.
- latency(ms): Measured network latency.
- rssi(dBm): RSSI in dBm (more negative means weaker signal).
- target: Binary label (0/1). Present only in train.csv.

Notes
- The target is derived deterministically from the latency(ms) stream using the rule above.
- Throughput and packet loss fields are constant in the source data and are omitted here.
- The data has irregular sampling and temporal dependence; treat it as a time series. Using only current-row features is allowed, but leveraging history without peeking into the future generally improves performance.

Train/test split
- A strictly chronological split is used per device: the earlier portion is in train and the later portion is in test. No rows overlap between the two, and test timestamps are strictly after the last train timestamp within each device.
- Class imbalance is severe (positives are rare). Both classes are present in the training data.

What you should build
- Data processing to parse timestamps and handle irregular sampling.
- Feature engineering such as lags and rolling statistics over past 10/30/120 seconds for latency and rssi, temperature/humidity recent stats, time-of-day features, inter-arrival times, and device-wise trends. Ensure no leakage by using only information available up to each timestamp.
- A classifier that outputs calibrated probabilities (e.g., gradient boosting, logistic regression over time-series features, or sequence models such as LSTM/TCN).
- Proper handling of class imbalance (e.g., class weights, focal loss, threshold calibration).

Submission format
- Submit a CSV with exactly two columns: id, target
- The id column must match the ids in test.csv (one row per test row).
- The target column must contain predicted probabilities in [0, 1] for the positive class (target=1).

Evaluation metric
- Scoring uses macro-averaged Average Precision (PR-AUC) across devices:
  1) For each device_id, compute Average Precision between the ground-truth target and your predicted probabilities.
  2) The final score is the unweighted mean of these device-wise AP values. Higher is better.
- PR-AUC focuses on ranking quality under severe class imbalance and is minimally affected by true negatives; macro-averaging prevents a larger device stream from dominating the score.

Tips
- Carefully validate that your rolling/lag features never use future information relative to each prediction timestamp.
- Imbalanced-learning techniques and probability calibration often improve PR-AUC.
- Consider ensembling diverse models (e.g., tree-based + sequence models).

Good luck and happy modeling!
