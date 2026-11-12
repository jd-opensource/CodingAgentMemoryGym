# OpenMLE-fast task

Task ID: `school-student-daily-attendance@1`

Native metric: `DailyAbsenteeRateMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1245 bytes)
- `data/sample_submission.csv` (504906 bytes); columns: ["row_id", "absent_rate"]
- `data/test.csv` (551393 bytes); columns: ["row_id", "school_id", "date", "enrolled"]
- `data/train.csv` (12494005 bytes); columns: ["school_id", "date", "enrolled", "absent", "present", "released", "absent_rate"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (21546 lines)
test.csv (21546 lines)
train.csv (255585 lines)```

-> sample_submission.csv has 21545 rows and 2 columns.
Here is some information about the columns:
absent_rate (float64) has range: 0.00 - 0.44, 0 nan values
row_id (int64) has range: 0.00 - 21544.00, 0 nan values

-> test.csv has 21545 rows and 4 columns.
Here is some information about the columns:
date (int64) has range: 20190603.00 - 20190626.00, 0 nan values
enrolled (int64) has range: 26.00 - 5901.00, 0 nan values
row_id (int64) has range: 0.00 - 21544.00, 0 nan values
school_id (object) has 1580 unique values. Some example values: ['08X367', '09X505', '09X117', '09X231']

-> train.csv has 255584 rows and 7 columns.
Here is some information about the columns:
absent (int64) has range: 0.00 - 2050.00, 0 nan values
absent_rate (float64) has range: 0.00 - 0.92, 0 nan values
date (int64) has range: 20180904.00 - 20190531.00, 0 nan values
enrolled (int64) has range: 14.00 - 5955.00, 0 nan values
present (int64) has range: 1.00 - 5847.00, 0 nan values
released (int64) has range: 0.00 - 5904.00, 0 nan values
school_id (object) has 1580 unique values. Some example values: ['10X228', '17K394', '17K382', '27Q123']
