# OpenMLE-fast task

Task ID: `child-weight-at-birth-and-gestation-details@1`

Native metric: `BirthweightRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2262 bytes)
- `data/sample_submission.csv` (5544 bytes); columns: ["id", "bwt"]
- `data/test.csv` (7746 bytes); columns: ["id", "gestation", "parity", "age", "height", "weight", "smoke"]
- `data/train.csv` (35455 bytes); columns: ["id", "gestation", "parity", "age", "height", "weight", "smoke", "bwt"]

## Public description

Title: Birthweight Prediction from Gestation and Maternal Factors

Overview
Predict infant birthweight (in ounces) at delivery from gestational age and maternal factors. You are given a historical cohort with mixed numeric and binary predictors and realistic missing values. Build the most accurate regression model you can.

Files provided
- train.csv: Labeled training data with features and the target bwt.
- test.csv: Unlabeled test data with the same features as train.csv, except bwt is withheld.
- sample_submission.csv: Example submission file with the required format.

Columns
- id: Row identifier created for this competition (no semantics beyond identification).
- Features (predictors): gestation, parity, age, height, weight, smoke.
  - gestation: Gestational length (days).
  - parity: 0 if first baby, >0 otherwise (integer).
  - age: Maternal age (years).
  - height: Maternal height (inches).
  - weight: Maternal pre-pregnancy weight (pounds).
  - smoke: 1 if mother smoked during pregnancy, 0 otherwise.
- Target (train.csv only): bwt (infant birthweight, ounces).

Task
Train a regression model to predict bwt for the rows in test.csv and submit predictions in the required format.

Submission format
- A CSV file with exactly two columns and a header: id,bwt
- id must match the id values in test.csv exactly, with no missing or duplicate ids.
- bwt must be numeric and finite (no NaN/Inf).

Evaluation
- Root Mean Squared Error (RMSE) between your predictions and the true bwt.
- Lower RMSE is better. Ties are broken by smaller RMSE at full double precision.

Notes and recommendations
- The dataset contains genuine missing values in several predictors. Handle them carefully (e.g., imputation or models tolerant to missingness). Adding missing-indicator features can help.
- Consider nonlinear effects and interactions (e.g., gestation × smoking). Feature engineering or non-linear models (tree ensembles, GAMs) may improve performance.
- Standardization/regularization often helps due to correlated predictors.
- Use cross-validation on the training set to tune your approach. The test set is unseen and should not be used for model selection.
- The id column is provided only for row matching; do not assume any ordering or meaning.
