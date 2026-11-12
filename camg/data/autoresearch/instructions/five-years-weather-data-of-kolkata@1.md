# OpenMLE-fast task

Task ID: `five-years-weather-data-of-kolkata@1`

Native metric: `KolkataNextDayTempMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3426 bytes)
- `data/sample_submission.csv` (8110 bytes); columns: ["row_id", "target"]
- `data/test.csv` (53402 bytes); columns: ["row_id", "date", "context_date", "dow", "month", "dom", "doy", "doy_sin", "doy_cos", "Minimum_Temperature", "Maximum_Temperature", "Temperature", "Dew_Point", "Relative_Humidity", "Heat_Index", "Wind_Speed", "Wind_Gust", "Wind_Direction", "Wind_Chill", "Precipitation", "Precipitation_Cover", "Snow_Depth", "Visibility", "Cloud_Cover", "Sea_Level_Pressure"]
- `data/train.csv` (272606 bytes); columns: ["date", "context_date", "dow", "month", "dom", "doy", "doy_sin", "doy_cos", "Minimum_Temperature", "Maximum_Temperature", "Temperature", "Dew_Point", "Relative_Humidity", "Heat_Index", "Wind_Speed", "Wind_Gust", "Wind_Direction", "Wind_Chill", "Precipitation", "Precipitation_Cover", "Snow_Depth", "Visibility", "Cloud_Cover", "Sea_Level_Pressure", "target"]

## Public description

Kolkata Next-Day Maximum Temperature Forecast (2017–2022)

Problem statement
You are given six years of daily weather observations for Kolkata, India. Your task is to forecast the next day’s maximum temperature (in °C) for each day of 2022, using only information available up to the previous day. This is a realistic one-step-ahead daily forecasting task focused on short-term maxima, important for energy demand, health risk mitigation, and city operations.

Files provided
- train.csv: Supervised training data constructed from 2017–2021. Each row corresponds to a context day t and the target is the maximum temperature at day t+1.
- test.csv: Feature matrix for 2022 predictions. Each row contains the context day (t), the prediction date (t+1), and features that would have been known by the prediction time. Use the row_id column to align your predictions.
- sample_submission.csv: A sample submission with the correct format and randomized but plausible target values. Use it as a template.

Target
- target: Next-day maximum temperature (°C).

Columns and feature schema
Time columns:
- date: The prediction date (t+1) for which the target is evaluated.
- context_date: The context day (t) from which features are drawn. date = context_date + 1 day.

Calendar features (derived from date):
- dow: Day of week [0–6]
- month: Month number [1–12]
- dom: Day of month [1–31]
- doy: Day of year [1–366]
- doy_sin, doy_cos: Cyclical encodings of the day-of-year.

Meteorological features (measured on context_date):
- Minimum_Temperature, Maximum_Temperature, Temperature, Dew_Point, Relative_Humidity, Heat_Index, Wind_Speed, Wind_Gust, Wind_Direction, Wind_Chill, Precipitation, Precipitation_Cover, Snow_Depth, Visibility, Cloud_Cover, Sea_Level_Pressure

These meteorological variables are numerical and correspond to the same-named measurements in the original dataset, recorded for Kolkata. They are taken from context_date (t), which prevents label leakage when forecasting t+1.

Prediction format
- Create a CSV file with columns: row_id, target
- Each row_id must appear exactly once and align with test.csv.

Evaluation
- Submissions are evaluated using Mean Absolute Error (MAE) between your predictions and the ground truth next-day maximum temperatures for 2022.
- Lower MAE is better. MAE is interpretable in degrees Celsius and robust to occasional extremes.

Rules and guidance
- Treat this as a strictly one-step-ahead forecasting task: use only features at or before context_date (t) to predict date (t+1).
- You may perform any data processing and feature engineering you like (e.g., lagged features, rolling statistics, seasonal encodings), as long as you avoid leakage from the prediction day.
- External data are allowed only if they could have been known before the prediction date (e.g., public holiday calendars). If used, document your sources and ensure reproducibility.

Notes
- Train/test split is chronological: train covers 2017–2021 targets, test covers 2022 targets.
- test.csv includes both date and context_date to help you reason about temporal relationships; do not use any information from future days.
- The dataset is single-location; spatial identifiers are intentionally omitted from the feature set to prevent spurious correlations.
- All dates are daily with no gaps; day counting follows the calendar.

Submission example
row_id,target
0,33.2
1,32.7
2,31.4
...
