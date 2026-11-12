# OpenMLE-fast task

Task ID: `cairo-whether@1`

Native metric: `CairoWeatherSunshineMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4758 bytes)
- `data/sample_submission.csv` (1475 bytes); columns: ["id", "sunshine_duration (s)"]
- `data/test.csv` (18162 bytes); columns: ["id", "time", "temperature_2m_mean (°C)", "rain_sum (mm)", "wind_speed_10m_max (km/h)", "apparent_temperature_mean (°C)", "temperature_2m_min (°C)", "temperature_2m_max (°C)", "apparent_temperature_max (°C)", "weather_code (wmo code)", "wind_direction_10m_dominant (°)", "wind_gusts_10m_max (km/h)", "shortwave_radiation_sum (MJ/m²)", "daylight_duration (s)", "apparent_temperature_min (°C)", "sunrise (iso8601)", "sunset (iso8601)", "precipitation_hours (h)", "et0_fao_evapotranspiration (mm)", "cloud_cover_mean (%)", "dew_point_2m_mean (°C)", "relative_humidity_2m_mean (%)", "wind_gusts_10m_mean (km/h)", "wind_speed_10m_mean (km/h)", "wind_gusts_10m_min (km/h)", "wind_speed_10m_min (km/h)"]
- `data/train.csv` (871168 bytes); columns: ["time", "temperature_2m_mean (°C)", "rain_sum (mm)", "wind_speed_10m_max (km/h)", "apparent_temperature_mean (°C)", "temperature_2m_min (°C)", "temperature_2m_max (°C)", "apparent_temperature_max (°C)", "weather_code (wmo code)", "wind_direction_10m_dominant (°)", "wind_gusts_10m_max (km/h)", "shortwave_radiation_sum (MJ/m²)", "daylight_duration (s)", "apparent_temperature_min (°C)", "sunrise (iso8601)", "sunset (iso8601)", "precipitation_hours (h)", "et0_fao_evapotranspiration (mm)", "cloud_cover_mean (%)", "dew_point_2m_mean (°C)", "relative_humidity_2m_mean (%)", "wind_gusts_10m_mean (km/h)", "wind_speed_10m_mean (km/h)", "wind_gusts_10m_min (km/h)", "wind_speed_10m_min (km/h)", "sunshine_duration (s)"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (121 lines)
test.csv (121 lines)
train.csv (5726 lines)```

-> sample_submission.csv has 120 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 119.00, 0 nan values
sunshine_duration (s) (float64) has 1 unique values: [39623.86]

-> test.csv has 120 rows and 26 columns.
Here is some information about the columns:
apparent_temperature_max (°C) (float64) has range: 12.30 - 36.10, 0 nan values
apparent_temperature_mean (°C) (float64) has range: 9.30 - 29.30, 0 nan values
apparent_temperature_min (°C) (float64) has range: 5.30 - 25.10, 0 nan values
cloud_cover_mean (%) (int64) has range: 0.00 - 100.00, 0 nan values
daylight_duration (s) (float64) has range: 36747.93 - 42278.86, 0 nan values
dew_point_2m_mean (°C) (float64) has range: -2.60 - 17.80, 0 nan values
et0_fao_evapotranspiration (mm) (float64) has range: 2.02 - 6.66, 0 nan values
id (int64) has range: 0.00 - 119.00, 0 nan values
precipitation_hours (h) (int64) has 5 unique values: [0, 3, 6, 1, 4]
rain_sum (mm) (float64) has 6 unique values: [0.0, 0.7, 0.6, 2.2, 0.1, 0.5]
relative_humidity_2m_mean (%) (int64) has range: 33.00 - 77.00, 0 nan values
shortwave_radiation_sum (MJ/m²) (float64) has range: 7.00 - 20.54, 0 nan values
sunrise (iso8601) (object) has 120 unique values. Some example values: ['2024-10-05T06:50', '2024-10-06T06:51', '2024-10-07T06:52', '2024-10-08T06:52']
sunset (iso8601) (object) has 120 unique values. Some example values: ['2024-10-05T18:35', '2024-10-06T18:34', '2024-10-07T18:33', '2024-10-08T18:31']
temperature_2m_max (°C) (float64) has range: 17.10 - 34.90, 0 nan values
temperature_2m_mean (°C) (float64) has range: 13.20 - 28.60, 0 nan values
temperature_2m_min (°C) (float64) has range: 9.00 - 21.90, 0 nan values
time (object) has 120 unique values. Some example values: ['10/5/2024', '10/6/2024', '10/7/2024', '10/8/2024']
weather_code (wmo code) (int64) has 7 unique values: [0, 3, 2, 1, 51, 55, 53]
wind_direction_10m_dominant (°) (int64) has range: 2.00 - 359.00, 0 nan values
wind_gusts_10m_max (km/h) (float64) has range: 15.50 - 53.30, 0 nan values
wind_gusts_10m_mean (km/h) (float64) has range: 8.10 - 38.20, 0 nan values
wind_gusts_10m_min (km/h) (float64) has range: 0.70 - 24.80, 0 nan values
wind_speed_10m_max (km/h) (float64) has range: 3.80 - 30.50, 0 nan values
wind_speed_10m_mean (km/h) (float64) has range: 1.80 - 22.20, 0 nan values
wind_speed_10m_min (km/h) (float64) has range: 0.00 - 15.60, 0 nan values

