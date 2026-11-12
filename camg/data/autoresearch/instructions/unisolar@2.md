# OpenMLE-fast task

Task ID: `unisolar@2`

Native metric: `UniSolarPVForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3492 bytes)
- `data/sample_submission.csv` (671502 bytes); columns: ["row_id", "target"]
- `data/test.csv` (3056841 bytes); columns: ["row_id", "CampusKey", "Timestamp", "ApparentTemperature", "AirTemperature", "DewPointTemperature", "RelativeHumidity", "WindSpeed", "WindDirection", "minute_of_day", "day_of_year", "year", "is_weekend", "campus_lat", "campus_lon", "site_count"]
- `data/train.csv` (19485853 bytes); columns: ["CampusKey", "Timestamp", "ApparentTemperature", "AirTemperature", "DewPointTemperature", "RelativeHumidity", "WindSpeed", "WindDirection", "minute_of_day", "day_of_year", "year", "is_weekend", "campus_lat", "campus_lon", "site_count", "target"]

## Public description

UNISOLAR Campus PV Nowcasting Challenge

Problem statement
Participants are tasked with forecasting campus-level photovoltaic (PV) energy generation for the next 15-minute interval across multiple university campuses. Given historical campus PV generation aggregated from site-level records and concurrent campus weather observations, build a model that generalizes across seasons and meteorological conditions.

Data files
- train.csv: Feature matrix with target values. Each row represents a campus–timestamp pair at 15-minute resolution. The target column name is "target" and represents the campus’s total PV generation for that interval. Features include weather, geospatial, and time-derived variables.
- test.csv: Feature matrix without target values, following the same schema as train.csv except the absence of the target column. Each row has a unique "row_id" for submission alignment.
- sample_submission.csv: Example submission showing required format and realistic random values.

Features and target
- Target (train.csv only): target — campus-level total PV generation (sum of site-level generation) for the interval.
- Keys: row_id (test.csv only), CampusKey, Timestamp (all files).
- Weather features: ApparentTemperature, AirTemperature, DewPointTemperature, RelativeHumidity, WindSpeed, WindDirection (aligned and downsampled/aggregated to 15-minute resolution).
- Time features: minute_of_day, day_of_year, year, is_weekend.
- Campus geospatial and composition features: campus_lat, campus_lon (mean across campus sites), site_count (number of PV sites on the campus).

Task
- Process and engineer features from weather and calendar information.
- Aggregate site-level generation into campus-level targets.
- Train a model to predict next-interval campus PV generation based on available features.

Split protocol
- Chronological split: training spans January 1, 2020 through December 31, 2021. Testing spans January 1, 2022 through the end of the dataset (April 2022). All campuses present in the test set also appear in the training set.

Evaluation metric
- Primary score: campus-normalized mean absolute error (NMAE).
- Computation:
  1) Compute each campus’s training-period normalization constant as the 95th percentile of its target values in train.csv.
  2) For each campus, compute MAE over all of its test rows.
  3) Normalize each campus’s MAE by its constant from step (1).
  4) Average the normalized MAEs equally across campuses to obtain the final score.
- Notes: This normalization accounts for campus capacity differences and promotes fair comparison. The metric is robust to missingness and scales; safeguards prevent division by zero.

Submission format
- A CSV file with two columns: row_id and target.
- row_id must exactly match the identifiers in test.csv.
- target must be numeric (floats permitted). Negative values are allowed by the validator, but PV is non-negative, so sensible models should predict ≥0.

Recommendations
- Use lag features from training history only (e.g., t−1, t−4, rolling means) to capture temporal dynamics while respecting chronology.
- Consider feature interactions and non-linear models such as gradient boosting or sequence models.
- Address missing data carefully; timestamps without numeric generation in training are excluded from the target construction.

This challenge demands robust data processing, feature engineering, and modeling to deliver accurate, campus-normalized near-term PV forecasts.
