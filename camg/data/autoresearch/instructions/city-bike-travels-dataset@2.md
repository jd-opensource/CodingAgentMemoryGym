# OpenMLE-fast task

Task ID: `city-bike-travels-dataset@2`

Native metric: `CityBikeETAMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1218 bytes)
- `data/sample_submission.csv` (563268 bytes); columns: ["row_id", "duration"]
- `data/test.csv` (1523349 bytes); columns: ["row_id", "departure_time", "departure_station_id", "return_station_id"]
- `data/train.csv` (15044981 bytes); columns: ["departure_time", "departure_station_id", "return_station_id", "duration"]

## Public description

```
description.txt (43 lines)
sample_submission.csv (46643 lines)
test.csv (46643 lines)
train.csv (481375 lines)```

-> sample_submission.csv has 46642 rows and 2 columns.
Here is some information about the columns:
duration (float64) has range: 60.00 - 14280.00, 0 nan values
row_id (int64) has range: 0.00 - 46641.00, 0 nan values

-> test.csv has 46642 rows and 4 columns.
Here is some information about the columns:
departure_station_id (int64) has range: 1.00 - 902.00, 0 nan values
departure_time (object) has 20994 unique values. Some example values: ['2021-04-30 16:14:05', '2021-04-30 11:36:40', '2021-04-29 16:37:54', '2021-04-30 18:01:02']
return_station_id (int64) has range: 1.00 - 902.00, 0 nan values
row_id (int64) has range: 0.00 - 46641.00, 0 nan values

-> train.csv has 481374 rows and 4 columns.
Here is some information about the columns:
departure_station_id (int64) has range: 1.00 - 997.00, 0 nan values
departure_time (object) has 216899 unique values. Some example values: ['2021-04-16 18:58:18', '2021-04-21 14:17:52', '2021-04-20 17:59:19', '2021-04-18 17:04:19']
duration (int64) has range: 60.00 - 14308.00, 0 nan values
return_station_id (int64) has range: 1.00 - 997.00, 0 nan values
