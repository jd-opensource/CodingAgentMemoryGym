# OpenMLE-fast task

Task ID: `netflix-vs-disney@2`

Native metric: `CorrelationForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2077 bytes)
- `data/sample_submission.csv` (13262 bytes); columns: ["Date", "Corr20"]
- `data/test.csv` (36748 bytes); columns: ["Date", "NFLX_Open", "NFLX_High", "NFLX_Low", "NFLX_Close", "NFLX_Volume", "DIS_Open", "DIS_High", "DIS_Low", "DIS_Close", "DIS_Volume"]
- `data/train.csv` (675531 bytes); columns: ["Date", "NFLX_Open", "NFLX_High", "NFLX_Low", "NFLX_Close", "NFLX_Volume", "DIS_Open", "DIS_High", "DIS_Low", "DIS_Close", "DIS_Volume", "Corr20"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (432 lines)
test.csv (432 lines)
train.csv (5190 lines)```

-> sample_submission.csv has 431 rows and 2 columns.
Here is some information about the columns:
Corr20 (float64) has range: -0.99 - 0.98, 0 nan values
Date (object) has 431 unique values. Some example values: ['2024-09-19', '2023-01-03', '2023-01-04', '2023-01-05']

-> test.csv has 431 rows and 11 columns.
Here is some information about the columns:
DIS_Close (float64) has range: 79.32 - 122.82, 0 nan values
DIS_High (float64) has range: 79.79 - 123.74, 0 nan values
DIS_Low (float64) has range: 78.73 - 121.20, 0 nan values
DIS_Open (float64) has range: 79.10 - 122.27, 0 nan values
DIS_Volume (float64) has range: 5029969.00 - 60558410.00, 0 nan values
Date (object) has 431 unique values. Some example values: ['2024-09-19', '2023-01-03', '2023-01-04', '2023-01-05']
NFLX_Close (float64) has range: 292.76 - 706.91, 0 nan values
NFLX_High (float64) has range: 297.45 - 715.66, 0 nan values
NFLX_Low (float64) has range: 285.33 - 698.37, 0 nan values
NFLX_Open (float64) has range: 287.34 - 707.55, 0 nan values
NFLX_Volume (float64) has range: 1354154.00 - 28430339.00, 0 nan values

-> train.csv has 5189 rows and 12 columns.
Here is some information about the columns:
Corr20 (float64) has range: -0.79 - 0.94, 0 nan values
DIS_Close (float64) has range: 13.77 - 201.91, 0 nan values
DIS_High (float64) has range: 14.10 - 203.02, 0 nan values
DIS_Low (float64) has range: 13.48 - 195.40, 0 nan values
DIS_Open (float64) has range: 13.80 - 200.19, 0 nan values
DIS_Volume (float64) has range: 1487900.00 - 116625000.00, 0 nan values
Date (object) has 5189 unique values. Some example values: ['2022-12-30', '2002-05-23', '2002-05-24', '2002-05-28']
NFLX_Close (float64) has range: 0.37 - 691.69, 0 nan values
NFLX_High (float64) has range: 0.41 - 700.99, 0 nan values
NFLX_Low (float64) has range: 0.35 - 686.09, 0 nan values
NFLX_Open (float64) has range: 0.38 - 692.35, 0 nan values
NFLX_Volume (float64) has range: 38622.00 - 323414000.00, 0 nan values
