# OpenMLE-fast task

Task ID: `cooling-chamber-energy-consumption@1`

Native metric: `CoolingChamberEnergyMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3751 bytes)
- `data/sample_submission.csv` (87712 bytes); columns: ["sample_id", "target_kwh_15m"]
- `data/test.csv` (885220 bytes); columns: ["sample_id", "ts", "hour_of_day", "day_of_week", "is_weekend", "month", "cons_prev_15m", "cons_prev_30m", "cons_prev_60m", "cons_prev_4h", "cons_prev_24h", "temp_mean_prev_15m", "temp_min_prev_15m", "temp_max_prev_15m", "temp_mean_prev_1h", "temp_min_prev_1h", "temp_max_prev_1h", "SP_temp_current", "H_band_current", "SP_temp_delta_1h", "H_band_delta_1h", "price_prev_1h", "price_current_bin", "price_target_bin"]
- `data/train.csv` (3781271 bytes); columns: ["sample_id", "ts", "hour_of_day", "day_of_week", "is_weekend", "month", "cons_prev_15m", "cons_prev_30m", "cons_prev_60m", "cons_prev_4h", "cons_prev_24h", "temp_mean_prev_15m", "temp_min_prev_15m", "temp_max_prev_15m", "temp_mean_prev_1h", "temp_min_prev_1h", "temp_max_prev_1h", "SP_temp_current", "H_band_current", "SP_temp_delta_1h", "H_band_delta_1h", "price_prev_1h", "price_current_bin", "price_target_bin", "target_kwh_15m"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (3493 lines)
test.csv (3493 lines)
train.csv (13973 lines)```

-> sample_submission.csv has 3492 rows and 2 columns.
Here is some information about the columns:
sample_id (int64) has range: 13972.00 - 17463.00, 0 nan values
target_kwh_15m (float64) has range: 0.00 - 14.97, 0 nan values

-> test.csv has 3492 rows and 24 columns.
Here is some information about the columns:
H_band_current (float64) has 1 unique values: [2.5]
H_band_delta_1h (float64) has 1 unique values: [0.0]
SP_temp_current (float64) has 1 unique values: [-18.3]
SP_temp_delta_1h (float64) has 1 unique values: [0.0]
cons_prev_15m (float64) has range: 0.00 - 8.77, 0 nan values
cons_prev_24h (float64) has range: 84.21 - 168.74, 0 nan values
cons_prev_30m (float64) has range: 0.22 - 13.23, 0 nan values
cons_prev_4h (float64) has range: 3.38 - 52.18, 0 nan values
cons_prev_60m (float64) has range: 0.60 - 22.71, 0 nan values
day_of_week (int64) has 7 unique values: [4, 5, 6, 0, 1, 2, 3]
hour_of_day (int64) has range: 0.00 - 23.00, 0 nan values
is_weekend (int64) has 2 unique values: [0, 1]
month (int64) has 2 unique values: [3, 4]
price_current_bin (float64) has range: -0.00 - 0.20, 0 nan values
price_prev_1h (float64) has range: -0.00 - 0.20, 0 nan values
price_target_bin (float64) has range: -0.00 - 0.20, 0 nan values
sample_id (int64) has range: 13972.00 - 17463.00, 0 nan values
temp_max_prev_15m (float64) has range: -18.50 - -15.40, 0 nan values
temp_max_prev_1h (float64) has range: -17.90 - -15.40, 0 nan values
temp_mean_prev_15m (float64) has range: -18.59 - -15.53, 0 nan values
temp_mean_prev_1h (float64) has range: -18.27 - -15.77, 0 nan values
temp_min_prev_15m (float64) has range: -18.60 - -15.70, 0 nan values
temp_min_prev_1h (float64) has range: -18.60 - -15.90, 0 nan values
ts (object) has 3492 unique values. Some example values: ['2025-04-14 01:15:00', '2025-03-07 06:45:00', '2025-03-07 07:00:00', '2025-03-07 07:15:00']

-> train.csv has 13972 rows and 25 columns.
Here is some information about the columns:
H_band_current (float64) has 2 unique values: [2.5, 0.2]
H_band_delta_1h (float64) has 3 unique values: [0.0, -2.3, 2.3]
SP_temp_current (float64) has 3 unique values: [-18.3, -20.8, -15.8]
SP_temp_delta_1h (float64) has 5 unique values: [0.0, -2.5, 2.5, -5.0, 5.0]
cons_prev_15m (float64) has range: -0.65 - 9.80, 0 nan values
cons_prev_24h (float64) has range: 84.86 - 177151.96, 0 nan values
cons_prev_30m (float64) has range: 0.06 - 14.43, 0 nan values
cons_prev_4h (float64) has range: 3.21 - 63.78, 0 nan values
cons_prev_60m (float64) has range: 0.33 - 23.37, 0 nan values
day_of_week (int64) has 7 unique values: [2, 3, 4, 5, 6, 0, 1]
hour_of_day (int64) has range: 0.00 - 23.00, 0 nan values
is_weekend (int64) has 2 unique values: [0, 1]
month (int64) has 6 unique values: [10, 11, 12, 1, 2, 3]
price_current_bin (float64) has range: -0.00 - 0.24, 0 nan values
price_prev_1h (float64) has range: -0.00 - 0.24, 0 nan values
price_target_bin (float64) has range: -0.00 - 0.24, 0 nan values
sample_id (int64) has range: 0.00 - 13971.00, 0 nan values
target_kwh_15m (float64) has range: 0.00 - 6.54, 0 nan values
temp_max_prev_15m (float64) has range: -19.20 - -11.90, 0 nan values
temp_max_prev_1h (float64) has range: -18.40 - -11.90, 0 nan values
temp_mean_prev_15m (float64) has range: -19.49 - -11.90, 0 nan values
temp_mean_prev_1h (float64) has range: -19.05 - -11.90, 0 nan values
temp_min_prev_15m (float64) has range: -19.60 - -11.90, 0 nan values
temp_min_prev_1h (float64) has range: -19.60 - -11.90, 0 nan values
ts (object) has 13972 unique values. Some example values: ['2025-03-07 06:30:00', '2024-10-02 02:00:00', '2024-10-02 02:15:00', '2024-10-02 02:30:00']
