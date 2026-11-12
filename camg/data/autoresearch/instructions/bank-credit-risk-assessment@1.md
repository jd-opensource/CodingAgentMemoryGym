# OpenMLE-fast task

Task ID: `bank-credit-risk-assessment@1`

Native metric: `BankCreditDelinquencyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2775 bytes)
- `data/sample_submission.csv` (27043 bytes); columns: ["ClientID", "DelinquencyBucket"]
- `data/test.csv` (440492 bytes); columns: ["ClientID", "Debt", "InitialLimit", "Income", "Term", "Sex", "Education", "CreditHistoryRating", "Region", "SettlementName", "IndustryName", "UnderageChildrenCount", "FamilyStatus", "Age"]
- `data/train.csv` (1777157 bytes); columns: ["ClientID", "Debt", "InitialLimit", "Income", "Term", "Sex", "Education", "CreditHistoryRating", "Region", "SettlementName", "IndustryName", "UnderageChildrenCount", "FamilyStatus", "Age", "DelinquencyBucket"]

## Public description

Bank Credit Delinquency Severity (Ordinal) Prediction

Problem statement
Banks must prioritize and manage delinquency risk. Your task is to predict each customer’s delinquency severity bucket using rich tabular data (demographics, credit terms, income, credit history, region, settlement, and industry). The target is an ordinal class derived from observed overdue days, aligning with real-world credit operations.

Target definition
- DelinquencyBucket (integer, ordinal 0–5), mapped from OverdueDays as:
  - 0: 0 days (On-time)
  - 1: 1–30 days
  - 2: 31–60 days
  - 3: 61–90 days
  - 4: 91–120 days
  - 5: >120 days

Files provided
- train.csv: features plus the target column DelinquencyBucket.
- test.csv: features only; no labels.
- sample_submission.csv: correct format example with random valid labels.

Columns in train.csv and test.csv
- ClientID: unique identifier for each customer (string/integer)
- Debt: current debt amount
- InitialLimit: initial credit limit
- Income: income amount
- Term: loan term (months)
- Sex: gender
- Education: education level
- CreditHistoryRating: credit history rating (categorical)
- Region: living area/region
- SettlementName: settlement/city/town name
- IndustryName: industry of employment
- UnderageChildrenCount: number of underage children
- FamilyStatus: marital/family status
- Age: age in years (engineered from birth date at a fixed snapshot)

Notes on features
- OverdueDays and any model-like scores (e.g., PDN, ScoringMark, VelcomScoring) are excluded to prevent target leakage.
- High-cardinality categoricals (e.g., SettlementName) are preserved to encourage robust encoding strategies.
- Missing values may exist and should be handled appropriately.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) on DelinquencyBucket (classes 0–5). Higher is better.
  - QWK accounts for the ordinal nature of the target and penalizes larger-distance errors more than adjacent ones.

Submission format
- A CSV file with two columns and no header changes:
  - ClientID
  - DelinquencyBucket (predicted integer class in {0,1,2,3,4,5})
- Each ClientID from test.csv must appear exactly once in the submission.
- Predicted labels must be valid integers in the allowed set.

Guidance (non-exhaustive)
- Data processing and cleaning, including handling missing values, numeric outliers, and category normalization.
- Feature engineering: robust transforms for skewed numerics, encodings for high-cardinality categoricals, and ordinal-aware modeling strategies.
- Model training: gradient boosting, linear models with encodings, or neural tabular methods.
- Model evaluation: use QWK locally to tune models and reduce large-distance misclassifications.

Deliverables
- train.csv
- test.csv
- sample_submission.csv
