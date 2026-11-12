# OpenMLE-fast task

Task ID: `delhi-air-quality@2`

Native metric: `DelhiAirQualityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1984 bytes)
- `data/sample_submission.csv` (44571 bytes); columns: ["id", "pred"]
- `data/test.csv` (140879 bytes); columns: ["id", "date", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
- `data/train.csv` (1288245 bytes); columns: ["id", "date", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3", "label"]

## Public description

Competition: Delhi PM2.5 Exceedance Prediction (24-hour ahead)

Background
Delhi experiences frequent hazardous air quality episodes driven by particulate matter (PM2.5). Reliable 24-hour-ahead exceedance predictions enable public health advisories and mitigation actions.

Problem statement
Given the city-level hourly pollutant readings at time t, predict the probability that PM2.5 will exceed a hazardous threshold 24 hours later (at t+24h). The target label y(t) = 1 if pm2_5 at t+24 ≥ 250 µg/m³, else 0. Participants must submit p(y=1) for each provided test timestamp.

Public data files (relative to public/)
- train.csv: id, date, co, no, no2, o3, so2, pm2_5, pm10, nh3, label
- test.csv: id, date, co, no, no2, o3, so2, pm2_5, pm10, nh3  (No label)
- sample_submission.csv: id, pred  (Predicted probability p(y=1) in [0,1] for each test id)

Evaluation metric
- Primary metric: Average Precision (PR-AUC) for the positive class (exceedance) computed over the test set. This threshold-free metric emphasizes ranking quality under class imbalance and is robust to rare-event prediction.
- Submission format: a CSV with two columns [id, pred], where id matches test.csv and pred is a numeric probability in [0,1].

Modeling guidance
- Recommended feature engineering: calendar features (hour-of-day, day-of-week, month) and lag/rolling statistics of pollutants using only past values up to time t. Handle gaps carefully to avoid windows that cross missing periods.
- Suggested models: calibrated gradient boosting, logistic regression with engineered lags, random forests, temporal CNN/RNN classifiers.
- No external data is required; focus on robust preprocessing (e.g., median/IQR scaling) to address heavy tails and seasonality.

Rules and integrity
- Time-based split prevents leakage: training precedes test. Do not use any information at or after t when predicting for t.
- The organizers ensured that every test label class occurs in the training set at least once.
