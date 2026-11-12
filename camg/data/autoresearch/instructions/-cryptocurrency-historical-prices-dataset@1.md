# OpenMLE-fast task

Task ID: `-cryptocurrency-historical-prices-dataset@1`

Native metric: `CryptoReturnRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2427 bytes)
- `data/sample_submission.csv` (282121 bytes); columns: ["row_id", "y"]
- `data/test.csv` (1020777 bytes); columns: ["row_id", "open", "high", "low", "close", "volume", "marketCap", "timestamp", "crypto_name", "date"]
- `data/train.csv` (10886348 bytes); columns: ["row_id", "open", "high", "low", "close", "volume", "marketCap", "timestamp", "crypto_name", "date", "y"]

## Public description

```
description.txt (57 lines)
sample_submission.csv (6944 lines)
test.csv (6944 lines)
train.csv (65576 lines)```

-> sample_submission.csv has 6943 rows and 2 columns.
Here is some information about the columns:
row_id (object) has 6943 unique values. Some example values: ['XRP-2022-09-19', 'Aave-2022-01-01', 'Aave-2022-01-02', 'Aave-2022-01-04']
y (float64) has range: -2.03 - 1.99, 0 nan values

-> test.csv has 6943 rows and 10 columns.
Here is some information about the columns:
close (float64) has range: 0.00 - 47686.81, 0 nan values
crypto_name (object) has 53 unique values. Some example values: ['Aave', 'Algorand', 'Avalanche', 'BNB']
date (object) has 131 unique values. Some example values: ['2022-01-01', '2022-01-02', '2022-01-04', '2022-01-05']
high (float64) has range: 0.00 - 48086.84, 0 nan values
low (float64) has range: 0.00 - 47115.14, 0 nan values
marketCap (float64) has range: 130465101.45 - 902104193384.61, 0 nan values
open (float64) has range: 0.00 - 47680.93, 0 nan values
row_id (object) has 6943 unique values. Some example values: ['XRP-2022-09-19', 'Aave-2022-01-01', 'Aave-2022-01-02', 'Aave-2022-01-04']
timestamp (object) has 131 unique values. Some example values: ['2022-01-01T23:59:59.999Z', '2022-01-02T23:59:59.999Z', '2022-01-04T23:59:59.999Z', '2022-01-05T23:59:59.999Z']
volume (float64) has range: 1117781.13 - 159700404396.02, 0 nan values

-> train.csv has 65575 rows and 11 columns.
Here is some information about the columns:
close (float64) has range: 0.00 - 67566.83, 0 nan values
crypto_name (object) has 53 unique values. Some example values: ['Bitcoin', 'Litecoin', 'XRP', 'Dogecoin']
date (object) has 3112 unique values. Some example values: ['2021-09-29', '2021-12-19', '2021-12-20', '2021-10-19']
high (float64) has range: 0.00 - 162188.26, 0 nan values
low (float64) has range: 0.00 - 66458.72, 0 nan values
marketCap (float64) has range: 0.00 - 1274831490851.01, 0 nan values
open (float64) has range: 0.00 - 67549.74, 0 nan values
row_id (object) has 65575 unique values. Some example values: ['XRP-2021-12-31', 'Aave-2020-10-02', 'Aave-2020-10-03', 'Aave-2020-10-04']
timestamp (object) has 3112 unique values. Some example values: ['2021-09-29T23:59:59.999Z', '2021-12-19T23:59:59.999Z', '2021-12-20T23:59:59.999Z', '2021-10-19T23:59:59.999Z']
volume (float64) has range: 0.00 - 350967941479.06, 0 nan values
y (float64) has range: -1.46 - 5.18, 0 nan values
