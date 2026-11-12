# OpenMLE-fast task

Task ID: `california-ground-water-stations@2`

Native metric: `GroundWaterDepthMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3079 bytes)
- `data/sample_submission.csv` (64439 bytes); columns: ["id", "well_depth"]
- `data/test.csv` (348755 bytes); columns: ["id", "swn", "latitude", "longitude", "gse", "rpe", "gse_method", "gse_acc", "basin_code", "basin_name", "county_name", "well_use", "well_type", "monitoring_program", "rpe_minus_gse"]
- `data/train.csv` (1461489 bytes); columns: ["id", "swn", "latitude", "longitude", "gse", "rpe", "gse_method", "gse_acc", "basin_code", "basin_name", "county_name", "well_use", "well_type", "monitoring_program", "rpe_minus_gse", "well_depth"]

## Public description

California Ground Water Stations: Well Depth Estimation Challenge

Problem statement
Build a machine learning model to estimate well depth (in feet) for groundwater monitoring stations across California using station metadata and geospatial attributes. The task is a supervised regression problem on tabular data.

Data description
- Train data file: train.csv
  - Columns: station features and the target well_depth.
  - Features include numeric and categorical fields like latitude, longitude, gse, rpe, rpe_minus_gse, gse_method, gse_acc, basin_code, basin_name, county_name, well_use, well_type, monitoring_program, and swn (if present). Identifier-like fields that do not generalize (e.g., site_code, stn_id, well_name, wcr_no, continuous_data_station_number) are excluded from the provided features.
  - Target: well_depth (feet), a non-negative real number.
  - An id column is included for reference (an anonymized integer); do not use it as a predictive feature.
- Test data file: test.csv
  - Columns: the same station features as train.csv plus id; well_depth is not included.
- Sample submission: sample_submission.csv
  - Columns: id, well_depth
  - The id must match those in test.csv; well_depth is your predicted value in feet.

Data notes
- Missing values: The string "Unknown" and empty cells represent missing entries in the source and are left as-is (as NaN) for participants to handle.
- Derived feature: rpe_minus_gse = rpe − gse is included to capture elevation-reference differences.
- Deduplication: Exact duplicate stations by the key (latitude, longitude, basin_name, county_name) are removed prior to splitting to reduce leakage from near-duplicates.
- Split: A single deterministic 80/20 train/test split is used, drawn from the subset of stations with known well_depth.

Evaluation
- Metric: Mean Absolute Error (MAE) on well_depth.
- Rationale: MAE is robust to outliers and measures average error in physically interpretable units (feet), ensuring a fair comparison across a heavy-tailed depth distribution.

What you can use
- Any standard ML techniques for tabular regression: missing-value handling, encoding categorical variables, feature engineering (e.g., rpe − gse), geospatial transforms, model training and ensembling.
- External data is not required; the challenge is designed to be solvable using the provided files.

Submission format
- Provide a CSV file with exactly two columns in this order: id, well_depth.
- The id values must match those in test.csv in the same order; do not add or remove rows.
- Predictions must be finite numeric values (non-negative values are physically consistent).

Tips and considerations
- Treat "Unknown" and blank cells as missing.
- Categorical spaces are broad (hundreds of basins, dozens of counties). Ensure robust encoding and consider rare-category handling.
- Elevation-derived features (gse and rpe) can be informative. Consider interactions and non-linear models.
- Latitude/longitude encode geospatial context; you may derive additional geospatial features without external shapefiles.
