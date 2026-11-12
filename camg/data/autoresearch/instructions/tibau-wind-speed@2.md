# OpenMLE-fast task

Task ID: `tibau-wind-speed@2`

Native metric: `WindExceedance24hMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3133 bytes)
- `data/sample_submission.csv` (22167 bytes); columns: ["id", "probability"]
- `data/test.csv` (1284777 bytes); columns: ["id", "ws_0", "wd_0", "ws_lag_1", "ws_lag_2", "ws_lag_3", "ws_lag_4", "ws_lag_5", "ws_lag_6", "ws_lag_7", "ws_lag_8", "ws_lag_9", "ws_lag_10", "ws_lag_11", "ws_lag_12", "ws_lag_13", "ws_lag_14", "ws_lag_15", "ws_lag_16", "ws_lag_17", "ws_lag_18", "ws_lag_19", "ws_lag_20", "ws_lag_21", "ws_lag_22", "ws_lag_23", "ws_lag_24", "wd_lag_1", "wd_lag_2", "wd_lag_3", "wd_lag_4", "wd_lag_5", "wd_lag_6", "wd_lag_7", "wd_lag_8", "wd_lag_9", "wd_lag_10", "wd_lag_11", "wd_lag_12", "wd_lag_13", "wd_lag_14", "wd_lag_15", "wd_lag_16", "wd_lag_17", "wd_lag_18", "wd_lag_19", "wd_lag_20", "wd_lag_21", "wd_lag_22", "wd_lag_23", "wd_lag_24", "ws_roll_mean_3", "ws_roll_mean_6", "ws_roll_mean_12", "ws_roll_mean_24", "ws_roll_std_3", "ws_roll_std_6", "ws_roll_std_12", "ws_roll_std_24", "hour_sin", "hour_cos", "doy_sin", "doy_cos", "wd0_sin", "wd0_cos"]
- `data/train.csv` (4425074 bytes); columns: ["id", "ws_0", "wd_0", "ws_lag_1", "ws_lag_2", "ws_lag_3", "ws_lag_4", "ws_lag_5", "ws_lag_6", "ws_lag_7", "ws_lag_8", "ws_lag_9", "ws_lag_10", "ws_lag_11", "ws_lag_12", "ws_lag_13", "ws_lag_14", "ws_lag_15", "ws_lag_16", "ws_lag_17", "ws_lag_18", "ws_lag_19", "ws_lag_20", "ws_lag_21", "ws_lag_22", "ws_lag_23", "ws_lag_24", "wd_lag_1", "wd_lag_2", "wd_lag_3", "wd_lag_4", "wd_lag_5", "wd_lag_6", "wd_lag_7", "wd_lag_8", "wd_lag_9", "wd_lag_10", "wd_lag_11", "wd_lag_12", "wd_lag_13", "wd_lag_14", "wd_lag_15", "wd_lag_16", "wd_lag_17", "wd_lag_18", "wd_lag_19", "wd_lag_20", "wd_lag_21", "wd_lag_22", "wd_lag_23", "wd_lag_24", "ws_roll_mean_3", "ws_roll_mean_6", "ws_roll_mean_12", "ws_roll_mean_24", "ws_roll_std_3", "ws_roll_std_6", "ws_roll_std_12", "ws_roll_std_24", "hour_sin", "hour_cos", "doy_sin", "doy_cos", "wd0_sin", "wd0_cos", "target"]

## Public description

Tibau Extreme-Wind Early Warning (24h exceedance)

Problem statement:
Predict, for each hourly forecast origin, the probability that wind speed will exceed 8 m/s at least once in the next 24 hours. This is a probabilistic binary classification task designed for early warning of strong-wind episodes relevant to wind turbine safety and operations.

Data description:
- You are given derived tabular datasets built from the original Tibau hourly time series (10,681 hours). Each row represents a forecast origin t with features computed using only information available up to and including time t. Labels are computed from future observations (t+1..t+24) and are never included in the test set.
- Train file (train.csv): one row per training origin with columns:
  - id: unique integer identifier
  - Features: numerical features engineered from wind speed and wind direction (see below)
  - target: 1 if max wind_speed in the next 24 hours after the origin exceeds 8 m/s, else 0
- Test file (test.csv): identical to train.csv except without the target column
- Sample submission (sample_submission.csv): expected submission format with placeholder probabilities

Feature set provided (all computed using only history up to time t):
- Current wind speed and wind direction (ws_0, wd_0)
- Lagged wind speed and direction: ws_lag_1..ws_lag_24, wd_lag_1..wd_lag_24
- Rolling statistics of wind speed: means and standard deviations over 3, 6, 12, 24 hours (ws_roll_mean_{w}, ws_roll_std_{w})
- Cyclical calendar features: hour-of-day and day-of-year encoded as sin/cos pairs (hour_sin, hour_cos, doy_sin, doy_cos)
- Directional trigonometric projections: sin/cos of current direction (wd0_sin, wd0_cos)

Train/test split:
- Chronological split with the test period strictly after the training period. Only origins with a full 24-hour future window are included. The split point is chosen deterministically to ensure both classes are present in both sets.

Submission format:
- File name: submission.csv
- Columns:
  - id: integer identifiers exactly matching test.csv
  - probability: a float in [0, 1] representing P(exceedance in next 24h)
- The submission must contain exactly the same ids as test.csv, with no duplicates or missing/extra rows.

Evaluation metric:
- Primary metric: Average Precision (area under the precision–recall curve, PR-AUC) computed over all test origins. This metric is robust and informative for imbalanced events, rewarding correct ranking of high-risk hours.

Recommendations and constraints:
- Use only the provided train/test data. External data or future information relative to each origin is not allowed.
- Typical approaches include gradient boosting on tabular features, calibrated classifiers, and sequence models trained on the provided features.
- Be mindful of class imbalance; consider appropriate evaluation on your validation split and/or calibration techniques.

Files provided:
- train.csv
- test.csv
- sample_submission.csv

Your goal:
Train your model on train.csv and produce probabilistic predictions for test.csv. Submit a CSV with columns [id, probability]. Higher PR-AUC is better.
