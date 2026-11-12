# OpenMLE-fast task

Task ID: `car-consume@1`

Native metric: `CarFuelConsumptionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1652 bytes)
- `data/sample_submission.csv` (2139 bytes); columns: ["id", "consume"]
- `data/test.csv` (3851 bytes); columns: ["id", "distance", "speed", "temp_inside", "temp_outside", "gas_type", "AC", "rain", "sun", "specials"]
- `data/train.csv` (12503 bytes); columns: ["id", "distance", "speed", "temp_inside", "temp_outside", "gas_type", "AC", "rain", "sun", "specials", "consume"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (98 lines)
test.csv (98 lines)
train.csv (292 lines)```

-> sample_submission.csv has 97 rows and 2 columns.
Here is some information about the columns:
consume (float64) has range: 3.37 - 11.98, 0 nan values
id (int64) has range: 3.00 - 387.00, 0 nan values

-> test.csv has 97 rows and 10 columns.
Here is some information about the columns:
AC (int64) has 2 unique values: [1, 0]
distance (float64) has range: 1.70 - 216.10, 0 nan values
gas_type (object) has 2 unique values: ['E10', 'SP98']
id (int64) has range: 3.00 - 387.00, 0 nan values
rain (int64) has 2 unique values: [0, 1]
specials (object) has 10 unique values. Some example values: ['none', 'rain', 'sun', 'AC rain']
speed (float64) has range: 14.00 - 90.00, 0 nan values
sun (int64) has 2 unique values: [1, 0]
temp_inside (float64) has range: 20.00 - 25.50, 0 nan values
temp_outside (float64) has range: 0.00 - 30.00, 0 nan values

-> train.csv has 291 rows and 11 columns.
Here is some information about the columns:
AC (int64) has 2 unique values: [0, 1]
consume (float64) has range: 3.30 - 12.20, 0 nan values
distance (float64) has range: 1.30 - 211.00, 0 nan values
gas_type (object) has 2 unique values: ['E10', 'SP98']
id (int64) has range: 1.00 - 388.00, 0 nan values
rain (int64) has 2 unique values: [0, 1]
specials (object) has 11 unique values. Some example values: ['none', 'rain', 'sun', 'AC rain']
speed (float64) has range: 16.00 - 87.00, 0 nan values
sun (int64) has 2 unique values: [0, 1]
temp_inside (float64) has range: 19.00 - 25.50, 0 nan values
temp_outside (float64) has range: -5.00 - 31.00, 0 nan values
