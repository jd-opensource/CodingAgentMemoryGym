# OpenMLE-fast task

Task ID: `energy-consumption-dataset-linear-regression@2`

Native metric: `EnergyConsumptionRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2011 bytes)
- `data/sample_submission.csv` (1416 bytes); columns: ["row_id", "Energy Consumption"]
- `data/test.csv` (2113 bytes); columns: ["row_id", "Square Footage", "Number of Occupants", "Appliances Used", "Average Temperature"]
- `data/train.csv` (29330 bytes); columns: ["row_id", "Square Footage", "Number of Occupants", "Appliances Used", "Average Temperature", "Energy Consumption"]

## Public description

Competition: Privacy-Constrained Energy Forecasting

Problem statement
- Goal: Predict daily Energy Consumption for buildings using only non-sensitive numeric signals. You are given building size, occupancy, appliance count, and environmental temperature; sensitive identifiers (e.g., Building Type, Day of Week) are intentionally excluded to mimic privacy-limited deployments.
- Task type: Tabular regression.

Provided files
- train.csv: Training data with columns
  - row_id: Unique row identifier
  - Square Footage (numeric)
  - Number of Occupants (numeric)
  - Appliances Used (numeric)
  - Average Temperature (numeric)
  - Energy Consumption (numeric target)
- test.csv: Test data with the same feature columns and row_id (no Energy Consumption column)
- sample_submission.csv: Example submission with the expected format

What you need to do
- Train a model using train.csv to predict Energy Consumption for each row in test.csv.
- Submit a CSV with columns [row_id, Energy Consumption], covering all rows in test.csv.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the hidden ground truth.
  - MAE = mean(|y_true − y_pred|)
  - Lower is better.
  - Predictions must be numeric and finite. Rows are matched on row_id.

Notes and recommendations
- Only numeric features are provided to simulate privacy constraints; categorical identifiers are unavailable by design.
- Useful techniques include feature scaling, interaction terms, splines, gradient-boosted trees, random forests, regularized linear models, or neural nets.
- Consider modeling nonlinear effects of temperature and interactions with floor area, occupants, and appliance count.
- Outliers and heteroskedasticity management (robust loss, quantile targets, or transformations) may improve generalization.

Submission format
- CSV with exactly two columns: row_id, Energy Consumption
- row_id values must exactly match those in test.csv; order does not matter as long as all row_ids are present exactly once.
