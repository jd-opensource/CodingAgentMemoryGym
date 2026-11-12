# OpenMLE-fast task

Task ID: `churn-bank-customer@1`

Native metric: `BankCustomerChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2972 bytes)
- `data/sample_submission.csv` (29780 bytes); columns: ["CustomerId", "Exited"]
- `data/test.csv` (132268 bytes); columns: ["RowNumber", "CustomerId", "Surname", "CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
- `data/train.csv` (546339 bytes); columns: ["RowNumber", "CustomerId", "Surname", "CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary", "Exited"]

## Public description

Title: Bank Customer Churn Risk Ranking

Problem statement
You are given historical information on bank customers and must predict the probability that each customer in the test set will churn (Exited = 1). The objective is to rank customers by churn risk using well-calibrated probabilities.

Data description
The competition uses a single tabular dataset of 10,000 customers with mixed numeric and categorical features. The target label is Exited (binary: 1 indicates churn, 0 otherwise). The feature columns include a mixture of demographics and account attributes (e.g., credit score, geography, gender, age, tenure, balance, products, card ownership, activity, and estimated salary). Each row has a unique CustomerId which serves as the submission key.

Release files
- train.csv: Training data with all columns including Exited.
- test.csv: Test data with all columns except Exited.
- sample_submission.csv: A valid sample submission with CustomerId and predicted Exited probabilities in [0, 1].

Target and features
- Target: Exited (binary).
- Submission key: CustomerId.
- Feature types: Mixed numeric and categorical. Treat Geography and Gender as categorical; all other features are numeric. RowNumber and Surname exist but are not recommended for modeling.

Task expectations
Participants should apply the full ML pipeline: data processing, feature engineering, model training, and evaluation. Robust cross-validation, careful handling of categorical variables, interaction modeling, and class imbalance techniques are encouraged. Leakage prevention is important: do not use CustomerId, RowNumber, or Surname as predictive features.

Evaluation metric
- Primary metric: ROC AUC computed on Exited using the submitted probabilities.
- Why ROC AUC: It is threshold-independent, robust to the ~20% positive class imbalance, and directly measures how well you rank churners above non-churners.
- Submission format: A CSV with two columns: CustomerId and Exited, where Exited contains probabilities in [0, 1]. All CustomerId values in test.csv must be present exactly once.

Split and fairness
The train/test split is stratified by Exited with a fixed random seed to ensure reproducibility and maintain class balance. Additional guardrails ensure that the marginal distributions of Geography and Gender are preserved approximately in the test set to avoid unintended distribution shift.

Recommendations
- Encoding: One-hot or target/ordinal encoding for categorical variables (done within CV to avoid leakage).
- Scaling: Optional; often helpful for linear models but not required for tree-based methods.
- Class imbalance: Consider class weights, probability calibration, or resampling within CV.
- Interpretability: Techniques like SHAP or permutation importance can reveal the drivers of churn.

Files provided to participants
- train.csv
- test.csv
- sample_submission.csv

Submission
- Submit a single CSV with CustomerId and Exited (probabilities in [0, 1]).
