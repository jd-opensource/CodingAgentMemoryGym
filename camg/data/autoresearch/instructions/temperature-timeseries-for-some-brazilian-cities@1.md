# OpenMLE-fast task

Task ID: `temperature-timeseries-for-some-brazilian-cities@1`

Native metric: `TemperatureForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3132 bytes)
- `data/sample_submission.csv` (20196 bytes); columns: ["station_id", "year", "month", "temp"]
- `data/station_mapping.csv` (144 bytes); columns: ["station_id", "station_name"]
- `data/test.csv` (6802 bytes); columns: ["station_id", "year", "month"]
- `data/train.csv` (99985 bytes); columns: ["station_id", "year", "month", "temp"]

## Public description

Competition: Multi-City Monthly Temperature Forecasting in Brazil

Problem statement
Participants must forecast monthly mean air temperature (in °C) for multiple Brazilian weather stations over a future window. Using historical monthly temperatures per station, build time-series models that predict the temperature for every station-month in the held-out years.

Data description
- train.csv: Long-format training data with columns [station_id, year, month, temp]. Contains all stations and months for years strictly before 2010, excluding missing values.
- test.csv: Long-format test identifiers with columns [station_id, year, month]. Contains all stations and months for years 2010–2014 inclusive.
- sample_submission.csv: Example submission aligned with test.csv, columns [station_id, year, month, temp]. Values are placeholders.
- station_mapping.csv: Optional helper mapping [station_id, station_name] provided for transparency; station_name is not required for modeling.

Target and features
- Target: temp (monthly mean temperature, °C).
- Features: Participants may engineer features from train.csv (e.g., lags, seasonal indicators, station-wise trends). Do not rely on derived seasonal/annual columns; they are not included.

Important notes
- Missing values in the original source were encoded as 999.90. Training rows containing that sentinel are excluded from train.csv. In evaluation, months in the test window with 999.90 labels are masked out and do not contribute to the score.
- Time-awareness is required: models must avoid leakage from test to train (e.g., normalization must be fit on training data only).
- Multi-task setup: station_id is an anonymized integer per station to encourage generalization across heterogeneous climates.

Submission format
Submit a single CSV with columns [station_id, year, month, temp], containing one row per identifier in test.csv. The [station_id, year, month] keys must match test.csv exactly, and temp must be numeric and finite.

Evaluation metric
- Primary metric: Mean Absolute Error (MAE) in °C, computed over all test rows with valid ground truth (i.e., rows whose true temp is not 999.90 and is finite).
- Rationale: MAE is directly interpretable in °C, robust to occasional outliers, and fair across stations whose temperatures lie in similar ranges.

Scope and difficulty
- The dataset spans decades with strong seasonality, station-specific trends, and nonuniform record lengths. High-quality solutions will combine robust preprocessing (missing-data handling, de-seasonalization), feature engineering (calendar effects, lags, trends), and appropriate model families (e.g., ARIMA/ETS, gradient boosting, RNN/TCN/Transformer) to forecast multiple horizons.

Files to use
- Training: train.csv
- Test identifiers: test.csv
- Sample: sample_submission.csv (for format reference)

Scoring details
- The leaderboard score is the MAE over the evaluation set. Rows with missing or invalid ground truth are excluded from scoring via masking.
- Submissions must contain predictions for all rows in test.csv and only those rows; extra or missing rows will be rejected.
