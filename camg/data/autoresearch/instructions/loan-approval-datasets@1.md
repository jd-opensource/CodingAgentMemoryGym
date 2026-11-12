# OpenMLE-fast task

Task ID: `loan-approval-datasets@1`

Native metric: `LoanApprovalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2520 bytes)
- `data/sample_submission.csv` (145279 bytes); columns: ["ID", "Approval"]
- `data/test.csv` (469210 bytes); columns: ["ID", "Text", "Income", "Credit_Score", "Loan_Amount", "DTI_Ratio"]
- `data/train.csv` (1914039 bytes); columns: ["ID", "Text", "Income", "Credit_Score", "Loan_Amount", "DTI_Ratio", "Approval"]

## Public description

Loan Approval Probability Challenge

Problem Statement
Predict the probability that a loan application is approved using both structured financial attributes and a short free‑text description provided by the applicant. Your task is to build a model that outputs calibrated probabilities for approval.

Files Provided
- train.csv: Labeled training data.
- test.csv: Unlabeled test data for prediction.
- sample_submission.csv: Example submission format.

Data Schema
All numeric values are real‑valued unless noted.
- ID: Unique identifier for each application.
- Text: Applicant’s short narrative describing loan purpose/situation.
- Income: Applicant’s total income.
- Credit_Score: Integer creditworthiness score.
- Loan_Amount: Requested loan amount.
- DTI_Ratio: Debt‑to‑Income ratio.
- Approval (train only): Binary target (1 = Approved, 0 = Rejected).

Important Notes
- Employment_Status is intentionally excluded from the final files to avoid a degenerate shortcut and encourage robust modeling across financial features and text.
- The text field is compact but informative; using both word and character n‑grams or transformer embeddings can improve performance.

Evaluation
- Metric: Average Precision (PR‑AUC) on the positive class (Approved = 1).
  - Why PR‑AUC: The dataset is imbalanced, and PR‑AUC emphasizes ranking quality for the minority class without requiring a fixed threshold.
- Submission Format:
  - A single CSV with two columns: ID and Approval.
  - Approval must be a numeric probability in [0, 1] indicating the likelihood of approval.
  - The file must contain exactly one row for each ID in test.csv.

Guidance and Suggestions
- Data Processing: Robust‑scale or standardize numeric features; carefully handle outliers (e.g., clip extreme DTI_Ratio or Loan_Amount) and ensure no leakage.
- Text Features: Clean and tokenize text; consider word and character n‑grams with TF‑IDF; optionally extract domain lexicons (e.g., medical, business, education, home, travel).
- Modeling: Strong baselines include logistic regression and gradient boosting on engineered features; multi‑modal fusion (tabular + text) often yields substantial gains.
- Calibration: Use Platt scaling or isotonic regression to improve probability quality.

Deliverables
- Submit a CSV named arbitrarily but with the required two columns (ID, Approval). The leaderboard ranks submissions by PR‑AUC.

Good luck, and have fun exploring multimodal modeling for real‑world financial decisions!
