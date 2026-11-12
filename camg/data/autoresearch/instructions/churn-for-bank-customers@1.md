# OpenMLE-fast task

Task ID: `churn-for-bank-customers@1`

Native metric: `BankCustomerChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2847 bytes)
- `data/sample_submission.csv` (8007 bytes); columns: ["Exited"]
- `data/test.csv` (90035 bytes); columns: ["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
- `data/train.csv` (375271 bytes); columns: ["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]

## Public description

Bank Customer Churn Prediction (Probability Ranking)

Overview
Banks lose substantial value when customers churn. Your task is to estimate the probability that each customer in the test set will exit the bank. Build a robust ML pipeline that processes the tabular features, engineers meaningful signals, and outputs calibrated churn probabilities.

Files provided
- train.csv: Training data with features and the target column Exited.
- test.csv: Test data with the same features as train.csv but without Exited.
- sample_submission.csv: A single-column example with the required submission format.

Features
- CreditScore (numeric)
- Geography (categorical: France, Germany, Spain)
- Gender (categorical: Male, Female)
- Age (numeric)
- Tenure (numeric)
- Balance (numeric; many exact zeros and a wide continuous range)
- NumOfProducts (integer; can be treated as numeric or categorical)
- HasCrCard (binary 0/1)
- IsActiveMember (binary 0/1)
- EstimatedSalary (numeric)

Identifier-like fields (RowNumber, CustomerId, Surname) have been removed from the final files to prevent leakage and non-generalizable shortcuts.

Objective
- Train a binary classifier to produce probability predictions in [0, 1] for Exited (1 = churn, 0 = stay).
- Focus on ranking quality under moderate class imbalance (~20% churn). Thoughtful feature engineering (e.g., Geography×Age interactions, zero-balance indicator, tenure/product usage patterns) can improve performance.

Submission format
- CSV with a single header column named Exited
- One probability per test row, in the same order as test.csv
- Values must be numeric and within [0, 1]

Evaluation
- Metric: ROC AUC computed on the full test set.
- Rationale: AUC is threshold-independent, robust to class imbalance, and rewards correct ranking. Predictions are validated for format and numerical stability; non-finite values are not allowed. If the test set were to contain a single class (not expected), the score is set to 0.5.

Data split
- Deterministic 80/20 split with stratification on the target and preservation of Geography distribution.
- Both classes occur in the training set, and all Geography values present in test also appear in train.

Notes and guidance
- There are no missing values in the provided files.
- Handle categorical variables via suitable encodings (e.g., one-hot).
- Consider class imbalance techniques (stratified CV, class weights, calibration, threshold tuning for offline validation).
- Strong tabular models (e.g., gradient boosting, regularized linear models) typically perform well; neural networks can also be effective with careful preprocessing.

Deliverable
- Submit a CSV containing one probability per test row under the single column Exited. High-quality solutions will pair careful preprocessing with interaction-aware models that rank churn risk precisely.
