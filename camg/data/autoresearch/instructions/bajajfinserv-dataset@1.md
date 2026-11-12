# OpenMLE-fast task

Task ID: `bajajfinserv-dataset@1`

Native metric: `BajajNextDayReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2376 bytes)
- `data/sample_submission.csv` (5774 bytes); columns: ["row_id", "target"]
- `data/test.csv` (74040 bytes); columns: ["row_id", "Date", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP", "Volume", "Turnover", "Trades", "Deliverable Volume", "%Deliverble"]
- `data/train.csv` (322703 bytes); columns: ["row_id", "Date", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP", "Volume", "Turnover", "Trades", "Deliverable Volume", "%Deliverble", "target"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (641 lines)
test.csv (641 lines)
train.csv (2561 lines)```

-> sample_submission.csv has 640 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 2560.00 - 3199.00, 0 nan values
target (float64) has 1 unique values: [0.0]

-> test.csv has 640 rows and 14 columns.
Here is some information about the columns:
%Deliverble (float64) has range: 0.06 - 0.63, 0 nan values
Close (float64) has range: 4097.25 - 11176.55, 0 nan values
Date (object) has 640 unique values. Some example values: ['2021-02-26', '2021-03-01', '2021-03-02', '2021-03-03']
Deliverable Volume (int64) has range: 4777.00 - 875036.00, 0 nan values
High (float64) has range: 4276.95 - 11300.00, 0 nan values
Last (float64) has range: 4095.20 - 11175.45, 0 nan values
Low (float64) has range: 3985.30 - 10520.00, 0 nan values
Open (float64) has range: 4100.00 - 10540.00, 0 nan values
Prev Close (float64) has range: 4097.25 - 10537.70, 0 nan values
Trades (float64) has range: 2512.00 - 312959.00, 0 nan values
Turnover (float64) has range: 9918412280000.00 - 3394379491190000.00, 0 nan values
VWAP (float64) has range: 4144.52 - 10980.40, 0 nan values
Volume (int64) has range: 17624.00 - 4110412.00, 0 nan values
row_id (int64) has range: 2560.00 - 3199.00, 0 nan values

-> train.csv has 2560 rows and 15 columns.
Here is some information about the columns:
%Deliverble (float64) has range: 0.06 - 1.00, 0 nan values
Close (float64) has range: 90.75 - 7116.60, 0 nan values
Date (object) has 2560 unique values. Some example values: ['2018-07-26', '2018-07-27', '2018-07-30', '2018-07-31']
Deliverable Volume (int64) has range: 456.00 - 3804696.00, 0 nan values
High (float64) has range: 93.10 - 7200.00, 0 nan values
Last (float64) has range: 91.00 - 7105.00, 0 nan values
Low (float64) has range: 88.15 - 7075.10, 0 nan values
Open (float64) has range: 88.15 - 7170.00, 0 nan values
Prev Close (float64) has range: 90.75 - 7116.60, 0 nan values
Trades (float64) has range: 149.00 - 153610.00, 745 nan values
Turnover (float64) has range: 13767125000.00 - 1211763486425000.00, 0 nan values
VWAP (float64) has range: 89.26 - 7139.13, 0 nan values
Volume (int64) has range: 457.00 - 6271671.00, 0 nan values
row_id (int64) has range: 0.00 - 2559.00, 0 nan values
target (float64) has range: -20.00 - 20.01, 0 nan values
