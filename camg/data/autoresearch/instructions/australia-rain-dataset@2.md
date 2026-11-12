# OpenMLE-fast task

Task ID: `australia-rain-dataset@2`

Native metric: `AustraliaRainfallRMSLMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3294 bytes)
- `data/sample_submission.csv` (423818 bytes); columns: ["Id", "NextDayRainfall"]
- `data/test.csv` (3083618 bytes); columns: ["Id", "Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainToday"]
- `data/train.csv` (12387750 bytes); columns: ["Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainToday", "NextDayRainfall"]

## Public description

Australia Next-Day Rainfall Amount (Skewed Regression)

Background
Australia’s daily weather observations span multiple years and 49 locations, exhibiting strong seasonality and spatial variability. Rainfall amounts are zero-inflated and heavy-tailed, making quantitative prediction both challenging and practically important for weather-sensitive decision-making.

Problem statement
Using a day’s weather observations at a station, predict the next day’s rainfall amount (in mm) at the same station. This is a point-forecast regression task with a skewed, zero-inflated target.

Files
- train.csv: Training data containing features and the numeric target NextDayRainfall.
- test.csv: Test data containing the same features only, plus an Id column.
- sample_submission.csv: Example submission file with the correct format and random valid predictions.

Target construction
The target, NextDayRainfall, is constructed by grouping by Location and shifting the Rainfall column forward by one day. Rows without a valid next-day Rainfall are excluded from the dataset.

Features
Each row corresponds to a specific Date and Location and includes the following same-day observed features:
- Date, Location,
- MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
- WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm,
- WindSpeed9am, WindSpeed3pm,
- Humidity9am, Humidity3pm,
- Pressure9am, Pressure3pm,
- Cloud9am, Cloud3pm,
- Temp9am, Temp3pm,
- RainToday.
Note: The original classification label RainTomorrow is excluded to avoid label leakage.

Split strategy
This is a time-aware generalization task. For each Location, the most recent portion of dates is allocated to the test set, and the earlier portion to the train set. Splitting is performed per-location to prevent temporal leakage. All splits are deterministic.

Evaluation metric
Submissions are evaluated using Root Mean Squared Log Error (RMSLE) between the ground truth and your predictions:
RMSLE = sqrt(mean((log1p(y_true) - log1p(y_pred))^2)).
- y_true is the actual next-day rainfall (mm), and y_pred is your predicted next-day rainfall (mm).
- Predictions must be numeric; negative predictions are clipped to 0 for scoring.
- RMSLE is robust for zero-inflated, heavy-tailed targets and penalizes underprediction on rainy days.

Submission format
Submit a CSV file with the following columns, in any order:
- Id: integer row identifier matching test.csv
- NextDayRainfall: your predicted value (mm)
The submission must contain exactly one row per Id in test.csv, with no missing or duplicate Ids and no extra rows.

Modeling guidance (non-binding)
- Handle missing values carefully; some features (e.g., Sunshine, Evaporation, Cloud) have substantial missingness.
- Consider encoding wind directions and deriving seasonal/time features from Date (e.g., month, day-of-year).
- For temporal aggregates (e.g., rolling sums/means), compute them using only prior information relative to each forecast date to avoid leakage.
- Suitable models include gradient boosting, regularized GLMs, zero-inflated/mixture models, and tree-based ensembles.

Goal
Build the most accurate forecasting model for next-day rainfall across Australia’s stations and seasons under a fair, leakage-aware temporal split, using the full scale of the data.
