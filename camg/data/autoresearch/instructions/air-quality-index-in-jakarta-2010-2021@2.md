# OpenMLE-fast task

Task ID: `air-quality-index-in-jakarta-2010-2021@2`

Native metric: `JakartaAQICriticalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5027 bytes)
- `data/sample_submission.csv` (7704 bytes); columns: ["tanggal", "PM25", "PM10", "O3", "CO", "SO2", "NO2"]
- `data/test.csv` (657 bytes); columns: ["tanggal"]
- `data/test_input/citywide_aggregated.csv` (409480 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/test_input/ispu_dki1.csv` (360190 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/test_input/ispu_dki2.csv` (357992 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/test_input/ispu_dki3.csv` (327428 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/test_input/ispu_dki4.csv` (344291 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/test_input/ispu_dki5.csv` (287622 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train.csv` (81389 bytes); columns: ["tanggal", "critical"]
- `data/train/citywide_aggregated.csv` (409480 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train/ispu_dki1.csv` (360190 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train/ispu_dki2.csv` (357992 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train/ispu_dki3.csv` (327428 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train/ispu_dki4.csv` (344291 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train/ispu_dki5.csv` (287622 bytes); columns: ["tanggal", "stasiun", "pm25", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"]
- `data/train_targets.csv` (81389 bytes); columns: ["tanggal", "critical"]

## Public description

Competition: Jakarta AQI Critical Pollutant Next-Day Prediction

Overview
- Task: Given historical daily pollutant indices from five Jakarta stations and past citywide aggregates up to the day before prediction, forecast which pollutant will be the citywide critical pollutant tomorrow.
- Target: One of six classes {PM25, PM10, O3, CO, SO2, NO2}.
- Setting: Multi-station, multiclass time-series forecasting. Use all provided training history and the provided test-input history; predict the next-day class for each date in the test set.

Files provided
- train/:
  - citywide_aggregated.csv: Daily citywide index (highest across stations on each date) with pollutant indices, max and critical label.
  - ispu_dki1.csv … ispu_dki5.csv: Station-level daily pollutant indices and station-level max/critical.
- test_input/:
  - Same schema as train/, but restricted to dates up to 2024-12-31 to avoid leakage. Use these as the feature history when forecasting test targets.
- train_targets.csv: Two columns [tanggal, critical] for the training period.
- test.csv: Dates to predict (one row per target date).
- sample_submission.csv: Example submission with well-formed probability distributions for each class and each target date.

Final train/test artifacts (participants use these; original raw files are not part of the interface):
- Train inputs: train/citywide_aggregated.csv, train/ispu_dki1.csv … train/ispu_dki5.csv
- Train targets: train_targets.csv
- Test inputs: test_input/citywide_aggregated.csv, test_input/ispu_dki1.csv … test_input/ispu_dki5.csv
- Test index: test.csv (list of target dates)
- Submission template: sample_submission.csv

Detailed problem statement
- You must predict the next-day citywide critical pollutant for each date in test.csv. For a date D in test.csv, use any information occurring strictly before D (i.e., dates ≤ D-1) from station files and the citywide aggregate. Do not use same-day or future values relative to D.
- Align the five station files and the citywide aggregate by tanggal. You may engineer lags and rolling statistics (per-station/per-pollutant) and cross-station aggregates, and derive temporal features such as day-of-week and month.
- Rows with categori == "TIDAK ADA DATA" or with all pollutant indices missing/zero may be dropped during preprocessing. Handle missingness robustly.

Recommended feature engineering (non-exhaustive)
- Per station and pollutant: lags at t-1, t-3, t-7; 7/14/28-day rolling mean, max, std; valid-count.
- Cross-station aggregates (for each pollutant): rolling mean/max across stations.
- Encode previous-day critical pollutant (both station-level and citywide) as categorical features.
- Calendar features: day-of-week, month, day-of-year, holidays if desired.

Label definition
- For date D, the label is citywide_aggregated.critical at D (the pollutant with the highest AQI component that day). This yields a 1-day-ahead classification target when using history up to D-1.

Evaluation
- Primary metric: Macro F1 over the six classes. We compute argmax from your submitted class probabilities and average per-class F1.
- Secondary metric (tie-breaker): Multiclass log loss computed from your probabilities.
- Submission format: A CSV with columns [tanggal, PM25, PM10, O3, CO, SO2, NO2]. Dates in tanggal must match test.csv exactly (order need not match). Each row of probabilities will be normalized to sum to 1; rows with invalid/NaN/Inf values are auto-cleaned then clipped and renormalized.

Metric rationale
- Macro F1 treats all pollutants equally regardless of frequency, which is crucial under shifting regimes and class imbalance. Log loss promotes calibrated probabilities.

Data split
- Training period covers all available valid dates up to and including 2024-12-31.
- Test period to score spans 2025-01-01 through 2025-02-28. The test_input files intentionally stop at 2024-12-31 to force genuine forecasting and prevent label leakage.

Constraints and tips
- Handle missing data and station outages gracefully; some pollutants or stations can be unavailable on certain days/years.
- Avoid label leakage: do not use any target-date values. Align your lags based on tanggal and ensure only past information is used for a given prediction date.
- Consider non-stationarity: pollutant dominance changes across years and seasons. Use robust models and time-aware cross-validation for model selection.

Submission
- Create a CSV named however you like (for scoring), with exactly these columns: tanggal, PM25, PM10, O3, CO, SO2, NO2.
- Ensure that every date listed in test.csv is present exactly once in your submission. Probability rows will be re-normalized during evaluation.

Baseline ideas
- Gradient boosted trees on engineered lags/rolls and calendar features.
- Regularized multinomial logistic regression on compact features.
- Sequence models (e.g., temporal CNNs or RNNs) applied to aligned station histories.

Good luck and have fun building robust spatiotemporal classifiers for Jakarta’s air quality!
