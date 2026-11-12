# OpenMLE-fast task

Task ID: `weather-dataset@2`

Native metric: `SnowPrecipitationAPMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2161 bytes)
- `data/sample_submission.csv` (203068 bytes); columns: ["id", "snow"]
- `data/test.csv` (1567075 bytes); columns: ["id", "Temperature (C)", "Apparent Temperature (C)", "Humidity", "Wind Speed (km/h)", "Visibility (km)", "Pressure (millibars)", "wind_bearing_sin", "wind_bearing_cos", "hour_sin", "hour_cos", "doy_sin", "doy_cos"]
- `data/train.csv` (16489286 bytes); columns: ["id", "Temperature (C)", "Apparent Temperature (C)", "Humidity", "Wind Speed (km/h)", "Visibility (km)", "Pressure (millibars)", "wind_bearing_sin", "wind_bearing_cos", "hour_sin", "hour_cos", "doy_sin", "doy_cos", "snow"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (8411 lines)
test.csv (8411 lines)
train.csv (87493 lines)```

-> sample_submission.csv has 8410 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 8409.00, 0 nan values
snow (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 8410 rows and 13 columns.
Here is some information about the columns:
Apparent Temperature (C) (float64) has range: -17.22 - 37.01, 0 nan values
Humidity (float64) has range: 0.23 - 1.00, 0 nan values
Pressure (millibars) (float64) has range: 989.59 - 1038.01, 10 nan values
Temperature (C) (float64) has range: -10.13 - 34.81, 0 nan values
Visibility (km) (float64) has range: 0.02 - 16.10, 43 nan values
Wind Speed (km/h) (float64) has range: 0.06 - 38.83, 152 nan values
doy_cos (float64) has range: -1.00 - 1.00, 0 nan values
doy_sin (float64) has range: -1.00 - 1.00, 0 nan values
hour_cos (float64) has range: -1.00 - 1.00, 0 nan values
hour_sin (float64) has range: -1.00 - 1.00, 0 nan values
id (int64) has range: 0.00 - 8409.00, 0 nan values
wind_bearing_cos (float64) has range: -1.00 - 1.00, 0 nan values
wind_bearing_sin (float64) has range: -1.00 - 1.00, 0 nan values

-> train.csv has 87492 rows and 14 columns.
Here is some information about the columns:
Apparent Temperature (C) (float64) has range: -27.72 - 39.34, 0 nan values
Humidity (float64) has range: 0.12 - 1.00, 22 nan values
Pressure (millibars) (float64) has range: 973.78 - 1046.38, 1278 nan values
Temperature (C) (float64) has range: -21.82 - 39.91, 0 nan values
Visibility (km) (float64) has range: 0.02 - 16.10, 248 nan values
Wind Speed (km/h) (float64) has range: 0.03 - 63.85, 1144 nan values
doy_cos (float64) has range: -1.00 - 1.00, 0 nan values
doy_sin (float64) has range: -1.00 - 1.00, 0 nan values
hour_cos (float64) has range: -1.00 - 1.00, 0 nan values
hour_sin (float64) has range: -1.00 - 1.00, 0 nan values
id (int64) has range: 0.00 - 87491.00, 0 nan values
snow (int64) has 2 unique values: [0, 1]
wind_bearing_cos (float64) has range: -1.00 - 1.00, 0 nan values
wind_bearing_sin (float64) has range: -1.00 - 1.00, 0 nan values
