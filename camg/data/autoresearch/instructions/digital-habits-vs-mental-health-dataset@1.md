# OpenMLE-fast task

Task ID: `digital-habits-vs-mental-health-dataset@1`

Native metric: `DigitalHabitsMentalHealthMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1504 bytes)
- `data/sample_submission.csv` (284323 bytes); columns: ["id", "stress_level", "mood_score"]
- `data/test.csv` (480955 bytes); columns: ["id", "screen_time_hours", "social_media_platforms_used", "hours_on_TikTok", "sleep_hours"]
- `data/train.csv` (2292302 bytes); columns: ["id", "screen_time_hours", "social_media_platforms_used", "hours_on_TikTok", "sleep_hours", "stress_level", "mood_score"]

## Public description

```
description.txt (34 lines)
sample_submission.csv (19996 lines)
test.csv (19996 lines)
train.csv (80006 lines)```

-> sample_submission.csv has 19995 rows and 3 columns.
Here is some information about the columns:
id (object) has 19995 unique values. Some example values: ['id_099998', 'id_000003', 'id_000010', 'id_000019']
mood_score (int64) has 9 unique values: [2, 5, 10, 3, 9, 4, 8, 6, 7]
stress_level (int64) has range: 1.00 - 10.00, 0 nan values

-> test.csv has 19995 rows and 5 columns.
Here is some information about the columns:
hours_on_TikTok (float64) has range: 0.20 - 7.20, 0 nan values
id (object) has 19995 unique values. Some example values: ['id_099998', 'id_000003', 'id_000010', 'id_000019']
screen_time_hours (float64) has range: 1.00 - 12.00, 0 nan values
sleep_hours (float64) has range: 3.00 - 10.00, 0 nan values
social_media_platforms_used (int64) has 5 unique values: [3, 4, 5, 1, 2]

-> train.csv has 80005 rows and 7 columns.
Here is some information about the columns:
hours_on_TikTok (float64) has range: 0.20 - 7.20, 0 nan values
id (object) has 80005 unique values. Some example values: ['id_099999', 'id_000000', 'id_000001', 'id_000002']
mood_score (int64) has 9 unique values: [5, 8, 10, 9, 7, 6, 4, 3, 2]
screen_time_hours (float64) has range: 1.00 - 12.00, 0 nan values
sleep_hours (float64) has range: 3.00 - 10.00, 0 nan values
social_media_platforms_used (int64) has 5 unique values: [2, 5, 4, 3, 1]
stress_level (int64) has range: 1.00 - 10.00, 0 nan values
