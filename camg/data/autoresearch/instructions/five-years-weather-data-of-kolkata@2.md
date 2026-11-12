# OpenMLE-fast task

Task ID: `five-years-weather-data-of-kolkata@2`

Native metric: `KolkataRainProbabilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3167 bytes)
- `data/sample_submission.csv` (2823 bytes); columns: ["row_id", "rain_tomorrow"]
- `data/test.csv` (31036 bytes); columns: ["row_id", "date", "Minimum Temperature", "Maximum Temperature", "Temperature", "Dew Point", "Relative Humidity", "Heat Index", "Wind Speed", "Wind Gust", "Wind Direction", "Wind Chill", "Precipitation", "Precipitation Cover", "Snow Depth", "Visibility", "Cloud Cover", "Sea Level Pressure"]
- `data/train.csv` (167580 bytes); columns: ["row_id", "date", "Minimum Temperature", "Maximum Temperature", "Temperature", "Dew Point", "Relative Humidity", "Heat Index", "Wind Speed", "Wind Gust", "Wind Direction", "Wind Chill", "Precipitation", "Precipitation Cover", "Snow Depth", "Visibility", "Cloud Cover", "Sea Level Pressure", "rain_tomorrow"]

## Public description

Kolkata Next‑Day Rain Probability (PoP)

Problem statement
Forecast the probability that it will rain tomorrow in Kolkata (i.e., that next‑day precipitation > 0.0 mm). For each calendar day t, predict P(rain on day t+1) using only information available up to (and including) day t.

What you are given
- train.csv: Daily weather observations and the target for 2017–2021. Each row is a calendar day t with:
  - row_id: unique identifier for the row
  - date: the date for which features are recorded (YYYY‑MM‑DD)
  - 16 numeric weather features for that date (see below)
  - rain_tomorrow: binary target, 1 if precipitation on the next day (t+1) was > 0.0 mm, else 0
- test.csv: Daily weather observations for 2022 (except the final day). Each row is a calendar day t with:
  - row_id, date, the same 16 numeric features as train.csv
  - No target column
- sample_submission.csv: Example submission file listing every test row_id with a random but valid probability in [0, 1]. Replace the probability values with your predictions.

Features included (per day t)
- Minimum Temperature
- Maximum Temperature
- Temperature
- Dew Point
- Relative Humidity
- Heat Index
- Wind Speed
- Wind Gust
- Wind Direction
- Wind Chill
- Precipitation
- Precipitation Cover
- Snow Depth
- Visibility
- Cloud Cover
- Sea Level Pressure

Notes
- Textual descriptor fields and location metadata are excluded to avoid ambiguity and simplify usage. You are free to engineer additional features (e.g., lags, rolling statistics, seasonality encodings) from train.csv and test.csv.
- Dates are strictly chronological and daily. The last train row is 2021‑12‑30 and the first test row is 2022‑01‑01. The final 2022 day is excluded from test so that all targets exist for evaluation.

Task
- Train a model on train.csv that estimates the probability of rain tomorrow given the features for today.
- Generate predictions for every row in test.csv.
- Submit a CSV with two columns: row_id and rain_tomorrow, where rain_tomorrow is a probability in [0, 1].

Evaluation metric
- Submissions are evaluated using the Brier score (mean squared error between your predicted probabilities and the ground‑truth binary outcomes):
  - score = mean((p_i − y_i)^2) over all test rows
  - Lower is better
- This is a proper scoring rule: it rewards both discrimination and calibration.

File format requirements
- Your submission must contain exactly these columns in this order: row_id, rain_tomorrow.
- Every row_id from test.csv must appear exactly once.
- Predicted values must be numeric and within [0, 1].

Suggested modeling considerations
- Handle missing values carefully (some wind/heat‑derived fields may be blank on certain days).
- Incorporate temporal structure: lagged features, rolling means/variances, rain/no‑rain streaks, and seasonality (month, day‑of‑year, monsoon period) often help.
- Try probabilistic models or calibrate outputs (e.g., isotonic/Platt) to improve Brier score.

Deliverables
- train.csv, test.csv, and sample_submission.csv are provided.
- Submit your predictions as a CSV named however you like (content must match the required format).
