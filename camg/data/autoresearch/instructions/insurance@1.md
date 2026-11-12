# OpenMLE-fast task

Task ID: `insurance@1`

Native metric: `InsuranceChargesRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2506 bytes)
- `data/sample_submission.csv` (7386 bytes); columns: ["row_id", "charges"]
- `data/test.csv` (11375 bytes); columns: ["row_id", "age", "sex", "bmi", "children", "smoker", "region"]
- `data/train.csv` (40739 bytes); columns: ["age", "sex", "bmi", "children", "smoker", "region", "charges"]

## Public description

Title: Fair and Robust Medical Cost Regression

Problem statement:
- Predict individual medical insurance charges from demographic and lifestyle attributes. The target distribution is long-tailed with subgroup heterogeneity (e.g., smokers vs non-smokers) and interaction effects.

Data description:
- Features: age (numeric), sex (categorical), bmi (numeric), children (numeric count), smoker (categorical yes/no), region (categorical: northeast/northwest/southeast/southwest).
- Target: charges (numeric, positive).
- Files provided for the competition:
  - train.csv: Feature columns plus the target column charges.
  - test.csv: Feature columns only, without charges, with a row_id column to link submissions.
  - sample_submission.csv: Example submission containing row_id and a plausible charges prediction for each test row.

Train/test split:
- A single deterministic split preserves subgroup proportions by stratifying on smoker and region. Participants are free to use cross-validation on the training set; the public leaderboard uses only the provided test split.

Submission format:
- A CSV file with two columns:
  - row_id: integer identifiers corresponding to rows in test.csv.
  - charges: predicted insurance charges for each row in test.csv.
- The set of row_id values must exactly match those in test.csv, with no duplicates or missing entries.

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) between the predicted and ground-truth charges on the test set.
- Computation details:
  - Let y be the true charges and y_hat the predicted charges.
  - RMSLE = sqrt( mean( (log1p(y_hat) - log1p(y))^2 ) ).
  - Predictions must be non-negative and finite. The metric uses log1p for numerical stability and to accommodate potential zero values.

Guidance and modeling considerations:
- Handle categorical variables (sex, smoker, region) via appropriate encoding (e.g., one-hot, target encoding) inside cross-validation to avoid leakage.
- Consider interaction effects such as smoker × bmi and age × bmi, and nonlinear relationships (e.g., tree-based models, regularized GLMs, monotonic GBMs).
- Because charges are skewed and strictly non-negative, modeling log(charges) or using objectives tolerant to outliers (e.g., Huber loss) can improve robustness.
- Standardize or robust-scale numeric features (age, bmi, children) when using linear models.

Goal:
- Minimize RMSLE on the test set through careful data processing, feature engineering, model training, and evaluation.
