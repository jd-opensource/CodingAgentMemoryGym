# OpenMLE-fast task

Task ID: `phone-classification-dataset@1`

Native metric: `PhonePriceRangeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2730 bytes)
- `data/sample_submission.csv` (3248 bytes); columns: ["id", "price_range"]
- `data/test.csv` (31956 bytes); columns: ["id", "battery_power", "blue", "clock_speed", "dual_sim", "fc", "four_g", "int_memory", "m_dep", "mobile_wt", "n_cores", "pc", "px_height", "px_width", "ram", "sc_h", "sc_w", "talk_time", "three_g", "touch_screen", "wifi"]
- `data/train.csv` (98500 bytes); columns: ["id", "battery_power", "blue", "clock_speed", "dual_sim", "fc", "four_g", "int_memory", "m_dep", "mobile_wt", "n_cores", "pc", "px_height", "px_width", "ram", "sc_h", "sc_w", "talk_time", "three_g", "touch_screen", "wifi", "price_range"]

## Public description

```
description.txt (68 lines)
sample_submission.csv (501 lines)
test.csv (501 lines)
train.csv (1501 lines)```

-> sample_submission.csv has 500 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 1998.00, 0 nan values
price_range (int64) has 4 unique values: [0, 3, 2, 1]

-> test.csv has 500 rows and 21 columns.
Here is some information about the columns:
battery_power (int64) has range: 501.00 - 1996.00, 0 nan values
blue (int64) has 2 unique values: [1, 0]
clock_speed (float64) has range: 0.50 - 3.00, 0 nan values
dual_sim (int64) has 2 unique values: [1, 0]
fc (int64) has range: 0.00 - 18.00, 0 nan values
four_g (int64) has 2 unique values: [1, 0]
id (int64) has range: 1.00 - 1998.00, 0 nan values
int_memory (int64) has range: 2.00 - 64.00, 0 nan values
m_dep (float64) has range: 0.10 - 1.00, 0 nan values
mobile_wt (int64) has range: 80.00 - 200.00, 0 nan values
n_cores (int64) has 8 unique values: [3, 7, 8, 4, 2, 5, 6, 1]
pc (int64) has range: 0.00 - 20.00, 0 nan values
px_height (int64) has range: 0.00 - 1920.00, 0 nan values
px_width (int64) has range: 500.00 - 1996.00, 0 nan values
ram (int64) has range: 265.00 - 3990.00, 0 nan values
sc_h (int64) has range: 5.00 - 19.00, 0 nan values
sc_w (int64) has range: 0.00 - 18.00, 0 nan values
talk_time (int64) has range: 2.00 - 20.00, 0 nan values
three_g (int64) has 2 unique values: [1, 0]
touch_screen (int64) has 2 unique values: [1, 0]
wifi (int64) has 2 unique values: [0, 1]

-> train.csv has 1500 rows and 22 columns.
Here is some information about the columns:
battery_power (int64) has range: 502.00 - 1998.00, 0 nan values
blue (int64) has 2 unique values: [1, 0]
clock_speed (float64) has range: 0.50 - 3.00, 0 nan values
dual_sim (int64) has 2 unique values: [1, 0]
fc (int64) has range: 0.00 - 19.00, 0 nan values
four_g (int64) has 2 unique values: [1, 0]
id (int64) has range: 0.00 - 1999.00, 0 nan values
int_memory (int64) has range: 2.00 - 64.00, 0 nan values
m_dep (float64) has range: 0.10 - 1.00, 0 nan values
mobile_wt (int64) has range: 80.00 - 200.00, 0 nan values
n_cores (int64) has 8 unique values: [1, 7, 3, 2, 5, 6, 4, 8]
pc (int64) has range: 0.00 - 20.00, 0 nan values
price_range (int64) has 4 unique values: [2, 3, 1, 0]
px_height (int64) has range: 0.00 - 1960.00, 0 nan values
px_width (int64) has range: 500.00 - 1998.00, 0 nan values
ram (int64) has range: 256.00 - 3998.00, 0 nan values
sc_h (int64) has range: 5.00 - 19.00, 0 nan values
sc_w (int64) has range: 0.00 - 18.00, 0 nan values
talk_time (int64) has range: 2.00 - 20.00, 0 nan values
three_g (int64) has 2 unique values: [1, 0]
touch_screen (int64) has 2 unique values: [0, 1]
wifi (int64) has 2 unique values: [1, 0]
