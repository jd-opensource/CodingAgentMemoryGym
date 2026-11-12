# OpenMLE-fast task

Task ID: `california-ground-water-stations@1`

Native metric: `CaliforniaGroundwaterProgramMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2851 bytes)
- `data/sample_submission.csv` (179659 bytes); columns: ["id", "monitoring_program"]
- `data/test.csv` (1002176 bytes); columns: ["id", "latitude", "longitude", "gse", "rpe", "gse_method", "gse_acc", "basin_code", "basin_name", "county_name", "well_depth", "well_use", "well_type"]
- `data/train.csv` (4331095 bytes); columns: ["id", "latitude", "longitude", "gse", "rpe", "gse_method", "gse_acc", "basin_code", "basin_name", "county_name", "well_depth", "well_use", "well_type", "monitoring_program"]

## Public description

California Groundwater Monitoring Program Classification

Problem statement
- Given attributes of groundwater monitoring stations across California, predict which monitoring program each station belongs to.
- Target classes: CASGEM, SGMA, VOLUNTARY.
- This is a multi-class, imbalanced, tabular + geospatial classification task.

Files you will use
- train.csv: Training data with features and the target column monitoring_program.
- test.csv: Test data with the same features as train.csv but without the target. Contains an id column that uniquely identifies each test row.
- sample_submission.csv: A valid example submission with the required format and ids matching test.csv.

Columns included in train/test
- id: Unique identifier for each row (generated for this competition).
- latitude, longitude: Station latitude/longitude in decimal degrees.
- gse, rpe: Ground surface elevation and reference point elevation (feet), may be missing.
- gse_method, gse_acc: Elevation method and accuracy category (strings; may appear as Unknown).
- basin_code, basin_name: Groundwater basin identifiers.
- county_name: County name.
- well_depth: Reported well depth (feet), may be missing.
- well_use: Stated use category (e.g., Observation, Irrigation, Residential), may be missing.
- well_type: Construction/type descriptor, may be missing.
- monitoring_program (train only): The class label: CASGEM, SGMA, or VOLUNTARY.

What’s not included
- High-cardinality identifiers and sparsely populated administrative fields have been excluded to reduce spurious leakage and improve generalization.

Evaluation
- Metric: Macro-averaged F1 score across the three classes.
- Rationale: Classes are imbalanced, so macro F1 gives equal weight to each class and rewards models that perform well on minority classes.

Submission format
- A CSV file with exactly two columns and a header: id,monitoring_program
- id must match exactly the ids provided in test.csv (order does not matter; each id appears exactly once).
- monitoring_program must be one of: CASGEM, SGMA, VOLUNTARY.

Notes and guidance
- Handle missing values robustly. The strings Unknown and empty cells may indicate missingness.
- Consider geospatial feature engineering (e.g., interactions with basin/county, simple transforms of latitude/longitude).
- Elevation-related fields can be informative; entrants may derive rpe − gse or other robust transformations.
- Categorical encoding must be target-independent; do not leak label information from the training process into test data.
- The split is stratified by class to preserve label proportions. All classes present in test also occur in train.

Baseline expectations
- Simple encoders plus tree-based models should provide reasonable baselines. Strong solutions will combine careful preprocessing with robust modeling that handles imbalance.
