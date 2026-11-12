# OpenMLE-fast task

Task ID: `flights@1`

Native metric: `FlightDelayLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2749 bytes)
- `data/sample_submission.csv` (1040427 bytes); columns: ["late15"]
- `data/test.csv` (5002760 bytes); columns: ["year", "month", "day", "sched_dep_time", "sched_arr_time", "carrier", "flight", "tailnum", "origin", "dest", "distance", "hour", "minute", "time_hour", "name"]
- `data/train.csv` (25618071 bytes); columns: ["year", "month", "day", "sched_dep_time", "sched_arr_time", "carrier", "flight", "tailnum", "origin", "dest", "distance", "hour", "minute", "time_hour", "name", "late15"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (53992 lines)
test.csv (53992 lines)
train.csv (273356 lines)```

-> sample_submission.csv has 53991 rows and 1 columns.
Here is some information about the columns:
late15 (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 53991 rows and 15 columns.
Here is some information about the columns:
carrier (object) has 16 unique values. Some example values: ['UA', 'B6', 'EV', 'DL']
day (int64) has range: 1.00 - 31.00, 0 nan values
dest (object) has 97 unique values. Some example values: ['ATL', 'LAX', 'ORD', 'MCO']
distance (int64) has range: 94.00 - 4983.00, 0 nan values
flight (int64) has range: 1.00 - 6181.00, 0 nan values
hour (int64) has range: 5.00 - 23.00, 0 nan values
minute (int64) has range: 0.00 - 59.00, 0 nan values
month (int64) has 2 unique values: [11, 12]
name (object) has 16 unique values. Some example values: ['United Air Lines Inc.', 'JetBlue Airways', 'ExpressJet Airlines Inc.', 'Delta Air Lines Inc.']
origin (object) has 3 unique values: ['JFK', 'EWR', 'LGA']
sched_arr_time (int64) has range: 1.00 - 2359.00, 0 nan values
sched_dep_time (int64) has range: 500.00 - 2359.00, 0 nan values
tailnum (object) has 3411 unique values. Some example values: ['N857MQ', 'N813MQ', 'N527MQ', 'N839MQ']
time_hour (object) has 1159 unique values. Some example values: ['2013-11-01 08:00:00', '2013-11-26 08:00:00', '2013-11-22 08:00:00', '2013-11-21 08:00:00']
year (int64) has 1 unique values: [2013]

-> train.csv has 273355 rows and 16 columns.
Here is some information about the columns:
carrier (object) has 16 unique values. Some example values: ['UA', 'B6', 'EV', 'DL']
day (int64) has range: 1.00 - 31.00, 0 nan values
dest (object) has 103 unique values. Some example values: ['ORD', 'ATL', 'LAX', 'BOS']
distance (int64) has range: 80.00 - 4983.00, 0 nan values
flight (int64) has range: 1.00 - 8500.00, 0 nan values
hour (int64) has range: 5.00 - 23.00, 0 nan values
late15 (int64) has 2 unique values: [0, 1]
minute (int64) has range: 0.00 - 59.00, 0 nan values
month (int64) has range: 1.00 - 10.00, 0 nan values
name (object) has 16 unique values. Some example values: ['United Air Lines Inc.', 'JetBlue Airways', 'ExpressJet Airlines Inc.', 'Delta Air Lines Inc.']
origin (object) has 3 unique values: ['EWR', 'LGA', 'JFK']
sched_arr_time (int64) has range: 1.00 - 2359.00, 0 nan values
sched_dep_time (int64) has range: 500.00 - 2359.00, 0 nan values
tailnum (object) has 3960 unique values. Some example values: ['N725MQ', 'N722MQ', 'N723MQ', 'N711MQ']
time_hour (object) has 5763 unique values. Some example values: ['2013-09-20 08:00:00', '2013-09-23 08:00:00', '2013-09-19 08:00:00', '2013-09-16 08:00:00']
year (int64) has 1 unique values: [2013]
