# OpenMLE-fast task

Task ID: `indian-aqi-trends-and-health-risk-20192024@1`

Native metric: `IndianAQIMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3025 bytes)
- `data/sample_submission.csv` (30788 bytes); columns: ["row_id", "AQI"]
- `data/test.csv` (371416 bytes); columns: ["row_id", "City", "Temperature (°C)", "Humidity (%)", "Wind Speed (km/h)", "Rainfall (mm)", "Pressure (hPa)", "Vehicle Count", "Industrial Activity Index"]
- `data/train.csv` (885912 bytes); columns: ["City", "Temperature (°C)", "Humidity (%)", "Wind Speed (km/h)", "Rainfall (mm)", "Pressure (hPa)", "Vehicle Count", "Industrial Activity Index", "AQI"]

## Public description

Indian AQI from Drivers: Unseen-City Generalization Challenge

Problem statement
Build a model that predicts daily city-level Air Quality Index (AQI) using only non-pollutant drivers: meteorology and urban activity, plus the city identity. The test set contains cities that do not appear in the training set. Your goal is to generalize AQI estimation to unseen cities from proxy drivers when pollutant sensors are unavailable.

Data description
You are provided with three files:
- train.csv: Feature matrix and target for model development.
- test.csv: Feature matrix for which you must predict AQI.
- sample_submission.csv: A sample showing the required submission format.

Columns
- Features (present in train.csv and test.csv):
  - City (string)
  - Temperature (°C) (float)
  - Humidity (%) (float)
  - Wind Speed (km/h) (float)
  - Rainfall (mm) (float)
  - Pressure (hPa) (float)
  - Vehicle Count (int)
  - Industrial Activity Index (float)
- Target (only in train.csv):
  - AQI (numeric)
- Indexing:
  - row_id (int) is included in test.csv and expected in submissions to align predictions with rows. It is a unique, deterministic identifier for each test row.

Important exclusions (already handled in the prepared train/test files)
- No pollutant concentration columns (PM2.5, PM10, NO2, CO, SO2, O3) are provided to prevent label leakage.
- Non-informative columns are removed.

Split protocol
- Train/test split is by City to enforce domain shift. All rows from a given city appear either in train or in test, never both. Approximately 70% of cities are in train and 30% in test, chosen deterministically so that every participant sees the same split.

Task
- Train any regression model to predict AQI for the rows in test.csv. Typical approaches include tree ensembles, regularized linear models, and modern tabular deep learning. Careful feature engineering and robust handling of domain shift are encouraged.

Submission format
- A CSV with exactly two columns and the same number of rows as test.csv:
  - row_id (int)
  - AQI (numeric prediction)
- The row_id must match those in test.csv. Do not reorder or drop rows.

Evaluation
- Primary metric: Macro-averaged Mean Absolute Error (MAE) across cities.
  1) For each city in the test set, compute MAE between your predictions and the ground truth for that city.
  2) Average these city-level MAEs with equal weight (macro-average) to produce the final score.
- Rationale: MAE is interpretable and robust; macro-averaging prevents large cities from dominating the score and rewards generalization across diverse urban contexts.

File list delivered for the competition
- train.csv — features + AQI target
- test.csv — features + row_id (no AQI)
- sample_submission.csv — example submission with valid structure

Notes
- Numerical values may contain a wide range. Consider normalization, interaction features, and city encodings.
- Deterministic behavior is preferred (set random seeds where applicable).
- The task is regression, not classification.
