# OpenMLE-fast task

Task ID: `austin-weather@1`

Native metric: `AustinWeatherMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3453 bytes)
- `data/sample_submission.csv` (4838 bytes); columns: ["row_id", "ThunderstormNextDay"]
- `data/test.csv` (23515 bytes); columns: ["row_id", "Date", "TempHighF", "TempAvgF", "TempLowF", "DewPointHighF", "DewPointAvgF", "DewPointLowF", "HumidityHighPercent", "HumidityAvgPercent", "HumidityLowPercent", "SeaLevelPressureHighInches", "SeaLevelPressureAvgInches", "SeaLevelPressureLowInches", "VisibilityHighMiles", "VisibilityAvgMiles", "VisibilityLowMiles", "WindHighMPH", "WindAvgMPH", "WindGustMPH", "PrecipitationSumInches"]
- `data/train.csv` (129978 bytes); columns: ["row_id", "Date", "TempHighF", "TempAvgF", "TempLowF", "DewPointHighF", "DewPointAvgF", "DewPointLowF", "HumidityHighPercent", "HumidityAvgPercent", "HumidityLowPercent", "SeaLevelPressureHighInches", "SeaLevelPressureAvgInches", "SeaLevelPressureLowInches", "VisibilityHighMiles", "VisibilityAvgMiles", "VisibilityLowMiles", "WindHighMPH", "WindAvgMPH", "WindGustMPH", "PrecipitationSumInches", "ThunderstormNextDay"]

## Public description

```
description.txt (46 lines)
sample_submission.csv (212 lines)
test.csv (212 lines)
train.csv (1108 lines)```

-> sample_submission.csv has 211 rows and 2 columns.
Here is some information about the columns:
ThunderstormNextDay (float64) has range: 0.01 - 0.99, 0 nan values
row_id (int64) has range: 1.00 - 211.00, 0 nan values

-> test.csv has 211 rows and 21 columns.
Here is some information about the columns:
Date (object) has 211 unique values. Some example values: ['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04']
DewPointAvgF (float64) has range: 11.00 - 74.00, 0 nan values
DewPointHighF (float64) has range: 13.00 - 76.00, 0 nan values
DewPointLowF (float64) has range: 6.00 - 72.00, 0 nan values
HumidityAvgPercent (float64) has range: 30.00 - 94.00, 0 nan values
HumidityHighPercent (float64) has range: 42.00 - 100.00, 0 nan values
HumidityLowPercent (float64) has range: 15.00 - 87.00, 0 nan values
PrecipitationSumInches (float64) has range: 0.00 - 1.57, 0 nan values
SeaLevelPressureAvgInches (float64) has range: 29.56 - 30.74, 0 nan values
SeaLevelPressureHighInches (float64) has range: 29.63 - 30.83, 0 nan values
SeaLevelPressureLowInches (float64) has range: 29.41 - 30.61, 0 nan values
TempAvgF (float64) has range: 29.00 - 93.00, 0 nan values
TempHighF (float64) has range: 34.00 - 107.00, 0 nan values
TempLowF (float64) has range: 19.00 - 79.00, 0 nan values
VisibilityAvgMiles (float64) has 7 unique values: [8.0, 10.0, 3.0, 4.0, 9.0, 7.0, 6.0]
VisibilityHighMiles (float64) has 2 unique values: [10.0, 9.0]
VisibilityLowMiles (float64) has range: 0.00 - 10.00, 0 nan values
WindAvgMPH (float64) has range: 1.00 - 11.00, 0 nan values
WindGustMPH (float64) has range: 11.00 - 43.00, 0 nan values
WindHighMPH (float64) has range: 7.00 - 25.00, 0 nan values
row_id (int64) has range: 1.00 - 211.00, 0 nan values

-> train.csv has 1107 rows and 22 columns.
Here is some information about the columns:
Date (object) has 1107 unique values. Some example values: ['2016-12-31', '2013-12-21', '2013-12-22', '2013-12-23']
DewPointAvgF (float64) has range: 8.00 - 76.00, 0 nan values
DewPointHighF (float64) has range: 15.00 - 80.00, 0 nan values
DewPointLowF (float64) has range: 2.00 - 75.00, 0 nan values
HumidityAvgPercent (float64) has range: 27.00 - 97.00, 0 nan values
HumidityHighPercent (float64) has range: 37.00 - 100.00, 0 nan values
HumidityLowPercent (float64) has range: 10.00 - 93.00, 0 nan values
PrecipitationSumInches (float64) has range: 0.00 - 5.20, 0 nan values
SeaLevelPressureAvgInches (float64) has range: 29.55 - 30.68, 0 nan values
SeaLevelPressureHighInches (float64) has range: 29.63 - 30.80, 0 nan values
SeaLevelPressureLowInches (float64) has range: 29.44 - 30.60, 0 nan values
TempAvgF (float64) has range: 29.00 - 92.00, 0 nan values
TempHighF (float64) has range: 32.00 - 105.00, 0 nan values
TempLowF (float64) has range: 22.00 - 81.00, 0 nan values
ThunderstormNextDay (float64) has 2 unique values: [0.0, 1.0]
VisibilityAvgMiles (float64) has 9 unique values: [7.0, 10.0, 9.0, 2.0, 4.0, 8.0, 6.0, 5.0, 3.0]
VisibilityHighMiles (float64) has 4 unique values: [10.0, 9.0, 8.0, 5.0]
VisibilityLowMiles (float64) has range: 0.00 - 10.00, 0 nan values
WindAvgMPH (float64) has range: 1.00 - 12.00, 0 nan values
WindGustMPH (float64) has range: 9.00 - 57.00, 0 nan values
WindHighMPH (float64) has range: 6.00 - 29.00, 0 nan values
row_id (int64) has range: 100000.00 - 101106.00, 0 nan values
