# OpenMLE-fast task

Task ID: `bitcoin-price-history-btc-usd@1`

Native metric: `WeightedRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1348 bytes)
- `data/sample_submission.csv` (18516 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]
- `data/test.csv` (1985 bytes); columns: ["Date"]
- `data/train.csv` (147265 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (181 lines)
test.csv (181 lines)
train.csv (1774 lines)```

-> sample_submission.csv has 180 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 29228.38 - 52413.82, 0 nan values
Date (object) has 180 unique values. Some example values: ['2023-11-09', '2023-11-10', '2023-11-11', '2023-11-12']
High (float64) has range: 31414.54 - 52820.21, 0 nan values
Low (float64) has range: 24973.04 - 39339.58, 0 nan values
Open (float64) has range: 25784.42 - 44941.56, 0 nan values
Volume (float64) has range: 9956026109.18 - 38097737448.26, 0 nan values

-> test.csv has 180 rows and 1 columns.
Here is some information about the columns:
Date (object) has 180 unique values. Some example values: ['2023-11-09', '2023-11-10', '2023-11-11', '2023-11-12']

-> train.csv has 1773 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 3399.47 - 67566.83, 0 nan values
Date (object) has 1773 unique values. Some example values: ['2023-11-08', '2019-01-01', '2019-01-02', '2019-01-03']
High (float64) has range: 3427.95 - 68789.62, 0 nan values
Low (float64) has range: 3391.02 - 66382.06, 0 nan values
Open (float64) has range: 3401.38 - 67549.73, 0 nan values
Volume (int64) has range: 4324200990.00 - 350967941479.00, 0 nan values
