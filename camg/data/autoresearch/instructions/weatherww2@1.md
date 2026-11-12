# OpenMLE-fast task

Task ID: `weatherww2@1`

Native metric: `WW2PrecipitationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2895 bytes)
- `data/sample_submission.csv` (487017 bytes); columns: ["Id", "Precip"]
- `data/test.csv` (3321903 bytes); columns: ["Id", "STA", "Date", "YR", "MO", "DA", "Latitude", "Longitude", "ELEV", "MaxTemp", "MinTemp", "MeanTemp", "Snowfall", "PoorWeatherFlag", "TSHDSBRSGF_Flag", "day_of_year", "sin_doy", "cos_doy"]
- `data/train.csv` (13729103 bytes); columns: ["Id", "STA", "Date", "YR", "MO", "DA", "Latitude", "Longitude", "ELEV", "MaxTemp", "MinTemp", "MeanTemp", "Snowfall", "PoorWeatherFlag", "TSHDSBRSGF_Flag", "day_of_year", "sin_doy", "cos_doy", "Precip"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (23749 lines)
test.csv (23749 lines)
train.csv (95293 lines)
zero_submission.csv (23749 lines)```

-> sample_submission.csv has 23748 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 926.00 - 119039.00, 0 nan values
Precip (float64) has range: 0.00 - 15.57, 0 nan values

-> test.csv has 23748 rows and 18 columns.
Here is some information about the columns:
DA (int64) has range: 1.00 - 31.00, 0 nan values
Date (object) has 916 unique values. Some example values: ['1945-12-23', '1945-11-18', '1945-11-19', '1945-11-22']
ELEV (int64) has range: 1.00 - 9999.00, 0 nan values
Id (int64) has range: 926.00 - 119039.00, 0 nan values
Latitude (float64) has range: -27.60 - 67.02, 0 nan values
Longitude (float64) has range: -175.00 - 177.37, 0 nan values
MO (int64) has range: 1.00 - 12.00, 0 nan values
MaxTemp (float64) has range: -23.89 - 48.89, 0 nan values
MeanTemp (float64) has range: -26.67 - 39.44, 0 nan values
MinTemp (float64) has range: -30.00 - 33.89, 0 nan values
PoorWeatherFlag (int64) has 1 unique values: [1]
STA (int64) has range: 10001.00 - 82506.00, 0 nan values
Snowfall (float64) has range: 0.00 - 86.36, 0 nan values
TSHDSBRSGF_Flag (int64) has 1 unique values: [1]
YR (int64) has 4 unique values: [45, 44, 41, 43]
cos_doy (float64) has range: -1.00 - 1.00, 0 nan values
day_of_year (int64) has range: 1.00 - 366.00, 0 nan values
sin_doy (float64) has range: -1.00 - 1.00, 0 nan values

-> train.csv has 95292 rows and 19 columns.
Here is some information about the columns:
DA (int64) has range: 1.00 - 31.00, 0 nan values
Date (object) has 2183 unique values. Some example values: ['1944-10-19', '1944-10-18', '1944-10-23', '1944-10-22']
ELEV (int64) has range: 1.00 - 9999.00, 0 nan values
Id (int64) has range: 0.00 - 118956.00, 0 nan values
Latitude (float64) has range: -27.60 - 67.02, 0 nan values
Longitude (float64) has range: -175.00 - 177.37, 0 nan values
MO (int64) has range: 1.00 - 12.00, 0 nan values
MaxTemp (float64) has range: -33.33 - 50.00, 0 nan values
MeanTemp (float64) has range: -35.56 - 40.00, 0 nan values
MinTemp (float64) has range: -38.33 - 34.44, 0 nan values
PoorWeatherFlag (int64) has 1 unique values: [1]
Precip (float64) has range: 0.00 - 273.56, 0 nan values
STA (int64) has range: 10001.00 - 82506.00, 0 nan values
Snowfall (float64) has range: 0.00 - 81.28, 0 nan values
TSHDSBRSGF_Flag (int64) has 1 unique values: [1]
YR (int64) has 6 unique values: [42, 43, 44, 45, 41, 40]
cos_doy (float64) has range: -1.00 - 1.00, 0 nan values
day_of_year (int64) has range: 1.00 - 366.00, 0 nan values
sin_doy (float64) has range: -1.00 - 1.00, 0 nan values

-> zero_submission.csv has 23748 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 926.00 - 119039.00, 0 nan values
Precip (float64) has 1 unique values: [0.0]
