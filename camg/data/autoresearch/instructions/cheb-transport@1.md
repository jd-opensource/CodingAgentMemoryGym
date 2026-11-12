# OpenMLE-fast task

Task ID: `cheb-transport@1`

Native metric: `ChebTransportRouteAssignmentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3098 bytes)
- `data/sample_submission.csv` (6835 bytes); columns: ["sample_id", "rnum"]
- `data/test.csv` (186031 bytes); columns: ["sample_id", "rtype", "low_floor", "w0_lat", "w0_lon", "w0_dt", "w1_lat", "w1_lon", "w1_dt", "w2_lat", "w2_lon", "w2_dt", "w3_lat", "w3_lon", "w3_dt", "w4_lat", "w4_lon", "w4_dt", "w5_lat", "w5_lon", "w5_dt", "w6_lat", "w6_lon", "w6_dt", "w7_lat", "w7_lon", "w7_dt"]
- `data/train.csv` (349683 bytes); columns: ["sample_id", "rtype", "low_floor", "w0_lat", "w0_lon", "w0_dt", "w1_lat", "w1_lon", "w1_dt", "w2_lat", "w2_lon", "w2_dt", "w3_lat", "w3_lon", "w3_dt", "w4_lat", "w4_lon", "w4_dt", "w5_lat", "w5_lon", "w5_dt", "w6_lat", "w6_lon", "w6_dt", "w7_lat", "w7_lon", "w7_dt", "rnum"]

## Public description

Cheboksary Trajectory-to-Route Assignment Challenge

Problem statement
You are given short spatio-temporal windows of consecutive GPS pings from active public transport vehicles in Cheboksary, Russia. Each window represents the most recent movement of a single vehicle within one transport day. Your task is to predict the vehicle’s route number (rnum) based solely on the provided window features, without relying on vehicle or route identifiers.

Why this matters
Transit aggregators must continuously infer which route a vehicle is serving from recent GPS pings, even when explicit labels are missing or delayed. Accurate route assignment enables reliable arrival predictions, service monitoring, and analytics.

Data description
We provide fixed-length windows (size 8) created from consecutive GPS points for the same vehicle, confined within a single transport day. For each sample we include:
- sample_id: a unique identifier for the sample (no semantics)
- w0_lat, w0_lon, w0_dt, ..., w7_lat, w7_lon, w7_dt: latitude, longitude, and time offset (in seconds from the first ping) for each point in the window
- rtype: vehicle type (e.g., bus/trolleybus; categorical string)
- low_floor: low-floor flag (0/1)
- rnum: route number (train only; target label)

Important notes
- Windows never cross transport-day boundaries.
- The provided features intentionally exclude identifiers and metadata that could trivially leak labels (e.g., api_id, gos_num, rid, dir_api).
- Time offsets are relative to the first ping in the window to avoid revealing absolute dates while keeping temporal dynamics.

Files
- train.csv: training samples with features and the target column rnum
- test.csv: test samples with identical features but without rnum
- sample_submission.csv: submission format example (sample_id, rnum)

Task
Predict rnum for each sample in test.csv.

Evaluation
Submissions are evaluated using Macro F1 across all route classes present in the test set. Macro F1 equally weights each route class, which is important because route frequency is imbalanced. A valid submission must:
- Contain exactly the rows for all sample_id values found in test.csv
- Provide one integer rnum prediction per sample_id
- Have no duplicate sample_id rows and no missing values

Modeling guidance
- Leverage sequence modeling (e.g., RNNs/Transformers) or tree-based models on engineered features.
- Useful derived features include speeds, accelerations, bearings, turn angles, total distance moved, and time-of-day encodings (sin/cos) computed from the sequence.
- Geospatial context (within-city bounds) and temporal patterns (weekday/weekend, rush hours) may improve performance.

Split policy
- Training samples come from earlier transport days; test samples come from later transport days. All test classes appear at least once in the training set to ensure learnability.

Baseline expectations
A simple baseline can be built by clustering window shapes or using gradient boosting on engineered trajectory features. Strong solutions typically combine geospatial feature engineering with sequence models.
