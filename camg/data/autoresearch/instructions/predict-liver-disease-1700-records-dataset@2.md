# OpenMLE-fast task

Task ID: `predict-liver-disease-1700-records-dataset@2`

Native metric: `LiverDiseaseRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1364 bytes)
- `data/sample_submission.csv` (7661 bytes); columns: ["Id", "LiverFunctionTest"]
- `data/test.csv` (24639 bytes); columns: ["Id", "Age", "Gender", "BMI", "AlcoholConsumption", "Smoking", "GeneticRisk", "PhysicalActivity", "Diabetes", "Hypertension"]
- `data/train.csv` (122823 bytes); columns: ["Id", "Age", "Gender", "BMI", "AlcoholConsumption", "Smoking", "GeneticRisk", "PhysicalActivity", "Diabetes", "Hypertension", "LiverFunctionTest"]

## Public description

Task
Predict the continuous LiverFunctionTest value using only non-invasive features.

Files
- train.csv: Id + features + LiverFunctionTest
- test.csv: Id + features (no target)
- sample_submission.csv: Example submission format with random but valid predictions

Features
- Age (years)
- Gender (0/1)
- BMI (kg/m^2)
- AlcoholConsumption (units/week)
- Smoking (0/1)
- GeneticRisk (0/1/2)
- PhysicalActivity (hours/week)
- Diabetes (0/1)
- Hypertension (0/1)

Target
- LiverFunctionTest: a quantitative lab value (approximately in the 20–100 range)

Evaluation
- Mean Absolute Error (MAE) between your predictions and the ground truth.
- Lower MAE is better.

Rules and notes
- Do not use any information beyond the provided features in train/test.
- Do not assume column order; rely on column names.
- Fit any preprocessing (e.g., scaling/encoding/imputation) on training data only.
- You may use cross-validation within train.csv; the test set is held out.
- Ids in your submission must match test.csv exactly and be unique.

Submission format
- CSV with two columns, no header changes:
  - Id, LiverFunctionTest

Recommended workflow
- Explore feature relationships, interactions, and non-linearities.
- Consider robust models (e.g., gradient boosting, random forests, regularized regression).
- Calibrate and validate using CV; report the best model on test.
