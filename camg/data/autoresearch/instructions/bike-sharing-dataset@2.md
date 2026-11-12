# OpenMLE-fast task

Task ID: `bike-sharing-dataset@2`

Native metric: `BikeSharingRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1951 bytes)
- `data/sample_submission.csv` (2347 bytes); columns: ["dteday", "cnt"]
- `data/test.csv` (8874 bytes); columns: ["dteday", "season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed"]
- `data/train.csv` (37824 bytes); columns: ["dteday", "season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed", "cnt"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (147 lines)
test.csv (147 lines)
train.csv (585 lines)```

-> sample_submission.csv has 146 rows and 2 columns.
Here is some information about the columns:
cnt (int64) has range: 3657.00 - 4795.00, 0 nan values
dteday (object) has 146 unique values. Some example values: ['2019-08-08', '2019-08-09', '2019-08-10', '2019-08-11']

-> test.csv has 146 rows and 12 columns.
Here is some information about the columns:
atemp (float64) has range: 11.02 - 35.45, 0 nan values
dteday (object) has 146 unique values. Some example values: ['2019-08-08', '2019-08-09', '2019-08-10', '2019-08-11']
holiday (int64) has 2 unique values: [0, 1]
hum (float64) has range: 33.35 - 92.50, 0 nan values
mnth (int64) has 5 unique values: [8, 9, 10, 11, 12]
season (int64) has 3 unique values: [3, 4, 1]
temp (float64) has range: 8.85 - 31.33, 0 nan values
weathersit (int64) has 3 unique values: [2, 1, 3]
weekday (int64) has 7 unique values: [3, 4, 5, 6, 0, 1, 2]
windspeed (float64) has range: 3.13 - 27.29, 0 nan values
workingday (int64) has 2 unique values: [1, 0]
yr (int64) has 1 unique values: [1]

-> train.csv has 584 rows and 13 columns.
Here is some information about the columns:
atemp (float64) has range: 3.95 - 42.04, 0 nan values
cnt (int64) has range: 431.00 - 8362.00, 0 nan values
dteday (object) has 584 unique values. Some example values: ['2019-08-07', '2018-01-01', '2018-01-02', '2018-01-03']
holiday (int64) has 2 unique values: [0, 1]
hum (float64) has range: 0.00 - 97.25, 0 nan values
mnth (int64) has range: 1.00 - 12.00, 0 nan values
season (int64) has 4 unique values: [1, 2, 3, 4]
temp (float64) has range: 2.42 - 35.33, 0 nan values
weathersit (int64) has 3 unique values: [2, 1, 3]
weekday (int64) has 7 unique values: [6, 0, 1, 2, 3, 4, 5]
windspeed (float64) has range: 1.50 - 34.00, 0 nan values
workingday (int64) has 2 unique values: [0, 1]
yr (int64) has 2 unique values: [0, 1]
