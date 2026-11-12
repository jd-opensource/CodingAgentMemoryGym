# OpenMLE-fast task

Task ID: `lung-capacity-of-kids@1`

Native metric: `LungCapacityRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2085 bytes)
- `data/sample_submission.csv` (3260 bytes); columns: ["Id", "LungCap"]
- `data/test.csv` (3532 bytes); columns: ["Id", "Age", "Height", "Smoke", "Gender", "Caesarean"]
- `data/train.csv` (14846 bytes); columns: ["Age", "Height", "Smoke", "Gender", "Caesarean", "LungCap"]

## Public description

Title: Predict Lung Capacity of Kids from Demographics and Habits

Problem statement
- Build a machine learning model that estimates a child’s measured lung capacity (LungCap) from demographic and lifestyle features. The dataset covers ages 3–19 with gender, smoking status, birth via caesarean, and height.

What you are given
- Train data: feature columns plus the target column LungCap.
- Test data: the same feature columns without LungCap, with an Id column for correspondence.
- A sample_submission file: Id and LungCap (predicted) with random but valid values.

Task
- Predict LungCap for all rows in the test set and submit a CSV with columns: Id, LungCap.

Features and target
- Features:
  - Age (years, integer)
  - Height (inches, real number)
  - Smoke (yes/no)
  - Gender (male/female)
  - Caesarean (yes/no)
- Target:
  - LungCap (continuous, real-valued)

Modeling guidance (optional)
- Data processing: parse categorical fields robustly; ensure no missing values and valid categories.
- Feature engineering: consider interactions (e.g., Age×Height), nonlinear terms (e.g., Height^2), and subgroup effects (e.g., Smoke×Height).
- Scaling: standardize numeric features (Age, Height) when using linear or distance-based models.
- Validation: use robust cross-validation; minority groups (smokers) are smaller, so pay attention to subgroup generalization.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on LungCap across the full test set.
  - RMSE = sqrt(mean((y_true − y_pred)^2)).
  - The submission must contain exactly the test Ids once each; predictions must be finite numeric values.
  - Order of rows in the submission does not affect scoring (Ids are used to align).

Final files provided
- train.csv
- test.csv
- sample_submission.csv

Submission format
- CSV with header and exactly two columns in this order:
  - Id
  - LungCap

Notes
- Use all the data: the train/test split preserves the distribution of Age (in 2-year bins) and Smoke status.
- The dataset is clean; there are no missing values. Numerical care matters for RMSE (avoid NaN/Inf).
