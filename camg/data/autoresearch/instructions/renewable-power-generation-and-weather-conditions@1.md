# OpenMLE-fast task

Task ID: `renewable-power-generation-and-weather-conditions@1`

Native metric: `SolarEnergyRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3451 bytes)
- `data/sample_submission.csv` (297352 bytes); columns: ["row_id", "Energy delta[Wh]"]
- `data/test.csv` (1767008 bytes); columns: ["row_id", "Time", "GHI", "temp", "pressure", "humidity", "wind_speed", "rain_1h", "snow_1h", "clouds_all", "isSun", "sunlightTime", "dayLength", "SunlightTime/daylength", "hour", "month"]
- `data/train.csv` (13943318 bytes); columns: ["row_id", "Time", "GHI", "temp", "pressure", "humidity", "wind_speed", "rain_1h", "snow_1h", "clouds_all", "isSun", "sunlightTime", "dayLength", "SunlightTime/daylength", "hour", "month", "Energy delta[Wh]"]

## Public description

Title: Daylight Solar Output Regression Challenge

Problem statement
- Build a model to predict PV energy generated in each 15-minute interval using concurrent weather and sun-geometry variables. The target is the continuous value Energy delta[Wh]. Only daylight intervals are scored to ensure a fair, meaningful evaluation.

Data description
- You are given a single time-series covering multiple years at 15-minute resolution.
- Columns:
  - row_id: Unique identifier for each row (integer).
  - Time: Timestamp of the interval (local time string, 15-minute cadence).
  - Energy delta[Wh]: Target. Electrical energy generated in the 15-min interval (watt-hours).
  - GHI: Global Horizontal Irradiance (W/m^2).
  - temp: Temperature (°C).
  - pressure: Surface pressure (hPa).
  - humidity: Relative humidity (%).
  - wind_speed: Wind speed (m/s).
  - rain_1h: Precipitation in the last hour (mm).
  - snow_1h: Snow in the last hour (mm).
  - clouds_all: Cloudiness (%).
  - isSun: Daylight indicator (1 if sun is up, else 0).
  - sunlightTime: Minutes of sunshine during the day so far (min).
  - dayLength: Total daylight minutes for the day (min).
  - SunlightTime/daylength: Fraction of daylight elapsed (0–1).
  - hour: Hour of day (0–23).
  - month: Month of year (1–12).

Files provided for the competition
- train.csv: Feature columns plus the target Energy delta[Wh] and row_id for all training rows.
- test.csv: Same feature columns and row_id but no target.
- sample_submission.csv: Example submission with row_id and Energy delta[Wh] columns filled with valid example predictions.

Train/test split
- Chronological split to emulate real forecasting while preventing leakage:
  - Train: 2017-01-01 00:00:00 to 2021-12-31 23:45:00
  - Test: 2022-01-01 00:00:00 up to the last available timestamp in August 2022 (15-minute cadence).
- All rows in the original series are kept; no downsampling. Timestamps are deterministic and unique per row_id.

Target and features
- Target: Energy delta[Wh] (non-negative real). Do not assume it is zero at night during modeling; only scoring excludes night.
- You may freely engineer features from the provided columns (e.g., lags/rolling statistics/interactions) as part of your solution. External data is not required.

Evaluation metric
- Submissions must be a CSV with columns: row_id, Energy delta[Wh]. Values must be finite and non-negative.
- Scoring uses Root Mean Squared Error (RMSE) computed only on daylight rows (isSun == 1) of the test set:
  - Let yi be the true Energy delta[Wh] and pi be your prediction for rows where isSun == 1 in test.csv.
  - RMSE = sqrt(mean((pi - yi)^2)).
- Predictions that are NaN/inf/negative will be rejected; ensure finite, non-negative numeric predictions.

Notes and recommendations
- Time handling: The data are in 15-minute steps. Use Time as a potential feature (e.g., encode cyclic hour-of-day, month) and consider interactions with weather.
- Data quality: Occasional missing values may exist in features; impute as needed in your pipeline. Do not impute the target.
- Modeling: Gradient-boosted trees, random forests, linear models with interactions, or temporal deep nets can perform well. Consider non-linearities with GHI, clouds_all, and seasonality.

Submission format
- Two columns, with exact names:
  - row_id
  - Energy delta[Wh]
- One row per row_id in test.csv, in any order. Duplicate or missing row_id will be rejected.

Good luck!
