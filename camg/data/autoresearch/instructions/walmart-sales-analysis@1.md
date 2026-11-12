# OpenMLE-fast task

Task ID: `walmart-sales-analysis@1`

Native metric: `WalmartSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1591 bytes)
- `data/sample_submission.csv` (13555 bytes); columns: ["Id", "Weekly_Sales"]
- `data/test.csv` (24874 bytes); columns: ["Id", "Store_Number", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
- `data/train.csv` (291830 bytes); columns: ["Id", "Store_Number", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment", "Weekly_Sales"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (586 lines)
test.csv (586 lines)
train.csv (5851 lines)```

-> sample_submission.csv has 585 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 131.00 - 6435.00, 0 nan values
Weekly_Sales (float64) has range: 132086.46 - 7111163.29, 0 nan values

-> test.csv has 585 rows and 8 columns.
Here is some information about the columns:
CPI (int64) has range: 131.00 - 227.00, 0 nan values
Date (object) has 13 unique values. Some example values: ['2012-08-03', '2012-08-10', '2012-08-17', '2012-08-24']
Fuel_Price (float64) has range: 3.37 - 4.47, 0 nan values
Holiday_Flag (int64) has 2 unique values: [0, 1]
Id (int64) has range: 131.00 - 6435.00, 0 nan values
Store_Number (int64) has range: 1.00 - 45.00, 0 nan values
Temperature (float64) has range: 39.38 - 100.07, 0 nan values
Unemployment (float64) has range: 3.88 - 10.93, 0 nan values

-> train.csv has 5850 rows and 9 columns.
Here is some information about the columns:
CPI (int64) has range: 126.00 - 226.00, 0 nan values
Date (object) has 130 unique values. Some example values: ['2010-02-05', '2010-02-12', '2010-02-19', '2010-02-26']
Fuel_Price (float64) has range: 2.47 - 4.31, 0 nan values
Holiday_Flag (int64) has 2 unique values: [0, 1]
Id (int64) has range: 1.00 - 6422.00, 0 nan values
Store_Number (int64) has range: 1.00 - 45.00, 0 nan values
Temperature (float64) has range: -2.06 - 100.14, 0 nan values
Unemployment (float64) has range: 4.08 - 14.31, 0 nan values
Weekly_Sales (int64) has range: 209986.00 - 3818686.00, 0 nan values
