# OpenMLE-fast task

Task ID: `epidemy@2`

Native metric: `DengueQuantileForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3712 bytes)
- `data/sample_submission.csv` (3694 bytes); columns: ["city", "year", "weekofyear", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (20883 bytes); columns: ["city", "year", "weekofyear", "week_start_date", "ndvi_ne", "ndvi_nw", "ndvi_se", "ndvi_sw", "precipitation_amt_mm", "reanalysis_air_temp_k", "reanalysis_avg_temp_k", "reanalysis_dew_point_temp_k", "reanalysis_max_air_temp_k", "reanalysis_min_air_temp_k", "reanalysis_precip_amt_kg_per_m2", "reanalysis_relative_humidity_percent", "reanalysis_sat_precip_amt_mm", "reanalysis_specific_humidity_g_per_kg", "reanalysis_tdtr_k", "station_avg_temp_c", "station_diur_temp_rng_c", "station_max_temp_c", "station_min_temp_c", "station_precip_mm"]
- `data/train.csv` (270258 bytes); columns: ["city", "year", "weekofyear", "week_start_date", "ndvi_ne", "ndvi_nw", "ndvi_se", "ndvi_sw", "precipitation_amt_mm", "reanalysis_air_temp_k", "reanalysis_avg_temp_k", "reanalysis_dew_point_temp_k", "reanalysis_max_air_temp_k", "reanalysis_min_air_temp_k", "reanalysis_precip_amt_kg_per_m2", "reanalysis_relative_humidity_percent", "reanalysis_sat_precip_amt_mm", "reanalysis_specific_humidity_g_per_kg", "reanalysis_tdtr_k", "station_avg_temp_c", "station_diur_temp_rng_c", "station_max_temp_c", "station_min_temp_c", "station_precip_mm", "total_cases"]

## Public description

Title: Probabilistic Dengue Case Forecasting (Quantiles)

Problem statement
You are given weekly environmental, reanalysis, station weather, and NDVI features for two cities (San Juan and Iquitos). Your task is to produce calibrated probabilistic forecasts of dengue total_cases by predicting multiple quantiles for each (city, year, weekofyear) in a future hold‑out.

What you must predict
- For every row in test.csv (identified by city, year, weekofyear), predict the conditional quantiles of total_cases at Q = {0.10, 0.50, 0.90}.
- Your submission must contain the columns: city, year, weekofyear, q0.1, q0.5, q0.9.

Files provided
- train.csv: weekly features plus the target column total_cases.
- test.csv: weekly features without total_cases.
- sample_submission.csv: correct submission schema with example predictions.

Data description (columns)
- Identifiers and time: city, year, weekofyear, week_start_date (ISO date)
- NOAA station observations: station_max_temp_c, station_min_temp_c, station_avg_temp_c, station_precip_mm, station_diur_temp_rng_c
- PERSIANN precipitation: precipitation_amt_mm
- NCEP reanalysis: reanalysis_* (temperatures in K, humidity, precipitation, tdtr)
- NDVI: ndvi_ne, ndvi_nw, ndvi_se, ndvi_sw
- Target (train only): total_cases (weekly dengue case counts)

Train/test split
- The split is strictly chronological and city-specific to respect forecasting causality.
- For each city, the last 52 contiguous weeks are held out for testing; all earlier weeks form the training set.
- Therefore, test is a pure future hold‑out for each city.

Evaluation
- Primary metric: macro-averaged pinball (quantile) loss across cities and quantiles Q = {0.10, 0.50, 0.90}.
  1) For each city separately, compute the mean pinball loss for each q over all its test rows, then average over the three quantiles.
  2) Finally, average the two city scores with equal weight (macro average).
- Pinball loss for a single observation y and predicted quantile y_q at level q is:
    pinball(y, y_q, q) = (y - y_q) * q, if y >= y_q; otherwise (y_q - y) * (1 - q).
- Lower is better. Predictions may be any real values; negative values are allowed by the loss but are rarely sensible for counts.

Important notes and recommendations
- Time-series discipline: When engineering features (e.g., lags, rolling windows, or autoregressive targets), use only past information. Do not leak future values from the test horizon.
- Useful features: month/quarter, cyclic encodings of weekofyear, per-city lags (1–4, 6, 8, 12, 16) and rolling statistics for precipitation, temperatures, humidity, dew point, NDVI, diurnal range, and autoregressive total_cases (train only; for test, roll forward sequentially).
- Missing data: There are NaNs (e.g., NDVI). Impute using only historical information within each city. Missingness indicators can be helpful.
- Scaling: Per-city robust scaling can stabilize training due to climatology differences between cities.
- Modeling: Any ML approach capable of quantile prediction is allowed (e.g., Gradient Boosting/GBDT with quantile loss, LightGBM, XGBoost, CatBoost quantiles, distributional regression like Negative Binomial to extract quantiles, or conformalized quantiles on top of point forecasts).
- Validation: Use blocked or expanding-window time-series CV and optimize averaged pinball loss across the specified quantiles.

Submission format
- CSV with columns: city, year, weekofyear, q0.1, q0.5, q0.9
- Each (city, year, weekofyear) must appear exactly once.
- It is recommended (not required) that q0.1 <= q0.5 <= q0.9 for every row.

Final files for the competition
- train.csv
- test.csv
- sample_submission.csv

Good luck and forecast responsibly!
