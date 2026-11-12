# OpenMLE-fast task

Task ID: `fitness-track-daily-activity-dataset@1`

Native metric: `NextDayStepGoalMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1085 bytes)
- `data/sample_submission.csv` (1877 bytes); columns: ["id", "reached_10k_next_day"]
- `data/test.csv` (45800 bytes); columns: ["id", "user_id", "Total_Distance_lag1", "Total_Distance_lag2", "Total_Distance_lag3", "Tracker_Distance_lag1", "Tracker_Distance_lag2", "Tracker_Distance_lag3", "Logged_Activities_Distance_lag1", "Logged_Activities_Distance_lag2", "Logged_Activities_Distance_lag3", "Very_Active_Distance_lag1", "Very_Active_Distance_lag2", "Very_Active_Distance_lag3", "Moderately_Active_Distance_lag1", "Moderately_Active_Distance_lag2", "Moderately_Active_Distance_lag3", "Light_Active_Distance_lag1", "Light_Active_Distance_lag2", "Light_Active_Distance_lag3", "Sedentary_Active_Distance_lag1", "Sedentary_Active_Distance_lag2", "Sedentary_Active_Distance_lag3", "Very_Active_Minutes_lag1", "Very_Active_Minutes_lag2", "Very_Active_Minutes_lag3", "Fairly_Active_Minutes_lag1", "Fairly_Active_Minutes_lag2", "Fairly_Active_Minutes_lag3", "Lightly_Active_Minutes_lag1", "Lightly_Active_Minutes_lag2", "Lightly_Active_Minutes_lag3", "Sedentary_Minutes_lag1", "Sedentary_Minutes_lag2", "Sedentary_Minutes_lag3", "Steps_lag1", "Steps_lag2", "Steps_lag3", "Calories_Burned_lag1", "Calories_Burned_lag2", "Calories_Burned_lag3", "target_weekday", "target_is_weekend"]
- `data/train.csv` (209825 bytes); columns: ["id", "user_id", "Total_Distance_lag1", "Total_Distance_lag2", "Total_Distance_lag3", "Tracker_Distance_lag1", "Tracker_Distance_lag2", "Tracker_Distance_lag3", "Logged_Activities_Distance_lag1", "Logged_Activities_Distance_lag2", "Logged_Activities_Distance_lag3", "Very_Active_Distance_lag1", "Very_Active_Distance_lag2", "Very_Active_Distance_lag3", "Moderately_Active_Distance_lag1", "Moderately_Active_Distance_lag2", "Moderately_Active_Distance_lag3", "Light_Active_Distance_lag1", "Light_Active_Distance_lag2", "Light_Active_Distance_lag3", "Sedentary_Active_Distance_lag1", "Sedentary_Active_Distance_lag2", "Sedentary_Active_Distance_lag3", "Very_Active_Minutes_lag1", "Very_Active_Minutes_lag2", "Very_Active_Minutes_lag3", "Fairly_Active_Minutes_lag1", "Fairly_Active_Minutes_lag2", "Fairly_Active_Minutes_lag3", "Lightly_Active_Minutes_lag1", "Lightly_Active_Minutes_lag2", "Lightly_Active_Minutes_lag3", "Sedentary_Minutes_lag1", "Sedentary_Minutes_lag2", "Sedentary_Minutes_lag3", "Steps_lag1", "Steps_lag2", "Steps_lag3", "Calories_Burned_lag1", "Calories_Burned_lag2", "Calories_Burned_lag3", "target_weekday", "target_is_weekend", "reached_10k_next_day"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (145 lines)
test.csv (145 lines)
train.csv (698 lines)```

-> sample_submission.csv has 144 rows and 2 columns.
The columns are: id, reached_10k_next_day

-> test.csv has 144 rows and 43 columns.
The columns are: id, user_id, Total_Distance_lag1, Total_Distance_lag2, Total_Distance_lag3, Tracker_Distance_lag1, Tracker_Distance_lag2, Tracker_Distance_lag3, Logged_Activities_Distance_lag1, Logged_Activities_Distance_lag2, Logged_Activities_Distance_lag3, Very_Active_Distance_lag1, Very_Active_Distance_lag2, Very_Active_Distance_lag3, Moderately_Active_Distance_lag1... and 28 more columns

-> train.csv has 697 rows and 44 columns.
The columns are: id, user_id, Total_Distance_lag1, Total_Distance_lag2, Total_Distance_lag3, Tracker_Distance_lag1, Tracker_Distance_lag2, Tracker_Distance_lag3, Logged_Activities_Distance_lag1, Logged_Activities_Distance_lag2, Logged_Activities_Distance_lag3, Very_Active_Distance_lag1, Very_Active_Distance_lag2, Very_Active_Distance_lag3, Moderately_Active_Distance_lag1... and 29 more columns
