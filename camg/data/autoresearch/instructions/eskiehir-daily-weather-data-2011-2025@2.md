# OpenMLE-fast task

Task ID: `eskiehir-daily-weather-data-2011-2025@2`

Native metric: `ExtremeWeatherEventMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3840 bytes)
- `data/sample_submission.csv` (88612 bytes); columns: ["Id", "Heat", "Cold", "Windy", "Calm", "HighPressure", "LowPressure", "Humid", "Dry", "RapidPressureDrop"]
- `data/test.csv` (43610 bytes); columns: ["Id", "Year", "Month", "Day", "Temperature (°F) Max", "Temperature (°F) Avg", "Temperature (°F) Min", "Dew Point (°F) Max", "Dew Point (°F) Avg", "Dew Point (°F) Min", "Humidity (%) Max", "Humidity (%) Avg", "Humidity (%) Min", "Wind Speed (mph) Max", "Wind Speed (mph) Avg", "Wind Speed (mph) Min", "Pressure (in) Max", "Pressure (in) Avg", "Pressure (in) Min"]
- `data/train.csv` (503137 bytes); columns: ["Id", "Year", "Month", "Day", "Temperature (°F) Max", "Temperature (°F) Avg", "Temperature (°F) Min", "Dew Point (°F) Max", "Dew Point (°F) Avg", "Dew Point (°F) Min", "Humidity (%) Max", "Humidity (%) Avg", "Humidity (%) Min", "Wind Speed (mph) Max", "Wind Speed (mph) Avg", "Wind Speed (mph) Min", "Pressure (in) Max", "Pressure (in) Avg", "Pressure (in) Min", "Heat", "Cold", "Windy", "Calm", "HighPressure", "LowPressure", "Humid", "Dry", "RapidPressureDrop"]

## Public description

```
description.txt (69 lines)
sample_submission.csv (500 lines)
test.csv (500 lines)
train.csv (4749 lines)```

-> sample_submission.csv has 499 rows and 10 columns.
Here is some information about the columns:
Calm (float64) has range: 0.00 - 1.00, 0 nan values
Cold (float64) has range: 0.00 - 1.00, 0 nan values
Dry (float64) has range: 0.00 - 1.00, 0 nan values
Heat (float64) has range: 0.00 - 1.00, 0 nan values
HighPressure (float64) has range: 0.00 - 0.99, 0 nan values
Humid (float64) has range: 0.00 - 1.00, 0 nan values
Id (int64) has range: 0.00 - 498.00, 0 nan values
LowPressure (float64) has range: 0.00 - 1.00, 0 nan values
RapidPressureDrop (float64) has range: 0.00 - 1.00, 0 nan values
Windy (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 499 rows and 19 columns.
Here is some information about the columns:
Day (int64) has range: 1.00 - 31.00, 0 nan values
Dew Point (°F) Avg (float64) has range: 9.50 - 62.60, 0 nan values
Dew Point (°F) Max (float64) has range: 14.00 - 66.00, 0 nan values
Dew Point (°F) Min (float64) has range: 0.00 - 59.00, 0 nan values
Humidity (%) Avg (float64) has range: 26.80 - 99.20, 0 nan values
Humidity (%) Max (float64) has range: 40.00 - 100.00, 0 nan values
Humidity (%) Min (float64) has range: 0.00 - 93.00, 0 nan values
Id (int64) has range: 0.00 - 498.00, 0 nan values
Month (int64) has range: 1.00 - 12.00, 0 nan values
Pressure (in) Avg (float64) has range: 22.70 - 27.70, 0 nan values
Pressure (in) Max (float64) has 8 unique values: [27.5, 27.4, 27.3, 27.2, 27.6, 27.1, 27.7, 27.8]
Pressure (in) Min (float64) has range: 0.00 - 27.70, 0 nan values
Temperature (°F) Avg (float64) has range: 21.00 - 81.40, 0 nan values
Temperature (°F) Max (float64) has range: 28.00 - 99.00, 0 nan values
Temperature (°F) Min (float64) has range: 0.00 - 68.00, 0 nan values
Wind Speed (mph) Avg (float64) has range: 1.60 - 14.50, 0 nan values
Wind Speed (mph) Max (float64) has range: 5.00 - 37.00, 0 nan values
Wind Speed (mph) Min (float64) has 8 unique values: [0.0, 2.0, 1.0, 5.0, 8.0, 3.0, 7.0, 6.0]
Year (int64) has 2 unique values: [2024, 2025]

-> train.csv has 4748 rows and 28 columns.
Here is some information about the columns:
Calm (int64) has 2 unique values: [0, 1]
Cold (int64) has 2 unique values: [0, 1]
Day (int64) has range: 1.00 - 31.00, 0 nan values
Dew Point (°F) Avg (float64) has range: 0.00 - 65.30, 0 nan values
Dew Point (°F) Max (float64) has range: 0.00 - 70.00, 0 nan values
Dew Point (°F) Min (float64) has range: -35.00 - 63.00, 0 nan values
Dry (int64) has 2 unique values: [0, 1]
Heat (int64) has 2 unique values: [0, 1]
HighPressure (int64) has 2 unique values: [0, 1]
Humid (int64) has 2 unique values: [0, 1]
Humidity (%) Avg (float64) has range: 26.90 - 100.00, 0 nan values
Humidity (%) Max (float64) has range: 44.00 - 100.00, 0 nan values
Humidity (%) Min (float64) has range: 0.00 - 100.00, 0 nan values
Id (int64) has range: 0.00 - 4747.00, 0 nan values
LowPressure (int64) has 2 unique values: [0, 1]
Month (int64) has range: 1.00 - 12.00, 0 nan values
Pressure (in) Avg (float64) has range: 24.80 - 27.80, 0 nan values
Pressure (in) Max (float64) has range: 26.90 - 27.80, 0 nan values
Pressure (in) Min (float64) has range: 0.00 - 27.80, 0 nan values
RapidPressureDrop (int64) has 2 unique values: [0, 1]
Temperature (°F) Avg (float64) has range: 6.60 - 85.50, 0 nan values
Temperature (°F) Max (float64) has range: 16.00 - 106.00, 0 nan values
Temperature (°F) Min (float64) has range: -6.00 - 72.00, 0 nan values
Wind Speed (mph) Avg (float64) has range: 0.00 - 19.80, 0 nan values
Wind Speed (mph) Max (float64) has range: 0.00 - 41.00, 0 nan values
Wind Speed (mph) Min (float64) has range: 0.00 - 13.00, 0 nan values
Windy (int64) has 2 unique values: [0, 1]
Year (int64) has range: 2011.00 - 2023.00, 0 nan values
