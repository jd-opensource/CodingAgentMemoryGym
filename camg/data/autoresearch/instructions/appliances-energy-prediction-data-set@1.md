# OpenMLE-fast task

Task ID: `appliances-energy-prediction-data-set@1`

Native metric: `ApplianceEnergyNowcastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3693 bytes)
- `data/sample_submission.csv` (44495 bytes); columns: ["row_id", "Appliances"]
- `data/test.csv` (792538 bytes); columns: ["row_id", "date", "lights", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "RH_1", "RH_2", "RH_3", "RH_4", "RH_5", "RH_6", "RH_7", "RH_8", "RH_9", "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint"]
- `data/train.csv` (3201023 bytes); columns: ["row_id", "date", "lights", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "RH_1", "RH_2", "RH_3", "RH_4", "RH_5", "RH_6", "RH_7", "RH_8", "RH_9", "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint", "Appliances"]

## Public description

```
description.txt (55 lines)
sample_submission.csv (3948 lines)
test.csv (3948 lines)
train.csv (15789 lines)```

-> sample_submission.csv has 3947 rows and 2 columns.
Here is some information about the columns:
Appliances (float64) has range: 10.00 - 800.00, 0 nan values
row_id (int64) has range: 15788.00 - 19734.00, 0 nan values

-> test.csv has 3947 rows and 27 columns.
Here is some information about the columns:
Press_mm_hg (float64) has range: 744.10 - 766.90, 0 nan values
RH_1 (float64) has range: 27.02 - 54.67, 0 nan values
RH_2 (float64) has range: 20.46 - 54.09, 0 nan values
RH_3 (float64) has range: 28.77 - 47.69, 0 nan values
RH_4 (float64) has range: 28.72 - 50.76, 0 nan values
RH_5 (float64) has range: 29.82 - 88.95, 0 nan values
RH_6 (float64) has range: 1.00 - 58.79, 0 nan values
RH_7 (float64) has range: 25.70 - 48.29, 0 nan values
RH_8 (float64) has range: 31.33 - 55.00, 0 nan values
RH_9 (float64) has range: 29.85 - 51.54, 0 nan values
RH_out (float64) has range: 24.00 - 100.00, 0 nan values
T1 (float64) has range: 20.39 - 26.26, 0 nan values
T2 (float64) has range: 17.39 - 29.86, 0 nan values
T3 (float64) has range: 22.10 - 29.24, 0 nan values
T4 (float64) has range: 19.20 - 26.20, 0 nan values
T5 (float64) has range: 19.13 - 25.80, 0 nan values
T6 (float64) has range: 1.29 - 28.29, 0 nan values
T7 (float64) has range: 19.03 - 26.00, 0 nan values
T8 (float64) has range: 21.13 - 27.23, 0 nan values
T9 (float64) has range: 19.10 - 24.50, 0 nan values
T_out (float64) has range: 1.70 - 26.10, 0 nan values
Tdewpoint (float64) has range: -1.40 - 15.50, 0 nan values
Visibility (float64) has range: 1.00 - 65.00, 0 nan values
Windspeed (float64) has range: 0.00 - 10.00, 0 nan values
date (object) has 3947 unique values. Some example values: ['27-05-2016 18:00', '30-04-2016 08:20', '30-04-2016 08:30', '30-04-2016 08:40']
lights (int64) has 4 unique values: [0, 10, 30, 20]
row_id (int64) has range: 15788.00 - 19734.00, 0 nan values

-> train.csv has 15788 rows and 28 columns.
Here is some information about the columns:
Appliances (int64) has range: 10.00 - 1080.00, 0 nan values
Press_mm_hg (float64) has range: 729.30 - 772.30, 0 nan values
RH_1 (float64) has range: 27.73 - 63.36, 0 nan values
RH_2 (float64) has range: 25.76 - 56.03, 0 nan values
RH_3 (float64) has range: 32.63 - 50.16, 0 nan values
RH_4 (float64) has range: 27.66 - 51.09, 0 nan values
RH_5 (float64) has range: 35.36 - 96.32, 0 nan values
RH_6 (float64) has range: 1.00 - 99.90, 0 nan values
RH_7 (float64) has range: 23.20 - 51.40, 0 nan values
RH_8 (float64) has range: 29.60 - 58.78, 0 nan values
RH_9 (float64) has range: 29.17 - 53.33, 0 nan values
RH_out (float64) has range: 31.00 - 100.00, 0 nan values
T1 (float64) has range: 16.79 - 24.10, 0 nan values
T2 (float64) has range: 16.10 - 24.60, 0 nan values
T3 (float64) has range: 17.20 - 27.60, 0 nan values
T4 (float64) has range: 15.10 - 23.76, 0 nan values
T5 (float64) has range: 15.33 - 22.97, 0 nan values
T6 (float64) has range: -6.07 - 21.29, 0 nan values
T7 (float64) has range: 15.39 - 23.57, 0 nan values
T8 (float64) has range: 16.31 - 25.20, 0 nan values
T9 (float64) has range: 14.89 - 23.84, 0 nan values
T_out (float64) has range: -5.00 - 19.70, 0 nan values
Tdewpoint (float64) has range: -6.60 - 11.40, 0 nan values
Visibility (float64) has range: 1.00 - 66.00, 0 nan values
Windspeed (float64) has range: 0.00 - 14.00, 0 nan values
date (object) has 15788 unique values. Some example values: ['30-04-2016 08:10', '11-01-2016 17:00', '11-01-2016 17:10', '11-01-2016 17:20']
lights (int64) has 8 unique values: [30, 40, 50, 70, 60, 10, 20, 0]
row_id (int64) has range: 0.00 - 15787.00, 0 nan values
