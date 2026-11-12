# OpenMLE-fast task

Task ID: `mental-health-and-screen-time-correlation-dataset@1`

Native metric: `MentalHealthScreenTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2368 bytes)
- `data/sample_submission.csv` (87527 bytes); columns: ["Id", "Well_Being_Score", "Stress_Level", "Mood_Rating"]
- `data/test.csv` (65331 bytes); columns: ["Id", "Date", "Daily_Screen_Time", "App_Social_Media_Time", "App_Work_Time", "App_Entertainment_Time", "Phone_Unlocks", "Sleep_Duration"]
- `data/train.csv` (286652 bytes); columns: ["Id", "Date", "Daily_Screen_Time", "App_Social_Media_Time", "App_Work_Time", "App_Entertainment_Time", "Phone_Unlocks", "Sleep_Duration", "Well_Being_Score", "Stress_Level", "Mood_Rating"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (1001 lines)
test.csv (1001 lines)
train.csv (4001 lines)```

-> sample_submission.csv has 1000 rows and 4 columns.
Here is some information about the columns:
Id (object) has 1000 unique values. Some example values: ['fff764073911bf1b0d01ab10d2c20fff', '00038032a3998d49ba3245a10dd9daff', '000868b5432419a2fe84d15782d080ac', '0081fa77b256658bd28a1f6d04b8f626']
Mood_Rating (float64) has range: 1.00 - 9.99, 0 nan values
Stress_Level (float64) has range: 1.01 - 9.99, 0 nan values
Well_Being_Score (float64) has range: 1.01 - 10.00, 0 nan values

-> test.csv has 1000 rows and 8 columns.
Here is some information about the columns:
App_Entertainment_Time (int64) has range: 14.00 - 561.00, 0 nan values
App_Social_Media_Time (int64) has range: 0.00 - 297.00, 0 nan values
App_Work_Time (int64) has range: 0.00 - 174.00, 0 nan values
Daily_Screen_Time (int64) has range: 60.00 - 600.00, 0 nan values
Date (object) has 346 unique values. Some example values: ['2023-12-08', '2024-06-27', '2023-09-28', '2024-09-03']
Id (object) has 1000 unique values. Some example values: ['fff764073911bf1b0d01ab10d2c20fff', '00038032a3998d49ba3245a10dd9daff', '000868b5432419a2fe84d15782d080ac', '0081fa77b256658bd28a1f6d04b8f626']
Phone_Unlocks (int64) has range: 10.00 - 150.00, 0 nan values
Sleep_Duration (float64) has range: 4.00 - 9.00, 0 nan values

-> train.csv has 4000 rows and 11 columns.
Here is some information about the columns:
App_Entertainment_Time (int64) has range: 19.00 - 575.00, 0 nan values
App_Social_Media_Time (int64) has range: 0.00 - 295.00, 0 nan values
App_Work_Time (int64) has range: 0.00 - 177.00, 0 nan values
Daily_Screen_Time (int64) has range: 60.00 - 600.00, 0 nan values
Date (object) has 366 unique values. Some example values: ['2024-02-19', '2024-04-04', '2024-02-20', '2024-05-27']
Id (object) has 4000 unique values. Some example values: ['fd38d19e2bd292b1fb816c7d4ad67f85', 'fd4c804206664c60d200aef3927fbfc3', 'fd6d7ac81a1a73dda2937af097b4d5e5', 'fd6fd01123de4bbb8374706f4a7d5afd']
Mood_Rating (int64) has range: 1.00 - 10.00, 0 nan values
Phone_Unlocks (int64) has range: 10.00 - 150.00, 0 nan values
Sleep_Duration (float64) has range: 4.00 - 9.00, 0 nan values
Stress_Level (int64) has range: 1.00 - 10.00, 0 nan values
Well_Being_Score (int64) has range: 1.00 - 10.00, 0 nan values
