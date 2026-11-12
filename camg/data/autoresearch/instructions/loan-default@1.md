# OpenMLE-fast task

Task ID: `loan-default@1`

Native metric: `LoanDefaultMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2604 bytes)
- `data/sample_submission.csv` (301320 bytes); columns: ["id", "repay_fail"]
- `data/test.csv` (2216792 bytes); columns: ["id", "member_id", "loan_amnt", "funded_amnt", "funded_amnt_inv", "term", "int_rate", "installment", "emp_length", "home_ownership", "annual_inc", "verification_status", "issue_d", "purpose", "zip_code", "addr_state", "dti", "delinq_2yrs", "earliest_cr_line", "inq_last_6mths", "mths_since_last_delinq", "open_acc", "pub_rec", "revol_bal", "revol_util", "total_acc", "credit_age_months"]
- `data/train.csv` (5332031 bytes); columns: ["id", "member_id", "loan_amnt", "funded_amnt", "funded_amnt_inv", "term", "int_rate", "installment", "emp_length", "home_ownership", "annual_inc", "verification_status", "issue_d", "purpose", "zip_code", "addr_state", "dti", "delinq_2yrs", "earliest_cr_line", "inq_last_6mths", "mths_since_last_delinq", "open_acc", "pub_rec", "revol_bal", "revol_util", "total_acc", "credit_age_months", "repay_fail"]

## Public description

Loan Default Risk Prediction

Problem statement
Predict the probability that a newly issued loan will default. For each loan record in the test set, submit a calibrated probability for the default outcome (repay_fail = 1). This task imitates application-time risk scoring used by financial institutions.

Data description
- Train data: tabular CSV with loan-level records including the binary target column repay_fail.
- Test data: tabular CSV with the same feature columns as train, excluding repay_fail.
- Unique identifier: id (stable per record). Include id in your submission to align predictions with test rows.

Features provided
Origination-time attributes typically available at application/issuance (no post-outcome leakage). Mixed numeric, categorical, and date fields:
- id, member_id, loan_amnt, funded_amnt, funded_amnt_inv, term, int_rate, installment, emp_length, home_ownership, annual_inc, verification_status, issue_d, purpose, zip_code, addr_state, dti, delinq_2yrs, earliest_cr_line, inq_last_6mths, mths_since_last_delinq, open_acc, pub_rec, revol_bal, revol_util, total_acc, credit_age_months
Notes and quirks you may need to handle:
- term is textual (e.g., "36 months", "60 months").
- percent-like fields (e.g., revol_util) may include % signs or non-ASCII characters.
- dates are month-year strings (e.g., "Nov-11"); credit_age_months is a derived numeric feature measuring months since earliest credit line at issuance.
- high-cardinality categorical columns include zip_code; ensure robust encoding.

Evaluation
- Metric: Average Precision (area under the precision–recall curve) on the default class.
- Submission format: CSV with two columns — id and repay_fail — where repay_fail is the predicted probability of default in [0,1].
- The scorer aligns predictions to the test set by id and computes Average Precision. Predictions are validated for format, duplicates, and numerical stability.

Train/test split
- Time-aware split to mimic production: train contains earlier issue months; test contains later issue months. Expect distribution shift and class imbalance.

Files
- train.csv: features + repay_fail
- test.csv: features (no repay_fail)
- sample_submission.csv: example submission with random but valid probabilities

What’s expected from participants
- Build a robust pipeline including data cleaning, feature engineering, model training, and evaluation.
- Handle mixed data types, class imbalance, missing values, and categorical encoding.
- Prevent leakage by relying exclusively on origination-time attributes; post-outcome variables are not present.
