# OpenMLE-fast task

Task ID: `heartdisease-datasets@1`

Native metric: `HeartDiseaseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2766 bytes)
- `data/sample_submission.csv` (472 bytes); columns: ["id", "target"]
- `data/test.csv` (2429 bytes); columns: ["id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
- `data/train.csv` (9913 bytes); columns: ["id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]

## Public description

Heart Disease Risk: Robust Modeling on Small Tabular Data

Problem statement
Participants are tasked with predicting the probability that a patient has heart disease from clinical tabular features. The goal is to build models that generalize well to unseen patients while handling a small sample size, mixed feature types, and potential non-linear interactions.

Data description
- Training data: train.csv
  - Columns: id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target
  - target is a binary label: 1 indicates presence of heart disease, 0 indicates absence.
- Test data: test.csv
  - Columns: id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
  - No target column is provided.
- Sample submission: sample_submission.csv
  - Columns: id, target
  - target holds example prediction probabilities in [0,1].

Feature notes
- Mixed types:
  - Continuous: age, trestbps, chol, thalach, oldpeak
  - Integer-coded categorical: sex, cp, fbs, restecg, exang, slope, ca, thal (treat as categorical if helpful)
- No missing values are explicitly provided; retain all rows. If you choose to treat specific codes (e.g., thal==0) as an “unknown” category, that is acceptable.

Evaluation
- Metric: ROC AUC on the full test set.
- Submission format: A single CSV with columns:
  - id: integer identifier matching rows in test.csv
  - target: predicted probability of heart disease (float in [0,1])
- Ties and probability calibration are handled implicitly by the ROC AUC; only ranking quality matters.

Train/test split
- Provided by the host as a deterministic, stratified 80/20 split to preserve class proportions. No validation split is provided; use cross-validation on the training set as needed.

Recommended approach
- Data processing: standardize continuous variables; encode categorical codes (e.g., one-hot, target encoding) with care to avoid leakage.
- Feature engineering: consider interactions (e.g., cp with exang, oldpeak, slope), non-linear transforms, and monotonic constraints if using gradient boosting.
- Modeling: try regularized logistic regression, tree ensembles (GBDT, Random Forest), calibrated SVMs, and stacking/blending. Use robust cross-validation (e.g., stratified K-fold) and early stopping where applicable.
- Evaluation: tune hyperparameters using cross-validation ROC AUC; check stability across folds; assess calibration if you plan to interpret probabilities.

Files provided
- train.csv: training features and labels
- test.csv: test features only
- sample_submission.csv: example submission with valid structure

Your goal
Maximize ROC AUC on the test set by building a strong and well-validated model that generalizes under small-sample constraints.
