# OpenMLE-fast task

Task ID: `cooling-chamber-energy-consumption@2`

Native metric: `CoolingChamberMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2345 bytes)
- `data/extra_unlabeled.csv` (15221780 bytes); columns: ["timestamp", "active_energy", "minute_energy", "temperature", "SP_temp", "H_band", "price"]
- `data/sample_submission.csv` (111183 bytes); columns: ["row_id", "status"]
- `data/test.csv` (895115 bytes); columns: ["row_id", "timestamp", "active_energy", "minute_energy", "temperature", "SP_temp", "H_band", "price"]
- `data/train.csv` (3780388 bytes); columns: ["row_id", "timestamp", "active_energy", "minute_energy", "temperature", "SP_temp", "H_band", "price", "status"]

## Public description

```
description.txt (44 lines)
extra_unlabeled.csv (220854 lines)
sample_submission.csv (11958 lines)
test.csv (11958 lines)
train.csv (47830 lines)```

-> extra_unlabeled.csv has 220853 rows and 7 columns.
Here is some information about the columns:
H_band (float64) has 4 unique values: [2.5, 0.0, 1.25, 0.2]
SP_temp (float64) has 5 unique values: [-18.3, -0.3, -17.05, -20.8, -15.8]
active_energy (float64) has range: 0.00 - 177350.87, 0 nan values
minute_energy (float64) has range: 0.00 - 177043.68, 0 nan values
price (float64) has range: -0.00 - 0.24, 0 nan values
temperature (float64) has range: -19.60 - -0.30, 0 nan values
timestamp (object) has 220853 unique values. Some example values: ['2025-03-03 12:30:00', '2024-10-01 02:00:00', '2024-10-01 02:01:00', '2024-10-01 02:02:00']

-> sample_submission.csv has 11957 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 0.00 - 11956.00, 0 nan values
status (float64) has 3 unique values: [0.0, 0.0625, 1.0]

-> test.csv has 11957 rows and 8 columns.
Here is some information about the columns:
H_band (float64) has 1 unique values: [2.5]
SP_temp (float64) has 1 unique values: [-18.3]
active_energy (float64) has range: 181484.48 - 182648.00, 0 nan values
minute_energy (float64) has range: 0.00 - 4.58, 0 nan values
price (float64) has range: -0.00 - 0.17, 0 nan values
row_id (int64) has range: 0.00 - 11956.00, 0 nan values
temperature (float64) has range: -18.60 - -15.40, 0 nan values
timestamp (object) has 11957 unique values. Some example values: ['2025-04-14 01:59:00', '2025-04-05 18:43:00', '2025-04-05 18:44:00', '2025-04-05 18:45:00']

-> train.csv has 47829 rows and 9 columns.
Here is some information about the columns:
H_band (float64) has 1 unique values: [2.5]
SP_temp (float64) has 1 unique values: [-18.3]
active_energy (float64) has range: 0.00 - 181484.48, 0 nan values
minute_energy (float64) has range: 0.00 - 177350.98, 0 nan values
price (float64) has range: -0.01 - 0.20, 0 nan values
row_id (int64) has range: 0.00 - 47828.00, 0 nan values
status (float64) has 3 unique values: [0.0, 1.0, 0.0625]
temperature (float64) has range: -18.50 - -15.50, 0 nan values
timestamp (object) has 47829 unique values. Some example values: ['2025-04-05 18:42:00', '2025-03-03 12:34:00', '2025-03-03 12:35:00', '2025-03-03 12:36:00']
