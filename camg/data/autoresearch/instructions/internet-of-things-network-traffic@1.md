# OpenMLE-fast task

Task ID: `internet-of-things-network-traffic@1`

Native metric: `IotLatencyForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3040 bytes)
- `data/sample_submission.csv` (531348 bytes); columns: ["row_id", "latency_60s"]
- `data/test.csv` (1255387 bytes); columns: ["row_id", "device_id", "timestamp", "temperature", "humidity(%)", "latency(ms)", "throughput(bytes/sec)", "packet_loss(%)", "rssi(dBm)"]
- `data/train.csv` (5995691 bytes); columns: ["row_id", "device_id", "timestamp", "temperature", "humidity(%)", "latency(ms)", "throughput(bytes/sec)", "packet_loss(%)", "rssi(dBm)", "latency_60s"]

## Public description

IoT 60s-ahead Latency Forecasting Challenge

Problem statement
Predict the end-to-end network latency (in milliseconds) 60 seconds into the future for IoT devices. For each row in test.csv that represents a device at time t with its telemetry, your task is to predict the latency the device will experience at time t+60s.

Data description
You are given two ESP32 clients streaming environmental and link-quality telemetry to a gateway over roughly a day. Sampling is irregular (1–3s typical), with occasional gaps and spikes.

Files provided
- train.csv: Training rows. Each row corresponds to a device and a timestamp t with features observed at t and the target latency at t+60s.
- test.csv: Test rows with features observed at time t; targets at t+60s are hidden.
- sample_submission.csv: Correct submission format with randomly generated example predictions.

Columns
- row_id: Unique identifier for each row.
- device_id: Anonymized device identifier.
- timestamp: Time of the feature snapshot (ISO 8601, local time), irregularly sampled.
- temperature: Degrees Celsius at time t.
- humidity(%): Relative humidity (%) at time t.
- rssi(dBm): Received Signal Strength Indicator (dBm) at time t.
- latency(ms): Observed latency at time t (ms), included as a feature.
- throughput(bytes/sec): Throughput at time t. In this dataset it is constant and provides no signal.
- packet_loss(%): Estimated packet loss at time t. In this dataset it is constant and provides no signal.
- latency_60s: Only in train.csv. Target latency (ms) at the first observation with timestamp ≥ t+60s for the same device.

Important notes
- Irregular sampling: The target at t+60s is defined as the latency at the first available observation whose timestamp is at or after t+60s for the same device. Rows without such a follow-up observation are not included.
- Chronological split: The split is strictly chronological per device to avoid leakage. There is no validation file; create your own validation split if desired.
- Label leakage: Device identifiers are anonymized. There are no filename or path columns in the CSVs.

Evaluation
Submissions are scored with macro-averaged Mean Absolute Error (MAE) across devices:
1) Compute MAE per device on the t+60s targets.
2) Take the simple average of the per-device MAEs. Lower is better.

Submission format
Submit a CSV file with exactly the following columns and order:
- row_id
- latency_60s

Constraints
- The set of row_id values must match exactly the row_id values in test.csv.
- Each row_id must appear exactly once.
- Predictions must be finite real numbers.

Tips
- Feature engineering with lags and rolling statistics of latency, rssi, temperature, humidity is often helpful.
- Time-of-day features (e.g., sine/cosine of hour/minute) can capture diurnal patterns.
- You can model each device separately or build a single model with device_id as a categorical feature.
- Both classical time-series (e.g., ARIMA on a resampled grid) and ML models (gradient boosting, RNN/TCN) are viable approaches.
