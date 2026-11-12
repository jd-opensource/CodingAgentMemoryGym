# OpenMLE-fast task

Task ID: `2022-ukraine-russian-war@1`

Native metric: `WarLossForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3906 bytes)
- `data/sample_submission.csv` (10964 bytes); columns: ["row_id", "y"]
- `data/test.csv` (18054 bytes); columns: ["row_id", "series_id", "date"]
- `data/train.csv` (975874 bytes); columns: ["row_id", "series_id", "date", "y"]

## Public description

Competition: Multi-Target Daily Loss Forecasting (Russia–Ukraine War)

Problem statement
You are given multi-year daily cumulative counts of Russian personnel and equipment losses from the 2022–ongoing invasion of Ukraine. Your task is to forecast the next 28 days of daily new losses (increments) for a selected portfolio of target series. The competition evaluates joint accuracy across all targets with a robust, scale-free metric.

What you must predict
- Forecast horizon: 28 consecutive calendar days (the last 28 days of the dataset).
- Targets: daily increments for these series (one forecast per date and per series):
  - personnel
  - aircraft, helicopter, tank, APC, field_artillery, MRL, drone, anti_aircraft_warfare, naval_ship, special_equipment, submarines, cruise_missiles, vehicles_and_fuel
- All forecasts must be non-negative real numbers.

Provided files
- train.csv — Historical daily increments for each target series.
  - Columns: row_id, series_id, date, y
  - One row per (series_id, date). y is the observed daily increment (>= 0).
- test.csv — Rows to be forecasted for the next 28 days.
  - Columns: row_id, series_id, date
  - Submit predictions for all listed row_id.
- sample_submission.csv — A valid example submission with random but plausible values.
  - Columns: row_id, y

Data notes (already applied in train/test generation)
- Official correction records are integrated before computing daily increments. Corrections apply as step adjustments to the cumulative series from the correction date onward.
- Vehicles-and-fuel harmonization: vehicles_and_fuel is constructed consistently across the full history. When “vehicles and fuel tanks” exists it is used; for earlier periods, it is reconstructed as (military_auto + fuel_tank).
- Daily increments are computed via first differences of the corrected cumulative series; the first available day’s increment equals its cumulative value. Negative residuals, if any remain after correction handling, are clamped to 0.
- Non-target, textual, or extremely sparse columns are excluded. Only the series listed above appear in train/test.

Evaluation metric
- Primary metric: macro-averaged MASE (Mean Absolute Scaled Error) with weekly seasonality on daily increments.
  - For each series s, let y_s,t be the true increment on day t, and ŷ_s,t be your forecast. Define the seasonal naive baseline with period m = 7 using the training data only. Its in-sample MAE is MAE_s(naive) = mean over t≥m of |y_s,t − y_s,t−m|.
  - The series-level error is MASE_s = mean over all test days of |y_s,t − ŷ_s,t| / MAE_s(naive).
  - The competition score is the simple (macro) average of MASE_s across all series.
  - If a series has too little variation for the denominator (or too short length), a robust fallback is used so the denominator remains positive and finite. This ensures fair comparison across very low-count series.

Submission format
- File: submission.csv
- Columns:
  - row_id — unique identifier in the form series_id__YYYY-MM-DD (exactly as provided in test.csv)
  - y — your forecast (non-negative real number)
- Do not change row order or row_id values. Every row in test.csv must appear exactly once in submission.csv.

Important expectations
- Use time-series/ML methods to preprocess, engineer features, train models, and forecast the 28-day horizon. You may use cross-series information, calendar features, and model ensembles. External data is not required.
- The split is strictly chronological: training covers all dates up to T−28; test covers T−27 … T. Do not leak any test-period information into training.
- The dataset includes heterogeneous series, from frequent to rare events. Robust modeling and careful evaluation are essential.

Files you will find after running the preparation script
- train.csv, test.csv, sample_submission.csv

Good luck and happy forecasting!
