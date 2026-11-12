# OpenMLE-fast task

Task ID: `yahoo-finance-dataset-2018-2023@1`

Native metric: `OHLCVForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1344 bytes)
- `data/sample_submission.csv` (26153 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]
- `data/test.csv` (2777 bytes); columns: ["Date"]
- `data/train.csv` (57017 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (253 lines)
test.csv (253 lines)
train.csv (1007 lines)```

-> sample_submission.csv has 252 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 27021.78 - 27728.60, 0 nan values
Date (object) has 252 unique values. Some example values: ['2022-04-28', '2022-04-29', '2022-05-02', '2022-05-03']
High (float64) has range: 27223.89 - 27855.24, 0 nan values
Low (float64) has range: 26873.55 - 27568.97, 0 nan values
Open (float64) has range: 27079.18 - 27771.88, 0 nan values
Volume (float64) has range: 322741619.77 - 368049426.46, 0 nan values

-> test.csv has 252 rows and 1 columns.
Here is some information about the columns:
Date (object) has 252 unique values. Some example values: ['2022-04-28', '2022-04-29', '2022-05-02', '2022-05-03']

-> train.csv has 1006 rows and 6 columns.
Here is some information about the columns:
Close (float64) has range: 18591.93 - 36799.65, 0 nan values
Date (object) has 1006 unique values. Some example values: ['2022-04-27', '2018-05-01', '2018-05-02', '2018-05-03']
High (float64) has range: 19121.01 - 36952.65, 0 nan values
Low (float64) has range: 18213.65 - 36636.00, 0 nan values
Open (float64) has range: 19028.36 - 36722.60, 0 nan values
Volume (int64) has range: 86150000.00 - 915990000.00, 0 nan values
