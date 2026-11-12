# OpenMLE-fast task

Task ID: `fake-bills@2`

Native metric: `FakeBillsRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2594 bytes)
- `data/sample_submission.csv` (6235 bytes); columns: ["id", "margin_low"]
- `data/test.csv` (10808 bytes); columns: ["id", "diagonal", "height_left", "height_right", "margin_up", "length"]
- `data/train.csv` (48793 bytes); columns: ["id", "diagonal", "height_left", "height_right", "margin_up", "length", "margin_low"]

## Public description

Competition: Margin Matters — Imputing Lower Margin from Banknote Geometry

Problem statement
Manufacturing of banknotes follows strict geometric rules. In real measurement campaigns, some readings are occasionally missing. Your task is to build a regression model that predicts the lower margin (margin_low, in millimeters) of a banknote from other geometric measurements.

Given five measurements — diagonal, height_left, height_right, margin_up, and length — predict margin_low for the test set.

Data description
- Each row corresponds to one banknote measurement.
- Columns provided to participants:
  - id: unique identifier of the banknote
  - diagonal: diagonal length (float)
  - height_left: left height (float)
  - height_right: right height (float)
  - margin_up: upper margin (float)
  - length: banknote length (float)
- Target to predict:
  - margin_low: lower margin (float)

Files
- train.csv: id, the five feature columns, and the target column margin_low.
- test.csv: id and the five feature columns (no margin_low).
- sample_submission.csv: example submission with id and margin_low columns.

Important notes
- The original dataset contained an authenticity flag and some missing targets. Only rows with observed margin_low are used. Any authenticity label is removed to prevent leakage. The task is purely about geometric imputation.
- All files are comma-separated UTF-8 CSVs. Decimal separator is a dot.

Evaluation
- Metric: Root Mean Squared Error (RMSE) between your predictions and the ground-truth margin_low on the test set.
- RMSE is defined as sqrt(mean((y_pred - y_true)^2)). Lower is better.
- Submissions must include exactly the columns: id, margin_low, with all ids from test.csv and no duplicates. Predictions must be finite real numbers.

Recommended approach
- Data processing: consistent parsing, optional robust scaling.
- Feature engineering (optional):
  - Symmetry: height_left - height_right; (height_left + height_right)/2
  - Geometry consistency: diagonal minus sqrt(height_*^2 + length^2)
  - Ratios: margin_up / length; interactions among length and heights
- Modeling: regularized linear models, tree ensembles, and model stacking can perform well.

Train/test split
- A single deterministic split is provided (80/20 on the rows with observed margin_low). The test set simulates missingness by withholding margin_low.

Submission format
- A valid submission is a CSV with two columns: id, margin_low
- The id values must match those in test.csv exactly; the margin_low values should be numeric floats.

Good luck and have fun imputation!
