# OpenMLE-fast task

Task ID: `bitcoin-dataset-hourly@2`

Native metric: `BitcoinVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2246 bytes)
- `data/sample_submission.csv` (346559 bytes); columns: ["row_id", "rr_next"]
- `data/test.csv` (1642734 bytes); columns: ["row_id", "Timestamp", "Open", "High", "Low", "Close", "Volume", "Quote_Asset_Volume", "Number_of_Trades", "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume"]
- `data/train.csv` (7660105 bytes); columns: ["row_id", "Timestamp", "Open", "High", "Low", "Close", "Volume", "Quote_Asset_Volume", "Number_of_Trades", "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume", "rr_next"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (12870 lines)
test.csv (12870 lines)
train.csv (51478 lines)```

-> sample_submission.csv has 12869 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 51477.00 - 64345.00, 0 nan values
rr_next (float64) has range: 0.00 - 0.36, 0 nan values

-> test.csv has 12869 rows and 11 columns.
Here is some information about the columns:
Close (float64) has range: 25020.66 - 108258.39, 0 nan values
High (float64) has range: 25133.38 - 108353.00, 0 nan values
Low (float64) has range: 24901.00 - 107130.00, 0 nan values
Number_of_Trades (int64) has range: 8360.00 - 1235251.00, 0 nan values
Open (float64) has range: 25020.66 - 108258.38, 0 nan values
Quote_Asset_Volume (float64) has range: 3488263.13 - 1433205531.19, 0 nan values
Taker_Buy_Base_Volume (float64) has range: 46.10 - 14352.11, 0 nan values
Taker_Buy_Quote_Volume (float64) has range: 1498707.29 - 831597402.44, 0 nan values
Timestamp (object) has 12869 unique values. Some example values: ['2024-12-25 17:00:00+00:00', '2023-07-08 13:00:00+00:00', '2023-07-08 14:00:00+00:00', '2023-07-08 15:00:00+00:00']
Volume (float64) has range: 92.17 - 27563.36, 0 nan values
row_id (int64) has range: 51477.00 - 64345.00, 0 nan values

-> train.csv has 51477 rows and 12 columns.
Here is some information about the columns:
Close (float64) has range: 2919.00 - 68633.69, 0 nan values
High (float64) has range: 2950.00 - 69000.00, 0 nan values
Low (float64) has range: 2817.00 - 68451.19, 0 nan values
Number_of_Trades (int64) has range: 0.00 - 1442097.00, 0 nan values
Open (float64) has range: 2870.90 - 68635.12, 0 nan values
Quote_Asset_Volume (float64) has range: 0.00 - 3005633669.26, 0 nan values
Taker_Buy_Base_Volume (float64) has range: 0.00 - 68611.45, 0 nan values
Taker_Buy_Quote_Volume (float64) has range: 0.00 - 1502976679.73, 0 nan values
Timestamp (object) has 51477 unique values. Some example values: ['2023-07-08 12:00:00+00:00', '2017-08-17 04:00:00+00:00', '2017-08-17 05:00:00+00:00', '2017-08-17 06:00:00+00:00']
Volume (float64) has range: 0.00 - 137207.19, 0 nan values
row_id (int64) has range: 0.00 - 51476.00, 0 nan values
rr_next (float64) has range: 0.00 - 0.36, 0 nan values
