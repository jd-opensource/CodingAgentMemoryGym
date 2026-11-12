# OpenMLE-fast task

Task ID: `cryptocurrencypricehistory@1`

Native metric: `CryptoRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2032 bytes)
- `data/sample_submission.csv` (134601 bytes); columns: ["Id", "CloseNextDay"]
- `data/test.csv` (436871 bytes); columns: ["Id", "Symbol", "Date", "Open", "High", "Low", "Close", "Volume", "Marketcap"]
- `data/train.csv` (4483402 bytes); columns: ["Id", "Symbol", "Date", "Open", "High", "Low", "Close", "Volume", "Marketcap", "CloseNextDay"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (4141 lines)
test.csv (4141 lines)
train.csv (32920 lines)```

-> sample_submission.csv has 4140 rows and 2 columns.
Here is some information about the columns:
CloseNextDay (float64) has range: 0.00 - 16407.24, 0 nan values
Id (object) has 4140 unique values. Some example values: ['XRP_20210705', 'AAVE_20210107', 'AAVE_20210108', 'AAVE_20210109']

-> test.csv has 4140 rows and 9 columns.
Here is some information about the columns:
Close (float64) has range: 0.01 - 63503.46, 0 nan values
Date (object) has 180 unique values. Some example values: ['2021-01-07', '2021-01-08', '2021-01-09', '2021-01-10']
High (float64) has range: 0.01 - 64863.10, 0 nan values
Id (object) has 4140 unique values. Some example values: ['XRP_20210705', 'AAVE_20210107', 'AAVE_20210108', 'AAVE_20210109']
Low (float64) has range: 0.01 - 62208.96, 0 nan values
Marketcap (float64) has range: 621424746.01 - 1186364044140.27, 0 nan values
Open (float64) has range: 0.01 - 63523.75, 0 nan values
Symbol (object) has 23 unique values. Some example values: ['AAVE', 'ADA', 'ATOM', 'BNB']
Volume (float64) has range: 27904470.43 - 350967941479.06, 0 nan values

-> train.csv has 32919 rows and 10 columns.
Here is some information about the columns:
Close (float64) has range: 0.00 - 36824.36, 0 nan values
CloseNextDay (float64) has range: 0.00 - 39371.04, 0 nan values
Date (object) has 2810 unique values. Some example values: ['2020-10-17', '2020-10-18', '2020-10-19', '2020-10-20']
High (float64) has range: 0.00 - 40826.50, 0 nan values
Id (object) has 32919 unique values. Some example values: ['XRP_20210106', 'AAVE_20201005', 'AAVE_20201006', 'AAVE_20201007']
Low (float64) has range: 0.00 - 33567.03, 0 nan values
Marketcap (float64) has range: 0.00 - 684671246323.65, 0 nan values
Open (float64) has range: 0.00 - 34017.35, 0 nan values
Symbol (object) has 23 unique values. Some example values: ['BTC', 'LTC', 'XRP', 'DOGE']
Volume (float64) has range: 0.00 - 125906387010.61, 0 nan values
