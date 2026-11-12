# OpenMLE-fast task

Task ID: `electricity-consumption-uk-20092022@1`

Native metric: `ElectricityDemandForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1442 bytes)
- `data/sample_submission.csv` (359006 bytes); columns: ["row_id", "nd"]
- `data/test.csv` (633388 bytes); columns: ["row_id", "timestamp", "settlement_period", "is_holiday"]
- `data/train.csv` (12274000 bytes); columns: ["row_id", "timestamp", "settlement_period", "is_holiday", "nd"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (16319 lines)
test.csv (16319 lines)
train.csv (262195 lines)```

-> sample_submission.csv has 16318 rows and 2 columns.
Here is some information about the columns:
nd (float64) has range: 14511.00 - 58144.00, 0 nan values
row_id (object) has 16318 unique values. Some example values: ['20241205_P048', '20240101_P001', '20240101_P002', '20240101_P003']

-> test.csv has 16318 rows and 4 columns.
Here is some information about the columns:
is_holiday (int64) has 2 unique values: [1, 0]
row_id (object) has 16318 unique values. Some example values: ['20241205_P048', '20240101_P001', '20240101_P002', '20240101_P003']
settlement_period (int64) has range: 1.00 - 48.00, 0 nan values
timestamp (object) has 16318 unique values. Some example values: ['2024-12-05 23:30:00', '2024-01-01 00:00:00', '2024-01-01 00:30:00', '2024-01-01 01:00:00']

-> train.csv has 262194 rows and 5 columns.
Here is some information about the columns:
is_holiday (int64) has 2 unique values: [1, 0]
nd (float64) has range: 13367.00 - 59095.00, 0 nan values
row_id (object) has 262194 unique values. Some example values: ['20231231_P048', '20090101_P001', '20090101_P002', '20090101_P003']
settlement_period (int64) has range: 1.00 - 48.00, 0 nan values
timestamp (object) has 262194 unique values. Some example values: ['2023-12-31 23:30:00', '2009-01-01 00:00:00', '2009-01-01 00:30:00', '2009-01-01 01:00:00']
