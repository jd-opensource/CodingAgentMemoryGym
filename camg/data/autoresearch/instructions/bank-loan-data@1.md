# OpenMLE-fast task

Task ID: `bank-loan-data@1`

Native metric: `BankLoanRepaymentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (533 bytes)
- `data/sample_submission.csv` (135015 bytes); columns: ["id", "loan_status"]
- `data/test.csv` (721620 bytes); columns: ["id", "person_age", "person_gender", "person_education", "person_income", "person_emp_exp", "person_home_ownership", "loan_amnt", "loan_intent", "loan_percent_income", "cb_person_cred_hist_length", "credit_score"]
- `data/train.csv` (2957633 bytes); columns: ["id", "person_age", "person_gender", "person_education", "person_income", "person_emp_exp", "person_home_ownership", "loan_amnt", "loan_intent", "loan_percent_income", "cb_person_cred_hist_length", "credit_score", "loan_status"]

## Public description

Competition: Application-time Loan Repayment Risk (Binary Classification)

Files
- train.csv: Training data with id, features, and the target loan_status.
- test.csv: Test data with id and the same features (no loan_status).
- sample_submission.csv: Example submission with columns id and loan_status (probability of repayment).

Target
- loan_status: 1 if repaid, 0 if defaulted.

Evaluation
- ROC-AUC on loan_status. Submissions must contain exactly the same set of ids as in test.csv; loan_status must be a probability in [0, 1].
