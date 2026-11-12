# OpenMLE-fast task

Task ID: `natural-gas-prices@1`

Native metric: `NaturalGasPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1117 bytes)
- `data/monthly_train.csv` (3598 bytes); columns: ["Month", "Price"]
- `data/sample_submission.csv` (7508 bytes); columns: ["Date", "Price"]
- `data/test.csv` (2821 bytes); columns: ["Date"]
- `data/train.csv` (92108 bytes); columns: ["Date", "Price"]

## Public description

```
description.txt (43 lines)
monthly_train.csv (273 lines)
sample_submission.csv (257 lines)
test.csv (257 lines)
train.csv (5697 lines)```

-> monthly_train.csv has 272 rows and 2 columns.
Here is some information about the columns:
Month (object) has 272 unique values. Some example values: ['2019-08', '1997-01', '1997-02', '1997-03']
Price (float64) has range: 1.72 - 13.42, 0 nan values

-> sample_submission.csv has 256 rows and 2 columns.
Here is some information about the columns:
Date (object) has 256 unique values. Some example values: ['2019-09-03', '2019-09-04', '2019-09-05', '2019-09-06']
Price (float64) has range: 1.29 - 13.78, 0 nan values

-> test.csv has 256 rows and 1 columns.
Here is some information about the columns:
Date (object) has 256 unique values. Some example values: ['2019-09-03', '2019-09-04', '2019-09-05', '2019-09-06']

-> train.csv has 5696 rows and 2 columns.
Here is some information about the columns:
Date (object) has 5696 unique values. Some example values: ['2019-07-08', '2019-07-09', '2019-07-10', '2019-07-11']
Price (float64) has range: 1.05 - 18.48, 0 nan values
