# OpenMLE-fast task

Task ID: `weather-analysis@1`

Native metric: `WeatherForecastRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3615 bytes)
- `data/sample_submission.csv` (16951 bytes); columns: ["Id", "y"]
- `data/test.csv` (93473 bytes); columns: ["Id", "Average temperature (°F)", "Average humidity (%)", "Average dewpoint (°F)", "Average barometer (in)", "Average windspeed (mph)", "Average gustspeed (mph)", "Average direction (°deg)", "Rainfall for month (in)", "Rainfall for year (in)", "Maximum temperature (°F)", "Minimum temperature (°F)", "Maximum humidity (%)", "Minimum humidity (%)", "Maximum pressure", "Minimum pressure", "Maximum windspeed (mph)", "Maximum gust speed (mph)", "Maximum heat index (°F)", "Month", "BaseDate", "ForecastDate"]
- `data/train.csv` (376965 bytes); columns: ["Average temperature (°F)", "Average humidity (%)", "Average dewpoint (°F)", "Average barometer (in)", "Average windspeed (mph)", "Average gustspeed (mph)", "Average direction (°deg)", "Rainfall for month (in)", "Rainfall for year (in)", "Maximum temperature (°F)", "Minimum temperature (°F)", "Maximum humidity (%)", "Minimum humidity (%)", "Maximum pressure", "Minimum pressure", "Maximum windspeed (mph)", "Maximum gust speed (mph)", "Maximum heat index (°F)", "Month", "BaseDate", "ForecastDate", "y"]

## Public description

Competition: Next‑day Maximum Temperature Forecasting (Single Station, Daily)

Problem statement
Build a model that predicts the next day’s maximum temperature (°F) using daily weather observations from a single station. Each row in train.csv corresponds to a base day t with its features and target y equal to the next day’s (t+1) maximum temperature. Each row in test.csv corresponds to a base day in a held‑out, future period; you must predict y for the next day.

Files provided
- train.csv: Daily features for historical dates and the target column y (next day’s maximum temperature). Includes BaseDate (t) and ForecastDate (t+1).
- test.csv: Daily features for the held‑out period with an Id column for submission merging. Includes BaseDate (t) and ForecastDate (t+1). The y column is not provided.
- sample_submission.csv: Expected submission format with example predictions for all Ids in test.csv.

Data description (columns)
- Id (test.csv only): Unique identifier for each required prediction.
- BaseDate: The date of the provided features (day t).
- ForecastDate: The date for which the prediction is required (day t+1). Provided for clarity and time‑based feature engineering.
- y (train.csv only; and required in submissions): The next day’s maximum temperature (°F).
- Remaining columns: Meteorological features derived from the daily archive, including average temperature (°F), humidity (%), dewpoint (°F), barometer (in), windspeed (mph), gustspeed (mph), wind direction (°deg), cumulative rainfall indicators (in), daily minimum temperature (°F), daily maximum/minimum humidity (%), maximum/minimum pressure (in), maximum windspeed/gust speed (mph), maximum heat index (°F), and Month. Redundant or all‑zero columns have been removed to avoid leakage/duplication.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on °F.
  RMSE = sqrt(mean((y_pred − y_true)^2)) over all rows, after matching by Id.
- Submission format: A CSV with exactly two columns named Id and y (in this order), containing a prediction for every row in test.csv. Extra/missing rows or columns will not be scored.

Train/test split
- The split is strictly chronological. Training covers earlier years; testing is a final continuous block near the end of the time span to evaluate generalization across seasons and potential concept drift. The final files already implement this split and include all usable rows with a valid next‑day label.

Guidance and constraints
- Forecasting discipline: Use only information from days ≤ t to predict y for day t+1.
- Recommended feature engineering (you implement in your notebook/code):
  - Lagged and rolling statistics (e.g., 1/3/7/14/30‑day) for temperature, humidity, pressure, wind, and rainfall counters.
  - Encode seasonality (day‑of‑year as sin/cos) and wind direction as circular features (sin/cos of degrees).
  - Treat cumulative rainfall counters carefully (they reset at month/year boundaries); only use values available up to day t.
  - Non‑linear models (tree ensembles/GBMs) or regularized linear/neural models with temporal encodings often perform well.
- Validation tip: Use expanding‑window or time‑series cross‑validation that preserves chronology; do not shuffle across time.

Notes
- All rows and features in the provided files are intended for modeling; no subset is required.
- The target is continuous and physically meaningful; RMSE in °F is interpretable and penalizes large errors appropriately.
- The files contain only tabular data; there are no external assets. Paths are not included in any CSV values.
