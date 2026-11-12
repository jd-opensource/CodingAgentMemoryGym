# OpenMLE-fast task

Task ID: `parking-transactions@2`

Native metric: `ParkCastRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2970 bytes)
- `data/sample_submission.csv` (14773 bytes); columns: ["row_id", "count"]
- `data/test.csv` (51263 bytes); columns: ["row_id", "zone_id", "channel", "hour_start", "location_group", "app_zone_group"]
- `data/train.csv` (28686000 bytes); columns: ["zone_id", "channel", "hour_start", "count", "location_group", "app_zone_group"]

## Public description

ParkCast: Forecast Zone–Hour Transaction Volume by Channel

Overview
Forecast hourly parking transaction demand across the city. For every (zone_id, channel) and each hour in a future horizon, predict the number of transactions that start in that hour. Patterns are highly seasonal (hourly/weekly) and heterogeneous across zones and between channels (Parking Meters vs Passport - app).

Files provided
- train.csv
  Columns: [zone_id, channel, hour_start, count, location_group, app_zone_group]
  • zone_id: string identifier per channel (K_<kiosk_id> for meters, A_<app_zone_id> for app)
  • channel: one of {Parking Meters, Passport - app}
  • hour_start: start of the 1-hour bin in ISO format (YYYY-MM-DD HH:00:00)
  • count: number of transactions starting in that hour
  • location_group: coarse area label (may be empty)
  • app_zone_group: app zone grouping (may be empty)

- test.csv
  Columns: [row_id, zone_id, channel, hour_start, location_group, app_zone_group]
  • Each row is a (zone_id, channel, hour_start) bin in the forecast horizon.
  • row_id is the unique key for submission and evaluation.

- sample_submission.csv
  Columns: [row_id, count]
  • Example with random but valid non-negative counts.

Task
- Predict the target count for every row in test.csv.
- All test (zone_id, channel) pairs appear at least once in the training data.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE):
  RMSLE = sqrt( mean_i( log(1 + y_pred_i) − log(1 + y_true_i) )^2 )
- Scoring details:
  • Predictions must be non-negative real numbers; negatives are clipped to 0 before scoring.
  • Any NaN/Inf values are treated as 0.
  • Each test row contributes equally to the mean.

Submission format
- CSV with columns: [row_id, count]
- The set of row_id must exactly match test.csv (order does not matter). Do not add, drop, or duplicate rows.

Modeling guidance (non-exhaustive)
- Data processing: Consider forming complete hourly time grids per (zone_id, channel) and imputing missing hours with zeros if your model requires it.
- Feature engineering:
  • Calendar: hour-of-day, day-of-week, weekend/holiday flags, month, week-of-year.
  • Lags/rolling: t-1, t-24, t-168, rolling means and recent trends at zone and group levels.
  • Spatial/metadata: location_group and app_zone_group interactions with calendar.
- Modeling: gradient-boosted trees on engineered features; regularized linear models; hierarchical or global time-series models; sequence models (e.g., LSTM/TCN) for longer temporal context.
- Validation: use a time-based split that mirrors the forecast horizon.

Notes
- hour_start timestamps are timezone-naive; treat them consistently across train and test.
- Training rows represent hours with at least one observed transaction; participants may impute zeros for missing hours if beneficial.
- The test horizon covers a fixed final window of the data (multi-week) with a regular 1-hour resolution.
