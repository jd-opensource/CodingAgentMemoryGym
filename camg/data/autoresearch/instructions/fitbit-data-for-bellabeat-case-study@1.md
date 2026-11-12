# OpenMLE-fast task

Task ID: `fitbit-data-for-bellabeat-case-study@1`

Native metric: `FitbitIntensityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (553 bytes)
- `data/sample_submission.csv` (6528 bytes); columns: ["row_id", "TotalIntensity"]
- `data/test.csv` (186508 bytes); columns: ["hr_mean", "hr_median", "hr_min", "hr_max", "hr_std", "hr_mean_abs_diff", "hr_diff_std", "hr_up_count", "hr_down_count", "hr_zone_rest_frac", "hr_zone_light_frac", "hr_zone_moderate_frac", "hr_zone_vigorous_frac", "coverage_seconds", "hour_of_day", "day_of_week", "TotalSteps", "Calories", "VeryActiveMinutes", "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes", "VeryActiveDistance", "ModeratelyActiveDistance", "LightActiveDistance", "daily_missing", "TotalSleepRecords", "TotalMinutesAsleep", "TotalTimeInBed", "sleep_missing", "row_id"]
- `data/train.csv` (1163217 bytes); columns: ["hr_mean", "hr_median", "hr_min", "hr_max", "hr_std", "hr_mean_abs_diff", "hr_diff_std", "hr_up_count", "hr_down_count", "hr_zone_rest_frac", "hr_zone_light_frac", "hr_zone_moderate_frac", "hr_zone_vigorous_frac", "coverage_seconds", "hour_of_day", "day_of_week", "TotalSteps", "Calories", "VeryActiveMinutes", "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes", "VeryActiveDistance", "ModeratelyActiveDistance", "LightActiveDistance", "daily_missing", "TotalSleepRecords", "TotalMinutesAsleep", "TotalTimeInBed", "sleep_missing", "row_id", "TotalIntensity"]

## Public description

Title: Hourly Activity Intensity Prediction from Heart Rate and Daily Context

Files:
- train.csv
- test.csv
- sample_submission.csv

Contents:
- train.csv: Engineered features per user-hour with a unique row_id and the target column TotalIntensity.
- test.csv: Same features and row_id without the target.
- sample_submission.csv: Example predictions with columns [row_id, TotalIntensity].

Evaluation:
- Metric is RMSE on TotalIntensity. Lower is better.
Submission:
- Submit a CSV with columns [row_id, TotalIntensity] where row_id matches test.csv.
