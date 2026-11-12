# OpenMLE-fast task

Task ID: `common-heart-disease-data-4-hospitals@1`

Native metric: `HeartDiseaseGeneralizationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3824 bytes)
- `data/sample_submission.csv` (2874 bytes); columns: ["row_id", "target"]
- `data/test.csv` (7551 bytes); columns: ["row_id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
- `data/train.csv` (51658 bytes); columns: ["row_id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]

## Public description

Heart Disease Generalization Across Hospitals

Overview
Build a model to predict the probability of heart disease (target: 1=disease, 0=no disease) from routine clinical measurements. The dataset aggregates patient records collected across multiple hospitals, and the evaluation focuses on generalization to an unseen hospital domain with markedly different feature distributions and class balance.

Files provided
- train.csv: Training data with columns [row_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target].
- test.csv: Test data with columns [row_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal].
- sample_submission.csv: Example submission with columns [row_id, target].

Task
- Learn to predict the probability of target=1 (heart disease) for each row in test.csv.
- Submit a CSV with two columns: [row_id, target], where target is a probability in [0, 1] for heart disease.

Important data characteristics
- Mixed types: numerical (age, trestbps, chol, thalach, oldpeak) and categorical/ordinal (sex, cp, fbs, restecg, exang, slope, ca, thal).
- Inconsistent encodings: Some categorical columns may contain decimal-like encodings due to source harmonization (e.g., slope ~ {1,2,3} with decimals like 1.2 or 2.6; thal spans codes around {3,6,7}; ca can appear in 0.2 steps). Normalizing these to canonical integer categories often helps.
- Missingness and odd values: In the test domain, chol may be recorded as 0 and should be treated as missing rather than physiologically valid. A few other values can be 0 but clinically plausible (e.g., oldpeak=0). Robust imputation and scaling can substantially improve performance.
- Distribution shift: The test set comes from a distinct hospital with strong covariate shift and skewed prevalence. Methods that are robust to shift (proper imputation, calibrated models, regularization, and well-chosen encodings) are beneficial.

Evaluation
- Metric: ROC-AUC on the test set using the submitted probabilities for target=1.
  - Why ROC-AUC: It is threshold-free and robust to prevalence shift and class imbalance in the evaluation domain, measuring ranking quality without relying on a fixed threshold.

Submission format
- A CSV file with two columns and no header changes:
  - row_id: integer identifier that uniquely matches a row in test.csv.
  - target: predicted probability (float in [0, 1]) that target=1.
- Do not reorder, drop, or duplicate row_id values. Your file must contain predictions for every row_id in test.csv exactly once.

Suggested approach (non-exhaustive)
- Data cleaning: Normalize categorical encodings (e.g., round or map slope to {1,2,3}, restecg to {0,1,2}, thal to {3,6,7} if applicable; discretize ca to small integers), treat chol=0 as missing, and verify other edge cases (e.g., trestbps=0 is likely missing).
- Imputation: Use robust strategies (median, iterative, or model-based). Ensure any parameters are learned from training data only and applied to test data.
- Scaling: Robust scaling of continuous features (median/IQR) mitigates outliers.
- Modeling: Try calibrated logistic regression, gradient boosting, random forests, or other tabular ML methods. Consider class imbalance handling and calibration.
- Validation: Because the evaluation domain differs, use group-aware or domain-aware validation strategies (e.g., hospital-based split within training domains if you simulate), and avoid leakage from any columns that trivially indicate domain.

Reproducibility and constraints
- The provided row_id is the only identifier to use for submission alignment.
- No additional external data is required.

Deliverables
- Final submission: CSV file named as you wish, with columns [row_id, target], containing a probability for each row in test.csv.
