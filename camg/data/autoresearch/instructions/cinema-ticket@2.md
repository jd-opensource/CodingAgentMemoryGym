# OpenMLE-fast task

Task ID: `cinema-ticket@2`

Native metric: `CinemaTicketRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3162 bytes)
- `data/sample_submission.csv` (195576 bytes); columns: ["row_id", "ticket_use"]
- `data/test.csv` (579443 bytes); columns: ["row_id", "cinema_code", "date", "n_shows", "n_films", "n_morning_shows", "n_afternoon_shows", "n_evening_shows", "price_mean", "price_median", "price_std", "price_min", "price_max", "dow", "dom", "weekofyear", "month", "quarter", "is_weekend"]
- `data/train.csv` (4459302 bytes); columns: ["row_id", "cinema_code", "date", "n_shows", "n_films", "n_morning_shows", "n_afternoon_shows", "n_evening_shows", "price_mean", "price_median", "price_std", "price_min", "price_max", "dow", "dom", "weekofyear", "month", "quarter", "is_weekend", "ticket_use"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (5395 lines)
test.csv (5395 lines)
train.csv (39492 lines)```

-> sample_submission.csv has 5394 rows and 2 columns.
Here is some information about the columns:
row_id (object) has 5394 unique values. Some example values: ['cin565_2018-11-04', 'cin32_2018-10-08', 'cin33_2018-10-08', 'cin34_2018-10-08']
ticket_use (float64) has range: 0.00 - 19219.02, 0 nan values

-> test.csv has 5394 rows and 19 columns.
Here is some information about the columns:
cinema_code (int64) has range: 32.00 - 566.00, 0 nan values
date (object) has 28 unique values. Some example values: ['2018-10-16', '2018-10-18', '2018-10-09', '2018-10-19']
dom (int64) has range: 1.00 - 31.00, 0 nan values
dow (int64) has 7 unique values: [0, 1, 2, 3, 4, 5, 6]
is_weekend (int64) has 2 unique values: [0, 1]
month (int64) has 2 unique values: [10, 11]
n_afternoon_shows (int64) has 8 unique values: [0, 3, 2, 4, 1, 5, 6, 7]
n_evening_shows (int64) has range: 0.00 - 9.00, 0 nan values
n_films (int64) has range: 1.00 - 12.00, 0 nan values
n_morning_shows (int64) has range: 0.00 - 10.00, 0 nan values
n_shows (int64) has range: 1.00 - 12.00, 0 nan values
price_max (float64) has range: 4571.43 - 500000.00, 0 nan values
price_mean (float64) has range: 4571.43 - 150000.00, 0 nan values
price_median (float64) has range: 4571.43 - 150000.00, 0 nan values
price_min (float64) has range: 4571.43 - 150000.00, 0 nan values
price_std (float64) has range: 0.00 - 130738.87, 0 nan values
quarter (int64) has 1 unique values: [4]
row_id (object) has 5394 unique values. Some example values: ['cin565_2018-11-04', 'cin32_2018-10-08', 'cin33_2018-10-08', 'cin34_2018-10-08']
weekofyear (int64) has 4 unique values: [41, 42, 43, 44]

-> train.csv has 39491 rows and 20 columns.
Here is some information about the columns:
cinema_code (int64) has range: 32.00 - 637.00, 0 nan values
date (object) has 206 unique values. Some example values: ['2018-09-04', '2018-08-28', '2018-07-24', '2018-07-03']
dom (int64) has range: 1.00 - 31.00, 0 nan values
dow (int64) has 7 unique values: [2, 4, 3, 5, 6, 0, 1]
is_weekend (int64) has 2 unique values: [0, 1]
month (int64) has 9 unique values: [2, 3, 4, 5, 6, 7, 8, 9, 10]
n_afternoon_shows (int64) has range: 0.00 - 10.00, 0 nan values
n_evening_shows (int64) has range: 0.00 - 12.00, 0 nan values
n_films (int64) has range: 1.00 - 16.00, 0 nan values
n_morning_shows (int64) has range: 0.00 - 13.00, 0 nan values
n_shows (int64) has range: 1.00 - 16.00, 0 nan values
price_max (float64) has range: 2500.00 - 700000.00, 0 nan values
price_mean (float64) has range: 2500.00 - 700000.00, 0 nan values
price_median (float64) has range: 2500.00 - 700000.00, 0 nan values
price_min (float64) has range: 483.87 - 700000.00, 0 nan values
price_std (float64) has range: 0.00 - 140378.64, 0 nan values
quarter (int64) has 4 unique values: [1, 2, 3, 4]
row_id (object) has 39491 unique values. Some example values: ['cin561_2018-10-07', 'cin448_2018-02-21', 'cin518_2018-02-23', 'cin490_2018-10-07']
ticket_use (float64) has range: 0.00 - 15845.00, 0 nan values
weekofyear (int64) has range: 8.00 - 40.00, 0 nan values
