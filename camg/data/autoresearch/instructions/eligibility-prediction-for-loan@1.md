# OpenMLE-fast task

Task ID: `eligibility-prediction-for-loan@1`

Native metric: `LoanEligibilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2389 bytes)
- `data/sample_submission.csv` (3327 bytes); columns: ["Loan_ID", "Loan_Status"]
- `data/test.csv` (11154 bytes); columns: ["Loan_ID", "Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]
- `data/train.csv` (26470 bytes); columns: ["Loan_ID", "Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area", "Loan_Status"]

## Public description

Real-time Loan Eligibility Scoring

Problem statement
Dream Housing Finance aims to automate home-loan eligibility screening at application time. Given an applicant’s profile captured in the application form, predict the probability that their loan will be approved.

Task
Build a model that outputs the probability of approval (Loan_Status = Y) for each application in the test set.

Data
You are provided tabular application data split for training and testing:
- train.csv: includes the target column Loan_Status.
- test.csv: the same features without the target.
- sample_submission.csv: an example submission file.

Feature columns
- Loan_ID: unique identifier (use only as the key in your submission).
- Gender: Male/Female.
- Married: Yes/No.
- Dependents: number of dependents (values such as 0, 1, 2, 3+).
- Education: Graduate/Not Graduate.
- Self_Employed: Yes/No.
- ApplicantIncome: numeric.
- CoapplicantIncome: numeric.
- LoanAmount: loan amount in thousands (numeric).
- Loan_Amount_Term: loan term in months (numeric).
- Credit_History: meets guidelines (1/0; numeric).
- Property_Area: Urban/Semiurban/Rural.
- Loan_Status: target in train.csv only (Y/N).

Important notes
- The raw data contains missing values and minor inconsistencies (e.g., whitespace variants). Thoughtful preprocessing is important.
- Stratification preserves class balance across train/test. All classes present in test also appear in train.
- Use all available features except Loan_ID for modeling.

Submission format
- A single CSV with two columns named exactly:
  - Loan_ID: the identifier from test.csv.
  - Loan_Status: the predicted probability that the loan is approved (Y), a number between 0 and 1 for each row.

Evaluation
- Metric: Binary Log Loss on the probability of approval (Y).
- Lower is better. This proper scoring rule rewards well-calibrated probabilities and is robust to class imbalance.

Guidance for participants
- Recommended preprocessing: clean categorical values, handle missing data (e.g., median/mode imputation), and ensure numeric types where appropriate.
- Feature engineering ideas: affordability ratios (e.g., EMI and Income-to-EMI), log transforms for skewed monetary features, interactions with Credit_History and Property_Area.
- Models: logistic regression with regularization, tree ensembles, and calibrated boosting typically work well on tabular data.
