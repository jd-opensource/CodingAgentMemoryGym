# OpenMLE-fast task

Task ID: `seoul-bike-sharing@1`

Native metric: `SeoulBikeSharingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3537 bytes)
- `data/sample_submission.csv` (12026 bytes); columns: ["Rented Bike Count"]
- `data/test.csv` (46150 bytes); columns: ["Date", "Hour", "Temperature(°C)", "Humidity(%)", "Wind speed (m/s)", "Visibility (10m)", "Dew point temperature(°C)", "Solar Radiation (MJ/m2)", "Rainfall(mm)", "Snowfall (cm)", "Seasons", "Holiday", "Functioning Day"]
- `data/train.csv` (594367 bytes); columns: ["Date", "Hour", "Temperature(°C)", "Humidity(%)", "Wind speed (m/s)", "Visibility (10m)", "Dew point temperature(°C)", "Solar Radiation (MJ/m2)", "Rainfall(mm)", "Snowfall (cm)", "Seasons", "Holiday", "Functioning Day", "Rented Bike Count"]

## Public description

Seoul Bike Sharing Demand Prediction

Problem statement
You are tasked with forecasting hourly bike rental demand for Seoul’s public bike-sharing system. Using calendar information and contemporaneous weather observations, predict the number of bikes rented in each hour for a held-out, time-ordered evaluation period. Accurate demand forecasts help rebalance bikes, schedule maintenance, and optimize staffing.

Data description
Each row represents a single hour. The training data include the target column; the test data contain only features. All rows are chronologically ordered.
- Date: Calendar date (day/month/year).
- Hour: Hour of day [0–23].
- Temperature(°C): Ambient temperature in degrees Celsius.
- Humidity(%): Relative humidity in percent.
- Wind speed (m/s): Wind speed in meters per second.
- Visibility (10m): Visibility in units of 10 meters.
- Dew point temperature(°C): Dew point in degrees Celsius.
- Solar Radiation (MJ/m2): Solar radiation.
- Rainfall(mm): Rainfall in millimeters.
- Snowfall (cm): Snowfall in centimeters.
- Seasons: Categorical season label.
- Holiday: Categorical holiday indicator (e.g., “No Holiday”, specific holidays).
- Functioning Day: Operational flag (“Yes”/“No”).
- Rented Bike Count: Target variable, the number of bikes rented in the hour (non-negative integer). Present only in train; withheld in test.

Files provided
- train.csv: Feature columns plus the target column Rented Bike Count for all training hours.
- test.csv: The same feature columns as train.csv, in the same order, but without Rented Bike Count.
- sample_submission.csv: A sample prediction file with the correct format and number of rows.

Your task
- Build a model that maps exogenous features (weather + calendar) to hourly demand.
- Respect temporal order. The test set is the final contiguous block of hours (a 28-day horizon) held out chronologically to assess generalization across season and weather regimes.
- You may engineer additional features (e.g., day-of-week, month, is-weekend, day-of-year) derived solely from the provided Date/Hour information. Do not use any target-dependent or future information.

Submission format
- Submit a single-column CSV with header exactly: Rented Bike Count.
- The file must contain one prediction per row in the exact same order as rows in test.csv.
- Values should be non-negative real numbers. Integers are acceptable; decimals are allowed.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) between the submitted predictions and the ground truth for the test period.
- Definition: RMSLE = sqrt(mean((log1p(pred) − log1p(actual))^2)).
- Why RMSLE: Demand is non-negative and varies widely across hours and seasons. RMSLE emphasizes relative accuracy, handles zeros through log1p, reduces the influence of extreme peaks, and yields a stable, fair leaderboard.

Notes and recommendations
- Parse Date carefully (day-first format) and combine with Hour to construct a proper timestamp if needed.
- All provided columns are potentially useful. Participants commonly normalize continuous variables and one-hot encode categorical variables (Seasons, Holiday, Functioning Day). Consider non-linear models (e.g., gradient boosting) and time-aware features to capture strong daily/weekly/seasonal patterns and weather interactions.
- There can be zero or near-zero demand during late-night hours; ensure your model is robust and that predictions are non-negative.

Good luck and have fun building robust, time-aware demand forecasters!
