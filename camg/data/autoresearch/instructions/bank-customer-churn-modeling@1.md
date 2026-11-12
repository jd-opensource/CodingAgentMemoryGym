# OpenMLE-fast task

Task ID: `bank-customer-churn-modeling@1`

Native metric: `BankCustomerChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2509 bytes)
- `data/sample_submission.csv` (26018 bytes); columns: ["CustomerId", "Exited"]
- `data/test.csv` (108036 bytes); columns: ["CustomerId", "CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
- `data/train.csv` (375281 bytes); columns: ["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]

## Public description

Bank Customer Churn Prediction

Problem statement
Banks aim to proactively retain customers who are likely to exit (churn) in the next cycle. Your task is to build a machine learning model that, given a customer’s profile and account attributes, outputs the probability that the customer will churn.

Data description
- Training data (train.csv): Contains features and the target label Exited (0/1).
- Test data (test.csv): Contains the same feature columns as the training data but without the target label. It also includes CustomerId to identify rows for submission.
- Submission format (sample_submission.csv): Must contain two columns: CustomerId and Exited, where Exited is the predicted probability of churn for that CustomerId.

Features
Use the following columns as features:
- CreditScore (numeric)
- Geography (categorical; e.g., France, Spain, Germany)
- Gender (categorical; Male/Female)
- Age (numeric)
- Tenure (numeric)
- Balance (numeric; zero values are valid)
- NumOfProducts (numeric; integer 1–4 inclusive; rare values present)
- HasCrCard (binary)
- IsActiveMember (binary)
- EstimatedSalary (numeric)

Target
- Exited (binary; 1 indicates churn, 0 indicates retention)

Notes and constraints
- Identifiers and non-behavioral columns are excluded from the feature set to avoid label leakage and unrealistic generalization.
- Class distribution is imbalanced (around 20% churn). Robust handling of imbalance, calibration, and ranking quality is encouraged.
- No external data is needed; focus on careful preprocessing, feature engineering, and modeling.

Evaluation metric
- Submissions are evaluated using ROC-AUC on the test set, computed from the submitted probabilities.
- Why ROC-AUC: It is threshold-independent, robust under class imbalance, and measures ranking quality across decision thresholds.

What to submit
- A CSV with columns: CustomerId and Exited (probability between 0 and 1).
- The CustomerId values must match those in the test data.

Final data files in this competition
- train.csv
- test.csv
- sample_submission.csv

Tips for participants
- Encode categorical variables (e.g., one-hot for Geography and Gender).
- Consider interactions and non-linear relationships (e.g., Geography × Balance × IsActiveMember).
- Handle imbalance with appropriate techniques (class weights, calibrated probabilities, thresholding strategies).
- Avoid overfitting to rare categories and constant patterns.
- Validate preprocessing to ensure no NaN/Inf values are introduced.
