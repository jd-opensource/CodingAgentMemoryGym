# OpenMLE-fast task

Task ID: `task-turtles-vs-sprint-hares-work-style-dataset@2`

Native metric: `WorkQualityOrdinalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2384 bytes)
- `data/sample_submission.csv` (949 bytes); columns: ["row_id", "task_quality_score"]
- `data/test.csv` (5453 bytes); columns: ["developer_id", "task_complexity", "task_start_time", "task_deadline_time", "start_delay_min", "focus_rating", "distractions_count", "coffee_intake_mg", "row_id"]
- `data/train.csv` (17700 bytes); columns: ["developer_id", "task_complexity", "task_start_time", "task_deadline_time", "start_delay_min", "focus_rating", "distractions_count", "coffee_intake_mg", "task_quality_score", "row_id"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (72 lines)
test.csv (72 lines)
train.csv (229 lines)```

-> sample_submission.csv has 71 rows and 2 columns.
Here is some information about the columns:
row_id (object) has 71 unique values. Some example values: ['ROW_000073', 'ROW_000299', 'ROW_000137', 'ROW_000240']
task_quality_score (int64) has 1 unique values: [5]

-> test.csv has 71 rows and 9 columns.
Here is some information about the columns:
coffee_intake_mg (int64) has range: 6.00 - 597.00, 0 nan values
developer_id (object) has 30 unique values. Some example values: ['DEV028', 'DEV015', 'DEV023', 'DEV005']
distractions_count (int64) has 8 unique values: [7, 3, 4, 2, 1, 0, 6, 5]
focus_rating (int64) has range: 1.00 - 10.00, 0 nan values
row_id (object) has 71 unique values. Some example values: ['ROW_000073', 'ROW_000299', 'ROW_000137', 'ROW_000240']
start_delay_min (int64) has range: 1.00 - 288.00, 0 nan values
task_complexity (object) has 3 unique values: ['high', 'medium', 'low']
task_deadline_time (object) has 71 unique values. Some example values: ['2025-06-28 02:39:36', '2025-06-29 21:04:18', '2025-06-20 20:21:47', '2025-06-21 12:29:55']
task_start_time (object) has 71 unique values. Some example values: ['2025-06-27 17:46:36', '2025-06-29 17:36:18', '2025-06-20 15:03:47', '2025-06-21 06:38:55']

-> train.csv has 228 rows and 10 columns.
Here is some information about the columns:
coffee_intake_mg (int64) has range: 6.00 - 600.00, 0 nan values
developer_id (object) has 30 unique values. Some example values: ['DEV028', 'DEV015', 'DEV007', 'DEV012']
distractions_count (int64) has 9 unique values: [1, 3, 0, 5, 6, 4, 2, 10, 7]
focus_rating (int64) has 9 unique values: [8, 10, 5, 4, 7, 9, 6, 3, 2]
row_id (object) has 228 unique values. Some example values: ['ROW_000061', 'ROW_000064', 'ROW_000123', 'ROW_000223']
start_delay_min (int64) has range: 1.00 - 300.00, 0 nan values
task_complexity (object) has 3 unique values: ['high', 'low', 'medium']
task_deadline_time (object) has 228 unique values. Some example values: ['2025-06-08 07:52:43', '2025-06-14 01:10:48', '2025-06-19 19:57:58', '2025-06-12 00:14:00']
task_quality_score (int64) has range: 1.00 - 10.00, 0 nan values
task_start_time (object) has 228 unique values. Some example values: ['2025-06-07 23:59:43', '2025-06-13 19:33:48', '2025-06-19 17:54:58', '2025-06-11 17:32:00']
