# OpenMLE-fast task

Task ID: `predictive-maintenance-equipment-dataset-for-ml@1`

Native metric: `PredictiveMaintenanceMTTFMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2895 bytes)
- `data/sample_submission.csv` (10688 bytes); columns: ["UID", "MTTF"]
- `data/test.csv` (35805 bytes); columns: ["UID", "ProductType", "Humidity", "Temperature", "Age", "Quantity"]
- `data/train.csv` (158880 bytes); columns: ["UID", "ProductType", "Humidity", "Temperature", "Age", "Quantity", "MTTF"]

## Public description

Multi-Equipment Predictive Maintenance — MTTF Regression Challenge

Problem statement
- Production facilities operate a heterogeneous fleet of equipment (Pump, Extruder, Pressure Cutter, Gauge Machine, Coil Oven). Preventing unplanned downtime requires predicting mean time to failure (MTTF) from current operating conditions and machine characteristics.
- Given a tabular snapshot per equipment instance with ProductType, Humidity, Temperature, Age, and Quantity, your task is to predict the numeric MTTF.

Data description
- You are provided with:
  - train.csv: Each row corresponds to one equipment observation with columns [UID, ProductType, Humidity, Temperature, Age, Quantity, MTTF]. The target is MTTF.
  - test.csv: Same schema as train.csv but without the MTTF column. Columns: [UID, ProductType, Humidity, Temperature, Age, Quantity].
  - sample_submission.csv: A submission template with columns [UID, MTTF]. Use it to understand the required format; replace the MTTF values with your model predictions for the test set.
- Notes:
  - ProductType is categorical; Humidity and Temperature are floating-point; Age and Quantity are integers. UID is a unique identifier that must be preserved in the submission to align rows.
  - Column names are normalized (whitespace stripped). There are no missing values. All rows are usable.
  - The training and test sets jointly cover five equipment types and a broad range of operating conditions.

Task expectations
- Build an end-to-end ML solution:
  - Data processing: normalize column names, enforce types, handle the categorical feature ProductType (e.g., one-hot encoding or models that natively support categoricals).
  - Feature engineering: explore non-linearities and interactions (e.g., ProductType×sensor interactions), transformations, and regularization.
  - Model training: try robust tabular learners (e.g., gradient-boosted trees, regularized linear models with interaction terms, neural nets with categorical embeddings).
  - Model evaluation: validate your pipeline offline; the leaderboard is computed against the full test set using the metric below.

Evaluation metric
- The competition is evaluated using Root Mean Squared Error (RMSE) on MTTF.
  - RMSE = sqrt(mean((y_pred − y_true)^2))
  - RMSE penalizes large errors more strongly and preserves the native units of MTTF, making it a fair and precise measure for maintenance risk.
- Submissions must:
  - Be a CSV file with exactly two columns: [UID, MTTF].
  - Contain every UID from test.csv exactly once (no extras, no duplicates).
  - Use finite numeric values for MTTF (no NaN/inf).
- The evaluator aligns predictions to ground truth by UID to ensure correct pairing.

Final files provided
- train.csv: features and target for model development.
- test.csv: features only for generating predictions.
- sample_submission.csv: format reference for your upload.
