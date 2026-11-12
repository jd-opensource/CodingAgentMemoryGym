# OpenMLE-fast task

Task ID: `city-typeseda-and-model@1`

Native metric: `CityTypeClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2528 bytes)
- `data/sample_submission.csv` (360107 bytes); columns: ["id", "Type"]
- `data/test.csv` (1134832 bytes); columns: ["id", "Date", "CO", "NO2", "SO2", "O3", "PM2_5", "PM10"]
- `data/train.csv` (2696360 bytes); columns: ["id", "Date", "CO", "NO2", "SO2", "O3", "PM2_5", "PM10", "Type"]

## Public description

City Type Generalization from Air-Quality Traces

Problem statement
Urban emissions and activity patterns differ between industrial and residential areas. You are given hourly air-quality measurements and timestamps. Your task is to predict the area Type (Industrial vs Residential) for held-out rows from unseen cities. The provided data intentionally omits any city identifier to avoid trivial leakage. Generalize from learned temporal and pollutant patterns rather than memorizing cities.

Files
- train.csv: Labeled training rows.
- test.csv: Unlabeled test rows with the same schema as train.csv (minus the target).
- sample_submission.csv: Example submission with random but valid labels.

Columns
- id: Unique row identifier.
- Date: Timestamp string (UTC). You may engineer time features (hour, day-of-week, month, cyclic encodings, etc.).
- CO, NO2, SO2, O3, PM2_5, PM10: Air pollutant concentration features.
- Type: Target label in train.csv only. One of {Industrial, Residential}.

Task and constraints
- Learn to classify Type for test rows. City identifiers are not provided; do not attempt to reconstruct them. Use pollutant levels and temporal patterns.
- All data is hourly and spans a full year across multiple cities. The split is by city: test rows come from cities not present in the training set.

Evaluation
- Metric: Macro-averaged F1 score over the two classes (Industrial, Residential).
  - For each class c, F1_c = 2 * (precision_c * recall_c) / (precision_c + recall_c), with 0 when the denominator is 0.
  - Final score is the mean of F1 over both classes.
  - Predictions must be the exact string labels Industrial or Residential.

Submission format
- A CSV file with exactly two columns and a header: id,Type
- id must match the ids in test.csv (order is arbitrary). Each id must appear exactly once.
- Type must be one of: Industrial, Residential.

Modeling guidance (non-binding)
- Consider feature engineering from Date (hour-of-day, day-of-week, month, seasonal sin/cos) and interactions among pollutants.
- Fit scalers/encoders using only training data. Use robust validation (e.g., time-aware folds or group-by-city folds if you simulate).
- Gradient boosting trees, linear models with regularization, and shallow neural nets can all work well on tabular time-series features.

Data integrity
- No missing values are expected. All pollutant features and timestamps are provided for both train and test.

Good luck, and focus on learning domain-robust patterns that transfer to unseen cities!
