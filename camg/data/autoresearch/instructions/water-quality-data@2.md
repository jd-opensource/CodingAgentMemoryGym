# OpenMLE-fast task

Task ID: `water-quality-data@2`

Native metric: `WaterClarityRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1657 bytes)
- `data/sample_submission.csv` (14309 bytes); columns: ["row_id", "SecchiDepth (m)"]
- `data/test.csv` (28401 bytes); columns: ["row_id", "Date", "Salinity (ppt)", "DissolvedOxygen (mg/L)", "pH", "WaterDepth (m)", "WaterTemp (C)", "AirTemp (C)"]
- `data/train.csv` (82732 bytes); columns: ["row_id", "Date", "Salinity (ppt)", "DissolvedOxygen (mg/L)", "pH", "WaterDepth (m)", "WaterTemp (C)", "AirTemp (C)", "SecchiDepth (m)"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (605 lines)
test.csv (605 lines)
train.csv (1692 lines)```

-> sample_submission.csv has 604 rows and 2 columns.
Here is some information about the columns:
SecchiDepth (m) (float64) has range: 0.00 - 1.81, 0 nan values
row_id (int64) has range: 1691.00 - 2294.00, 0 nan values

-> test.csv has 604 rows and 8 columns.
Here is some information about the columns:
AirTemp (C) (float64) has range: -5.00 - 31.11, 1 nan values
Date (object) has 159 unique values. Some example values: ['2017-04-04', '2012-05-10', '2012-04-26', '2012-06-14']
DissolvedOxygen (mg/L) (float64) has range: 0.00 - 10.00, 247 nan values
Salinity (ppt) (float64) has range: 0.00 - 9.00, 16 nan values
WaterDepth (m) (float64) has range: 0.01 - 12.00, 1 nan values
WaterTemp (C) (float64) has range: 0.00 - 33.00, 16 nan values
pH (float64) has range: 4.80 - 9.00, 15 nan values
row_id (int64) has range: 1691.00 - 2294.00, 0 nan values

-> train.csv has 1691 rows and 9 columns.
Here is some information about the columns:
AirTemp (C) (float64) has range: -11.94 - 33.50, 61 nan values
Date (object) has 632 unique values. Some example values: ['2008-01-17', '2008-02-07', '2008-02-19', '2008-03-21']
DissolvedOxygen (mg/L) (float64) has range: 0.00 - 15.10, 555 nan values
Salinity (ppt) (float64) has range: 0.00 - 9.00, 90 nan values
SecchiDepth (m) (float64) has range: 0.00 - 7.40, 0 nan values
WaterDepth (m) (float64) has range: 0.01 - 8.50, 2 nan values
WaterTemp (C) (float64) has range: 0.00 - 74.00, 82 nan values
pH (float64) has range: 0.30 - 9.90, 56 nan values
row_id (int64) has range: 0.00 - 1690.00, 0 nan values
