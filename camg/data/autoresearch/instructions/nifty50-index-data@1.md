# OpenMLE-fast task

Task ID: `nifty50-index-data@1`

Native metric: `Nifty50OHLCLogRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2514 bytes)
- `data/sample_submission.csv` (35046 bytes); columns: ["TargetDate", "Open_T1", "High_T1", "Low_T1", "Close_T1"]
- `data/test.csv` (33398 bytes); columns: ["TargetDate", "RefDate", "Open_T0", "High_T0", "Low_T0", "Close_T0", "SharesTraded_T0", "TurnoverCr_T0", "DayOfWeek_T0", "Month_T0"]
- `data/train.csv` (184967 bytes); columns: ["TargetDate", "RefDate", "Open_T0", "High_T0", "Low_T0", "Close_T0", "SharesTraded_T0", "TurnoverCr_T0", "DayOfWeek_T0", "Month_T0", "Open_T1", "High_T1", "Low_T1", "Close_T1"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (411 lines)
test.csv (411 lines)
train.csv (1645 lines)```

-> sample_submission.csv has 410 rows and 5 columns.
Here is some information about the columns:
Close_T1 (float64) has range: 15882.68 - 22635.64, 0 nan values
High_T1 (float64) has range: 15895.63 - 22589.57, 0 nan values
Low_T1 (float64) has range: 15728.00 - 22513.21, 0 nan values
Open_T1 (float64) has range: 15735.69 - 22448.40, 0 nan values
TargetDate (object) has 410 unique values. Some example values: ['2024-02-29', '2022-07-07', '2022-07-08', '2022-07-11']

-> test.csv has 410 rows and 10 columns.
Here is some information about the columns:
Close_T0 (float64) has range: 15938.65 - 22217.45, 0 nan values
DayOfWeek_T0 (int64) has 7 unique values: [2, 3, 4, 0, 1, 6, 5]
High_T0 (float64) has range: 16011.35 - 22297.50, 0 nan values
Low_T0 (float64) has range: 15800.90 - 22186.10, 0 nan values
Month_T0 (int64) has range: 1.00 - 12.00, 0 nan values
Open_T0 (float64) has range: 15818.20 - 22290.00, 0 nan values
RefDate (object) has 410 unique values. Some example values: ['2024-02-28', '2022-07-06', '2022-07-07', '2022-07-08']
SharesTraded_T0 (float64) has range: 37311902.00 - 696495765.00, 1 nan values
TargetDate (object) has 410 unique values. Some example values: ['2024-02-29', '2022-07-07', '2022-07-08', '2022-07-11']
TurnoverCr_T0 (float64) has range: 2482.27 - 70755.08, 1 nan values

-> train.csv has 1644 rows and 14 columns.
Here is some information about the columns:
Close_T0 (float64) has range: 6970.60 - 18477.05, 0 nan values
Close_T1 (float64) has range: 6970.60 - 18477.05, 0 nan values
DayOfWeek_T0 (int64) has 7 unique values: [0, 1, 2, 4, 3, 6, 5]
High_T0 (float64) has range: 7034.20 - 18604.45, 0 nan values
High_T1 (float64) has range: 7034.20 - 18604.45, 0 nan values
Low_T0 (float64) has range: 6825.80 - 18445.30, 0 nan values
Low_T1 (float64) has range: 6825.80 - 18445.30, 0 nan values
Month_T0 (int64) has range: 1.00 - 12.00, 0 nan values
Open_T0 (float64) has range: 7023.65 - 18602.35, 0 nan values
Open_T1 (float64) has range: 7023.65 - 18602.35, 0 nan values
RefDate (object) has 1644 unique values. Some example values: ['2022-07-05', '2015-11-09', '2015-11-10', '2015-11-11']
SharesTraded_T0 (float64) has range: 16610872.00 - 1811564187.00, 1 nan values
TargetDate (object) has 1644 unique values. Some example values: ['2022-07-06', '2015-11-10', '2015-11-11', '2015-11-13']
TurnoverCr_T0 (float64) has range: 805.89 - 78522.93, 1 nan values