-> train.csv has 5725 rows and 26 columns.
Here is some information about the columns:
apparent_temperature_max (°C) (float64) has range: 5.00 - 44.50, 0 nan values
apparent_temperature_mean (°C) (float64) has range: 3.90 - 36.00, 0 nan values
apparent_temperature_min (°C) (float64) has range: 0.10 - 30.30, 0 nan values
cloud_cover_mean (%) (int64) has range: 0.00 - 100.00, 0 nan values
daylight_duration (s) (float64) has range: 36746.69 - 50694.67, 0 nan values
dew_point_2m_mean (°C) (float64) has range: -8.80 - 21.30, 0 nan values
et0_fao_evapotranspiration (mm) (float64) has range: 1.13 - 12.74, 0 nan values
precipitation_hours (h) (int64) has range: 0.00 - 20.00, 0 nan values
rain_sum (mm) (float64) has range: 0.00 - 43.10, 0 nan values
relative_humidity_2m_mean (%) (int64) has range: 10.00 - 86.00, 0 nan values
shortwave_radiation_sum (MJ/m²) (float64) has range: 4.84 - 30.07, 0 nan values
sunrise (iso8601) (object) has 5725 unique values. Some example values: ['2024-10-04T06:50', '2009-02-01T07:45', '2009-02-02T07:44', '2009-02-03T07:43']
sunset (iso8601) (object) has 5725 unique values. Some example values: ['2024-10-04T18:36', '2009-02-01T18:31', '2009-02-02T18:32', '2009-02-03T18:33']
sunshine_duration (s) (float64) has range: 0.00 - 47289.45, 0 nan values
temperature_2m_max (°C) (float64) has range: 11.20 - 45.40, 0 nan values
temperature_2m_mean (°C) (float64) has range: 8.60 - 37.40, 0 nan values
temperature_2m_min (°C) (float64) has range: 3.30 - 31.90, 0 nan values
time (object) has 5725 unique values. Some example values: ['10/4/2024', '2/1/2009', '2/2/2009', '2/3/2009']
weather_code (wmo code) (int64) has range: 0.00 - 65.00, 0 nan values
wind_direction_10m_dominant (°) (int64) has range: 0.00 - 360.00, 0 nan values
wind_gusts_10m_max (km/h) (float64) has range: 13.30 - 78.50, 0 nan values
wind_gusts_10m_mean (km/h) (float64) has range: 7.60 - 54.50, 0 nan values
wind_gusts_10m_min (km/h) (float64) has range: 1.10 - 41.00, 0 nan values
wind_speed_10m_max (km/h) (float64) has range: 6.90 - 43.20, 0 nan values
wind_speed_10m_mean (km/h) (float64) has range: 3.00 - 28.70, 0 nan values
wind_speed_10m_min (km/h) (float64) has range: 0.00 - 21.80, 0 nan values
