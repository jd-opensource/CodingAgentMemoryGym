# OpenMLE-fast task

Task ID: `cinema-ticket@1`

Native metric: `CinemaTicketRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1403 bytes)
- `data/sample_submission.csv` (423410 bytes); columns: ["row_id", "ticket_use"]
- `data/test.csv` (679459 bytes); columns: ["row_id", "film_code", "cinema_code", "date", "show_time", "ticket_price"]
- `data/train.csv` (5491557 bytes); columns: ["row_id", "film_code", "cinema_code", "date", "show_time", "ticket_price", "ticket_use"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (17855 lines)
test.csv (17855 lines)
train.csv (124565 lines)```

-> sample_submission.csv has 17854 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 0.00 - 17853.00, 0 nan values
ticket_use (float64) has range: 0.00 - 27513.56, 0 nan values

-> test.csv has 17854 rows and 6 columns.
Here is some information about the columns:
cinema_code (int64) has range: 32.00 - 566.00, 0 nan values
date (object) has 28 unique values. Some example values: ['2018-10-23', '2018-10-16', '2018-10-26', '2018-10-18']
film_code (int64) has range: 1481.00 - 1589.00, 0 nan values
row_id (int64) has range: 0.00 - 17853.00, 0 nan values
show_time (int64) has range: 1.00 - 40.00, 0 nan values
ticket_price (float64) has range: 4571.43 - 500000.00, 0 nan values

-> train.csv has 124564 rows and 7 columns.
Here is some information about the columns:
cinema_code (int64) has range: 32.00 - 637.00, 0 nan values
date (object) has 206 unique values. Some example values: ['2018-05-15', '2018-05-08', '2018-05-11', '2018-05-10']
film_code (int64) has range: 1471.00 - 1576.00, 0 nan values
row_id (int64) has range: 0.00 - 124563.00, 0 nan values
show_time (int64) has range: 1.00 - 60.00, 0 nan values
ticket_price (float64) has range: 483.87 - 700000.00, 0 nan values
ticket_use (float64) has range: 0.00 - 8499.00, 0 nan values
