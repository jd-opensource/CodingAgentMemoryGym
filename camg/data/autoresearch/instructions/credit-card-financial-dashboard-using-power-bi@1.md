# OpenMLE-fast task

Task ID: `credit-card-financial-dashboard-using-power-bi@1`

Native metric: `CreditCardDelinquencyMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (377 bytes)
- `data/sample_submission.csv` (28334 bytes); columns: ["Client_Num", "Delinquent_Acc"]
- `data/test.csv` (341932 bytes); columns: ["Client_Num", "Card_Category", "Annual_Fees", "Activation_30_Days", "Customer_Acq_Cost", "Week_Start_Date", "Week_Num", "Qtr", "current_year", "Credit_Limit", "Total_Revolving_Bal", "Total_Trans_Amt", "Total_Trans_Vol", "Avg_Utilization_Ratio", "Use Chip", "Exp Type", "Interest_Earned", "Customer_Age", "Gender", "Dependent_Count", "Education_Level", "Marital_Status", "state_cd", "Zipcode", "Car_Owner", "House_Owner", "Personal_loan", "contact", "Customer_Job", "Income", "Cust_Satisfaction_Score"]
- `data/train.csv` (1380350 bytes); columns: ["Client_Num", "Card_Category", "Annual_Fees", "Activation_30_Days", "Customer_Acq_Cost", "Week_Start_Date", "Week_Num", "Qtr", "current_year", "Credit_Limit", "Total_Revolving_Bal", "Total_Trans_Amt", "Total_Trans_Vol", "Avg_Utilization_Ratio", "Use Chip", "Exp Type", "Interest_Earned", "Delinquent_Acc", "Customer_Age", "Gender", "Dependent_Count", "Education_Level", "Marital_Status", "state_cd", "Zipcode", "Car_Owner", "House_Owner", "Personal_loan", "contact", "Customer_Job", "Income", "Cust_Satisfaction_Score"]

## Public description

Credit Card Delinquency Risk Prediction

Files in this public directory:
- train.csv: Labeled training data with features and the target column Delinquent_Acc.
- test.csv: Unlabeled test data with the same feature schema as train.csv (without Delinquent_Acc).
- sample_submission.csv: Example submission with two columns: Client_Num and Delinquent_Acc (probabilities in [0,1]).
