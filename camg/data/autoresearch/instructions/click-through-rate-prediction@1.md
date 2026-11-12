# OpenMLE-fast task

Task ID: `click-through-rate-prediction@1`

Native metric: `ClickThroughRateMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2542 bytes)
- `data/sample_submission.csv` (64592 bytes); columns: ["row_id", "Clicked on Ad"]
- `data/test.csv` (289619 bytes); columns: ["row_id", "Daily Time Spent on Site", "Age", "Area Income", "Daily Internet Usage", "Ad Topic Line", "City", "Gender", "Country", "Timestamp"]
- `data/train.csv` (864770 bytes); columns: ["row_id", "Daily Time Spent on Site", "Age", "Area Income", "Daily Internet Usage", "Ad Topic Line", "City", "Gender", "Country", "Timestamp", "Clicked on Ad"]

## Public description

```
description.txt (52 lines)
sample_submission.csv (2470 lines)
test.csv (2470 lines)
train.csv (7317 lines)```

-> sample_submission.csv has 2469 rows and 2 columns.
Here is some information about the columns:
Clicked on Ad (float64) has range: 0.01 - 0.99, 0 nan values
row_id (int64) has range: 107316.00 - 109784.00, 0 nan values

-> test.csv has 2469 rows and 10 columns.
Here is some information about the columns:
Ad Topic Line (object) has 389 unique values. Some example values: ['Optional multi-state hardware', 'Sharable reciprocal project', 'Total 5thgeneration standardization', 'Function-based context-sensitive secured line']
Age (float64) has range: 19.00 - 60.00, 0 nan values
Area Income (float64) has range: 14548.06 - 79332.33, 0 nan values
City (object) has 356 unique values. Some example values: ['Wrightburgh', 'Burgessside', 'New Michael', 'East Carlos']
Country (object) has 176 unique values. Some example values: ['Burundi', 'Singapore', 'Turkey', 'Hong Kong']
Daily Internet Usage (float64) has range: 105.86 - 269.96, 0 nan values
Daily Time Spent on Site (float64) has range: 32.60 - 90.97, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Timestamp (object) has 136 unique values. Some example values: ['2016-07-03 04:11:40', '2016-07-08 03:47:41', '2016-06-21 14:32:32', '2016-07-17 01:13:56']
row_id (int64) has range: 107316.00 - 109784.00, 0 nan values

-> train.csv has 7316 rows and 11 columns.
Here is some information about the columns:
Ad Topic Line (object) has 515 unique values. Some example values: ['Cloned explicit middleware', 'Business-focused transitional solution', 'Intuitive exuding service-desk', 'Optimized upward-trending productivity']
Age (float64) has range: 19.00 - 60.00, 0 nan values
Area Income (float64) has range: 13996.50 - 79332.33, 0 nan values
City (object) has 495 unique values. Some example values: ['Hubbardmouth', 'Lisafort', 'West Brandonton', 'Stewartbury']
Clicked on Ad (int64) has 2 unique values: [0, 1]
Country (object) has 206 unique values. Some example values: ['Czech Republic', 'Australia', 'Turkey', 'Bangladesh']
Daily Internet Usage (float64) has range: 105.22 - 269.96, 0 nan values
Daily Time Spent on Site (float64) has range: 32.60 - 90.97, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Timestamp (object) has 431 unique values. Some example values: ['2016-03-11 00:05:48', '2016-04-06 11:24:21', '2016-04-04 20:01:12', '2016-04-03 21:13:46']
row_id (int64) has range: 100000.00 - 107315.00, 0 nan values
