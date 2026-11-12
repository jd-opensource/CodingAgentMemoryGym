# OpenMLE-fast task

Task ID: `credit-score@1`

Native metric: `CreditScoreMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (524 bytes)
- `data/sample_submission.csv` (317679 bytes); columns: ["Id", "Credit_Score"]
- `data/test.csv` (3973631 bytes); columns: ["Id", "Delay_from_due_date", "Num_of_Delayed_Payment", "Num_Credit_Inquiries", "Credit_Utilization_Ratio", "Credit_History_Age", "Payment_of_Min_Amount", "Amount_invested_monthly", "Monthly_Balance", "Credit_Mix", "Payment_Behaviour", "Age", "Annual_Income", "Num_Bank_Accounts", "Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Monthly_Inhand_Salary", "Changed_Credit_Limit", "Outstanding_Debt", "Total_EMI_per_month"]
- `data/train.csv` (16465001 bytes); columns: ["Id", "Delay_from_due_date", "Num_of_Delayed_Payment", "Num_Credit_Inquiries", "Credit_Utilization_Ratio", "Credit_History_Age", "Payment_of_Min_Amount", "Amount_invested_monthly", "Monthly_Balance", "Credit_Score", "Credit_Mix", "Payment_Behaviour", "Age", "Annual_Income", "Num_Bank_Accounts", "Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Monthly_Inhand_Salary", "Changed_Credit_Limit", "Outstanding_Debt", "Total_EMI_per_month"]

## Public description

Competition: Credit Score Bracket Prediction

Files provided
- train.csv: Features and labels (includes Id and Credit_Score).
- test.csv: Features only (includes Id; does not include Credit_Score).
- sample_submission.csv: Template for submission with columns Id and Credit_Score.

Submission format
- CSV file with two columns: Id and Credit_Score.
- Id must match the Id values in test.csv.
- Credit_Score must be one of: Poor, Standard, Good.

Evaluation metric
- Macro-averaged F1 over the classes Poor, Standard, Good.
