# OpenMLE-fast task

Task ID: `netflix-stock-price-data-set-20022022@1`

Native metric: `NetflixNextDayReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1464 bytes)
- `data/sample_submission.csv` (8864 bytes); columns: ["row_id", "target"]
- `data/test.csv` (23004 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Adj_Close", "Volume"]
- `data/train.csv` (386739 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Adj_Close", "Volume", "target"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (358 lines)
test.csv (358 lines)
train.csv (4686 lines)```

-> sample_submission.csv has 357 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 0.00 - 356.00, 0 nan values
target (float64) has range: -0.12 - 0.14, 0 nan values

-> test.csv has 357 rows and 7 columns.
Here is some information about the columns:
Adj_Close (float64) has range: 166.37 - 691.69, 0 nan values
Date (object) has 357 unique values. Some example values: ['2022-06-02', '2021-01-04', '2021-01-05', '2021-01-06']
High (float64) has range: 177.58 - 700.99, 0 nan values
Low (float64) has range: 162.71 - 686.09, 0 nan values
Open (float64) has range: 163.96 - 692.35, 0 nan values
Volume (int64) has range: 1287200.00 - 133387500.00, 0 nan values
row_id (int64) has range: 0.00 - 356.00, 0 nan values

-> train.csv has 4685 rows and 8 columns.
Here is some information about the columns:
Adj_Close (float64) has range: 0.37 - 556.55, 0 nan values
Date (object) has 4685 unique values. Some example values: ['2020-12-30', '2002-05-23', '2002-05-24', '2002-05-28']
High (float64) has range: 0.41 - 575.37, 0 nan values
Low (float64) has range: 0.35 - 541.00, 0 nan values
Open (float64) has range: 0.38 - 567.98, 0 nan values
Volume (int64) has range: 285600.00 - 323414000.00, 0 nan values
row_id (int64) has range: 0.00 - 4684.00, 0 nan values
target (float64) has range: -0.53 - 0.35, 0 nan values
