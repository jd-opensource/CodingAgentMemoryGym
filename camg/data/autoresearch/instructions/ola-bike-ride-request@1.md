# OpenMLE-fast task

Task ID: `ola-bike-ride-request@1`

Native metric: `OlaBikeDemandRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1571 bytes)
- `data/sample_submission.csv` (15077 bytes); columns: ["row_id", "casual", "registered"]
- `data/test.csv` (46279 bytes); columns: ["row_id", "datetime", "season", "weather", "temp", "humidity", "windspeed"]
- `data/train.csv` (469468 bytes); columns: ["datetime", "season", "weather", "temp", "humidity", "windspeed", "casual", "registered"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (1023 lines)
test.csv (1023 lines)
train.csv (9865 lines)```

-> sample_submission.csv has 1022 rows and 3 columns.
Here is some information about the columns:
casual (float64) has range: 22.00 - 31.00, 0 nan values
registered (float64) has range: 93.00 - 120.00, 0 nan values
row_id (int64) has range: 0.00 - 1021.00, 0 nan values

-> test.csv has 1022 rows and 7 columns.
Here is some information about the columns:
datetime (object) has 1022 unique values. Some example values: ['2012-03-29 13:00:00', '2012-02-16 00:00:00', '2012-02-16 01:00:00', '2012-02-16 02:00:00']
humidity (float64) has range: 20.03 - 99.88, 0 nan values
row_id (int64) has range: 0.00 - 1021.00, 0 nan values
season (int64) has 4 unique values: [4, 1, 2, 3]
temp (float64) has range: 5.07 - 35.00, 0 nan values
weather (int64) has 4 unique values: [3, 2, 1, 4]
windspeed (float64) has range: 0.00 - 49.90, 0 nan values

-> train.csv has 9864 rows and 8 columns.
Here is some information about the columns:
casual (int64) has range: 0.00 - 49.00, 0 nan values
datetime (object) has 9864 unique values. Some example values: ['2012-02-15 23:00:00', '2011-01-01 00:00:00', '2011-01-01 01:00:00', '2011-01-01 02:00:00']
humidity (float64) has range: 20.00 - 99.98, 0 nan values
registered (int64) has range: 0.00 - 199.00, 0 nan values
season (int64) has 4 unique values: [3, 4, 1, 2]
temp (float64) has range: 5.00 - 35.00, 0 nan values
weather (int64) has 4 unique values: [2, 3, 1, 4]
windspeed (float64) has range: 0.00 - 49.99, 0 nan values
