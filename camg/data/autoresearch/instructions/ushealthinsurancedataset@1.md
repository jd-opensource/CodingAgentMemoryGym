# OpenMLE-fast task

Task ID: `ushealthinsurancedataset@1`

Native metric: `HealthInsurancePremiumMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2585 bytes)
- `data/sample_submission.csv` (7565 bytes); columns: ["id", "charges"]
- `data/test.csv` (10753 bytes); columns: ["id", "age", "sex", "bmi", "children", "smoker", "region"]
- `data/train.csv` (54239 bytes); columns: ["id", "age", "sex", "bmi", "children", "smoker", "region", "charges"]

## Public description

US Health Insurance Premium Prediction (RMSLE Challenge)

Problem statement:
Build a machine learning model to predict individual health insurance premium charges from tabular features describing demographic and lifestyle attributes. Models should generalize across heterogeneous subpopulations and handle the strong right-skew and heteroscedasticity in premium amounts.

Data description:
- Task type: Regression
- Features: age (numeric), sex (categorical), bmi (numeric), children (numeric), smoker (categorical), region (categorical)
- Target: charges (numeric). Present only in the training file.
- Files provided:
  - train.csv: id, features, and the target column charges
  - test.csv: id and features only (charges withheld)
  - sample_submission.csv: submission format example with id and predicted charges

Split protocol:
- Deterministic 80/20 train/test split with a fixed random seed
- Stratified by smoker and region to preserve group distributions
- The split is single-shot; no additional validation set is mandated

Submission format:
- CSV with two columns: id, charges
- The id values must exactly match those in test.csv and be present once each (no missing/duplicate ids)
- The charges column contains model predictions on the original scale (non-negative real numbers)

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) computed on charges
- Rationale:
  - RMSLE evaluates multiplicative error, suitable for right-skewed targets spanning orders of magnitude
  - Reduces outsized influence of extreme premiums while still penalizing large mistakes
  - Encourages consistent performance across low-cost (non-smoker) and high-cost (smoker) segments

RMSLE details:
- For each row i, let y_i be the true charge and p_i be the predicted charge (both >= 0)
- RMSLE = sqrt( mean( (log1p(p_i) - log1p(y_i))^2 ) )
- Submissions with negative, NaN, or infinite values in the charges column are invalid

Modeling guidance (optional, not enforced):
- Ensure robust preprocessing: type checks and handling of categorical features (e.g., one-hot)
- Consider feature engineering for nonlinear structure (e.g., smoker*bmi, age*bmi, bmi^2)
- Training on log(charges) and transforming back to the original scale can stabilize learning
- Use regularization and cross-feature interactions to mitigate overfitting on this small dataset

Deliverables:
- Submit a CSV matching sample_submission.csv’s structure: id, charges
- Keep the final predictions non-negative and aligned to test.csv ids

Good luck, and build models that are accurate and fair across all groups!
