# OpenMLE-fast task

Task ID: `noaa-weather-data-jfk-airport@1`

Native metric: `JFKVisibilityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2885 bytes)
- `data/sample_submission.csv` (189399 bytes); columns: ["row_id", "target_visibility_next_hour"]
- `data/test.csv` (1458160 bytes); columns: ["row_id", "STATION", "STATION_NAME", "ELEVATION", "LATITUDE", "LONGITUDE", "DATE", "HOURLYSKYCONDITIONS", "HOURLYPRSENTWEATHERTYPE", "REPORTTPYE", "HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYDewPointTempF", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYWindGustSpeed", "HOURLYStationPressure", "HOURLYSeaLevelPressure", "HOURLYPrecip", "HOURLYAltimeterSetting", "HOURLYVISIBILITY_num", "hour_of_day", "day_of_year"]
- `data/train.csv` (8192665 bytes); columns: ["STATION", "STATION_NAME", "ELEVATION", "LATITUDE", "LONGITUDE", "DATE", "HOURLYSKYCONDITIONS", "HOURLYPRSENTWEATHERTYPE", "REPORTTPYE", "HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYDewPointTempF", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYWindGustSpeed", "HOURLYStationPressure", "HOURLYSeaLevelPressure", "HOURLYPrecip", "HOURLYAltimeterSetting", "HOURLYVISIBILITY_num", "hour_of_day", "day_of_year", "target_visibility_next_hour"]

## Public description

JFK Next-Hour Visibility Forecasting Challenge

Problem statement
Airports depend on accurate short-term visibility forecasts to manage runway operations, sequencing, diversions, and safety. Your task is to predict the next-hour surface visibility (in miles) at JFK Airport given the current hour’s meteorological observations.

Data overview
You will work with an hourly time series from a single station spanning 2010–2018. The tabular records include:
- Timestamp and station metadata
- Meteorological measurements: dry/wet bulb temperature, dew point, relative humidity, wind speed/direction/gusts, station and sea-level pressure, precipitation, altimeter setting
- Categorical codes: sky conditions and present weather phenomena

Files provided
- train.csv: Hourly features and the target column target_visibility_next_hour.
- test.csv: Same feature schema as train.csv but without the target, plus a row_id column.
- sample_submission.csv: A valid submission template with columns [row_id, target_visibility_next_hour].

Target definition
- target_visibility_next_hour is the surface visibility (miles) observed during the next hour relative to the feature timestamp of the row.

Split policy
- Chronological split by target time. Training rows have next-hour timestamps before 2017-01-01; test rows have next-hour timestamps on/after 2017-01-01. This ensures forward-in-time evaluation.

Evaluation metric
- Root Mean Squared Error (RMSE) in miles between your predictions and the actual next-hour visibility over all rows in the test set.
- RMSE = sqrt(mean((y_pred − y_true)^2)). Lower is better.

Submission format
- A CSV file containing exactly two columns in this order:
  1) row_id: The identifier found in test.csv.
  2) target_visibility_next_hour: Your predicted visibility in miles for the next hour.
- No extra columns are allowed. All row_id values must be present exactly once.

Guidance and considerations
- Temporal features: Derive hour-of-day/day-of-year cyclic encodings, short-term lags, and rolling statistics (e.g., humidity, pressure tendency, wind changes).
- Meteorology: Coerce numeric fields carefully; handle tokens such as trace precipitation (T) and sentinel values (e.g., -9999). Avoid fabricating labels.
- Text parsing: Sky conditions and weather phenomena codes can be parsed into useful categorical indicators and cloud-base features.
- Robustness: Low-visibility events are rare but important. Strong models balance overall accuracy and performance on extremes.
- Leakage avoidance: Daily/monthly aggregates are excluded from the provided feature schema to prevent inadvertent target leakage.

You may use any machine learning approach. Effective solutions typically combine careful data processing and feature engineering with robust regression models (e.g., gradient boosting, linear models with engineered features, sequence models).
