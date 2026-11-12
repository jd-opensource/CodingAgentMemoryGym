# OpenMLE-fast task

Task ID: `denpasarbalihistoricalweatherdata@1`

Native metric: `RainfallNowcastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3372 bytes)
- `data/sample_submission.csv` (195766 bytes); columns: ["row_id", "next_rain_1h"]
- `data/test.csv` (1773973 bytes); columns: ["row_id", "temp", "temp_min", "temp_max", "pressure", "sea_level", "grnd_level", "humidity", "wind_speed", "wind_deg", "clouds_all", "rain_1h", "rain_3h", "rain_6h", "rain_12h", "rain_24h", "rain_today", "local_hour", "local_month", "local_dayofyear", "local_year", "dt", "timezone"]
- `data/train.csv` (25467928 bytes); columns: ["row_id", "temp", "temp_min", "temp_max", "pressure", "sea_level", "grnd_level", "humidity", "wind_speed", "wind_deg", "clouds_all", "rain_1h", "rain_3h", "rain_6h", "rain_12h", "rain_24h", "rain_today", "local_hour", "local_month", "local_dayofyear", "local_year", "dt", "timezone", "next_rain_1h"]

## Public description

Denpasar Hourly Rainfall Nowcasting (1-hour ahead)

Problem statement
Participants are challenged to build a model that predicts the next-hour rainfall amount (mm) in Denpasar, Bali, Indonesia. At each hour t, you must forecast rain_1h at t+1 using only information available up to and including hour t. This is a time-aware regression task on a long, zero-inflated series with occasional heavy rain events.

Data description
You are provided with curated training and test tables constructed from 30 years of hourly meteorological observations (OpenWeatherMap for Denpasar, UTC+8). Each row corresponds to an hour t. The training set includes the target column next_rain_1h (the rain_1h value at t+1). The test set contains only features at time t; the target is hidden for scoring.

Features
- Numeric meteorological variables at time t: temp, temp_min, temp_max, pressure, sea_level, grnd_level, humidity, wind_speed, wind_deg, clouds_all.
- Recent rainfall aggregates at time t: rain_1h, rain_3h, rain_6h, rain_12h, rain_24h, rain_today (missing values are treated as 0).
- Time-derived features at time t using local time (UTC+8): local_hour, local_month, local_dayofyear, local_year.
- Non-predictive categorical/text variables (e.g., weather_main/description) have been removed to avoid leakage and ensure focus on physically meaningful signals.

Files
- train.csv: feature columns at hour t and labeled target next_rain_1h at t+1, plus a unique row_id.
- test.csv: same feature columns and row_id but without next_rain_1h.
- sample_submission.csv: a valid example submission file demonstrating the required format.

Target and constraints
- Target: next_rain_1h (mm), non-negative.
- Use only features from hour t to predict the rainfall at hour t+1. You may engineer lagged features and aggregates, but they must be functions of information up to t.

Evaluation
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between predicted and true next_rain_1h:
- rmsle = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
This choice is well-suited for rainfall: values are non-negative, dominated by zeros with a long right tail. RMSLE balances performance across light/no rain and heavy rain, while damping the influence of rare extremes.

Submission format
- CSV with two columns in order: row_id, next_rain_1h.
- row_id must exactly match the provided test.csv row_id values and order.
- next_rain_1h must be a non-negative real number per row.

Train/test split
- Chronological split to respect causality:
  - Train covers historical hours where t+1 is before 2018-01-01 local time.
  - Test covers subsequent hours through early 2020.

Guidance and expectations
- Strong performance requires careful time-aware preprocessing, feature engineering (e.g., lagged rainfall and meteorological variables, rolling windows, seasonal indicators), and robust modeling (e.g., GBMs, random forests, linear models with regularization, or sequence models). Handle zero-inflation and non-stationarity. Avoid any information leakage from future times.

Notes
- All rainfall/snowfall aggregates with missing entries are treated as zero in the prepared tables.
- dt and timezone are retained for potential feature engineering; no future information is present in test.
- The dataset scale is large (hundreds of thousands of rows) — runtime is not constrained.
