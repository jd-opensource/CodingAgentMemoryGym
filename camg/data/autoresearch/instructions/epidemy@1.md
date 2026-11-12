# OpenMLE-fast task

Task ID: `epidemy@1`

Native metric: `DengueForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3441 bytes)
- `data/sample_submission.csv` (4551 bytes); columns: ["city", "year", "weekofyear", "total_cases"]
- `data/test.csv` (58085 bytes); columns: ["city", "year", "weekofyear", "week_start_date", "ndvi_ne", "ndvi_nw", "ndvi_se", "ndvi_sw", "precipitation_amt_mm", "reanalysis_air_temp_k", "reanalysis_avg_temp_k", "reanalysis_dew_point_temp_k", "reanalysis_max_air_temp_k", "reanalysis_min_air_temp_k", "reanalysis_precip_amt_kg_per_m2", "reanalysis_relative_humidity_percent", "reanalysis_sat_precip_amt_mm", "reanalysis_specific_humidity_g_per_kg", "reanalysis_tdtr_k", "station_avg_temp_c", "station_diur_temp_rng_c", "station_max_temp_c", "station_min_temp_c", "station_precip_mm"]
- `data/train.csv` (232570 bytes); columns: ["city", "year", "weekofyear", "week_start_date", "ndvi_ne", "ndvi_nw", "ndvi_se", "ndvi_sw", "precipitation_amt_mm", "reanalysis_air_temp_k", "reanalysis_avg_temp_k", "reanalysis_dew_point_temp_k", "reanalysis_max_air_temp_k", "reanalysis_min_air_temp_k", "reanalysis_precip_amt_kg_per_m2", "reanalysis_relative_humidity_percent", "reanalysis_sat_precip_amt_mm", "reanalysis_specific_humidity_g_per_kg", "reanalysis_tdtr_k", "station_avg_temp_c", "station_diur_temp_rng_c", "station_max_temp_c", "station_min_temp_c", "station_precip_mm", "total_cases"]

## Public description

Dengue Week-Ahead Case Forecasting for San Juan and Iquitos

Problem statement
You are given weekly environmental, reanalysis, station weather, and satellite vegetation (NDVI) measurements for two cities: San Juan (sj) and Iquitos (iq). Your task is to predict the number of dengue cases (total_cases) for each (city, year, weekofyear) in the test set. The data are weekly time series; relationships are nonlinear and include delays (e.g., between precipitation, temperature, humidity, vegetation, and disease incidence). This is a forecasting regression problem.

Files
- train.csv: Labeled training data. Columns include:
  - city (sj/iq), year, weekofyear, week_start_date
  - Weather and reanalysis features (e.g., station_max_temp_c, station_min_temp_c, station_avg_temp_c, station_precip_mm, station_diur_temp_rng_c, precipitation_amt_mm, reanalysis_* variables)
  - Satellite vegetation features: ndvi_ne, ndvi_nw, ndvi_se, ndvi_sw
  - Target: total_cases (nonnegative integer)
- test.csv: Unlabeled test data with the same feature columns as train.csv except total_cases is absent.
- sample_submission.csv: Correct submission format with random but valid example predictions.

Target
- total_cases: weekly dengue cases per (city, year, weekofyear), an integer count but evaluated on the original (non-log) scale. Predictions do not need to be integers.

Evaluation
- Macro-averaged Mean Absolute Error (MAE) across cities:
  1) Compute the MAE over test rows for San Juan (sj)
  2) Compute the MAE over test rows for Iquitos (iq)
  3) Final score = 0.5 * MAE_sj + 0.5 * MAE_iq
This weighting ensures balanced importance for both cities regardless of different test set sizes. MAE provides a robust, interpretable error on count data. Lower is better.

Submission format
- CSV with the following columns in any order:
  - city, year, weekofyear, total_cases
- Each row must correspond to exactly one row in the test set index (city, year, weekofyear). Extra or missing rows, duplicates, or malformed numeric values will be rejected by the validator.

Data split
- The test set is a deterministic, strictly future hold-out per city constructed from the most recent 20% of weeks in the labeled data for each city. This preserves the forecasting nature of the task and prevents leakage: the maximum train date is strictly earlier than the minimum test date within each city.

Guidance and caveats
- Handle missing values carefully (notably NDVI). Reasonable strategies include forward-fill within city, interpolation, rolling medians, and missingness indicators.
- Respect temporal causality when creating features (lags and rolling windows). Do not leak future information.
- Per-city modeling or features often help: different climatology and dynamics. City-aware scaling/normalization is encouraged.
- Seasonal encodings (e.g., month, sine/cosine of weekofyear) and lagged/rolling summaries of precipitation, temperature, humidity, dew point, NDVI, and diurnal temperature range are strong candidates.
- Consider count-aware models (e.g., Poisson/Negative Binomial), gradient boosting, or sequence models with causal structure. Use time-based cross-validation per city.

Quality checklist
- No paths are embedded in CSVs.
- Column names are stable across train/test.
- All test identifiers (city, year, weekofyear) are unique and correspond exactly to submission rows.

Good luck and build strong, causal, and robust dengue forecasts!
