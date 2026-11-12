# OpenMLE-fast task

Task ID: `credit-card-dataset-comprehensive@1`

Native metric: `CreditDefaultMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3987 bytes)
- `data/sample_submission.csv` (90868 bytes); columns: ["Customer_ID", "Defaulted"]
- `data/test.csv` (383950 bytes); columns: ["Customer_ID", "Age", "Gender", "Marital_Status", "Education_Level", "Employment_Status", "Annual_Income", "Credit_Score", "Number_of_Credit_Lines", "Credit_Utilization_Ratio", "Debt_To_Income_Ratio", "Number_of_Late_Payments", "Tenure_in_Years", "Total_Transactions_Last_Year", "Total_Spend_Last_Year", "CLV", "Total_Transactions", "Avg_Transaction_Amount", "Max_Transaction_Amount", "Min_Transaction_Amount", "Fraud_Transactions", "Unique_Merchant_Categories", "Unique_Transaction_Cities"]
- `data/train.csv` (909315 bytes); columns: ["Customer_ID", "Age", "Gender", "Marital_Status", "Education_Level", "Employment_Status", "Annual_Income", "Credit_Score", "Number_of_Credit_Lines", "Credit_Utilization_Ratio", "Debt_To_Income_Ratio", "Number_of_Late_Payments", "Tenure_in_Years", "Total_Transactions_Last_Year", "Total_Spend_Last_Year", "Defaulted", "CLV", "Total_Transactions", "Avg_Transaction_Amount", "Max_Transaction_Amount", "Min_Transaction_Amount", "Fraud_Transactions", "Unique_Merchant_Categories", "Unique_Transaction_Cities"]

## Public description

```
description.txt (42 lines)
sample_submission.csv (3001 lines)
test.csv (3001 lines)
train.csv (7001 lines)```

-> sample_submission.csv has 3000 rows and 2 columns.
Here is some information about the columns:
Customer_ID (object) has 3000 unique values. Some example values: ['CUST_02450', 'CUST_04885', 'CUST_02626', 'CUST_01342']
Defaulted (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 3000 rows and 23 columns.
Here is some information about the columns:
Age (int64) has range: 21.00 - 69.00, 0 nan values
Annual_Income (int64) has range: 7758.00 - 111104.00, 0 nan values
Avg_Transaction_Amount (float64) has range: 194.66 - 981.77, 0 nan values
CLV (int64) has range: 1047.00 - 165151.00, 0 nan values
Credit_Score (int64) has range: 493.00 - 811.00, 0 nan values
Credit_Utilization_Ratio (float64) has range: 0.00 - 1.00, 0 nan values
Customer_ID (object) has 3000 unique values. Some example values: ['CUST_02450', 'CUST_04885', 'CUST_02626', 'CUST_01342']
Debt_To_Income_Ratio (float64) has range: 0.00 - 1.00, 0 nan values
Education_Level (object) has 4 unique values: ['Master', 'High School', 'PhD', 'Bachelor']
Employment_Status (object) has 3 unique values: ['Self-employed', 'Employed', 'Unemployed']
Fraud_Transactions (int64) has 5 unique values: [0, 1, 2, 3, 4]
Gender (object) has 2 unique values: ['Male', 'Female']
Marital_Status (object) has 3 unique values: ['Married', 'Divorced', 'Single']
Max_Transaction_Amount (float64) has range: 520.83 - 4862.98, 0 nan values
Min_Transaction_Amount (float64) has range: 0.01 - 282.00, 0 nan values
Number_of_Credit_Lines (int64) has 9 unique values: [6, 3, 7, 4, 2, 5, 8, 1, 9]
Number_of_Late_Payments (int64) has 6 unique values: [0, 2, 1, 3, 4, 5]
Tenure_in_Years (int64) has range: 0.00 - 29.00, 0 nan values
Total_Spend_Last_Year (int64) has range: 956.00 - 40685.00, 0 nan values
Total_Transactions (int64) has range: 6.00 - 37.00, 0 nan values
Total_Transactions_Last_Year (int64) has range: 10.00 - 199.00, 0 nan values
Unique_Merchant_Categories (int64) has 7 unique values: [8, 10, 9, 6, 7, 4, 5]
Unique_Transaction_Cities (int64) has range: 5.00 - 19.00, 0 nan values

-> train.csv has 7000 rows and 24 columns.
Here is some information about the columns:
Age (int64) has range: 21.00 - 69.00, 0 nan values
Annual_Income (int64) has range: 576.00 - 112128.00, 0 nan values
Avg_Transaction_Amount (float64) has range: 189.17 - 1172.91, 0 nan values
CLV (int64) has range: 990.00 - 170968.00, 0 nan values
Credit_Score (int64) has range: 469.00 - 832.00, 0 nan values
Credit_Utilization_Ratio (float64) has range: 0.00 - 1.00, 0 nan values
Customer_ID (object) has 7000 unique values. Some example values: ['CUST_00791', 'CUST_05190', 'CUST_02171', 'CUST_06263']
Debt_To_Income_Ratio (float64) has range: 0.00 - 1.00, 0 nan values
Defaulted (int64) has 2 unique values: [0, 1]
Education_Level (object) has 4 unique values: ['Master', 'High School', 'Bachelor', 'PhD']
Employment_Status (object) has 3 unique values: ['Employed', 'Self-employed', 'Unemployed']
Fraud_Transactions (int64) has 6 unique values: [0, 1, 4, 2, 3, 5]
Gender (object) has 2 unique values: ['Female', 'Male']
Marital_Status (object) has 3 unique values: ['Married', 'Single', 'Divorced']
Max_Transaction_Amount (float64) has range: 414.20 - 7096.24, 0 nan values
Min_Transaction_Amount (float64) has range: 0.00 - 376.01, 0 nan values
Number_of_Credit_Lines (int64) has 9 unique values: [1, 4, 5, 7, 2, 8, 6, 9, 3]
Number_of_Late_Payments (int64) has 8 unique values: [0, 1, 2, 3, 4, 5, 7, 6]
Tenure_in_Years (int64) has range: 0.00 - 29.00, 0 nan values
Total_Spend_Last_Year (int64) has range: 201.00 - 41128.00, 0 nan values
Total_Transactions (int64) has range: 7.00 - 37.00, 0 nan values
Total_Transactions_Last_Year (int64) has range: 10.00 - 199.00, 0 nan values
Unique_Merchant_Categories (int64) has 7 unique values: [9, 8, 7, 10, 6, 5, 4]
Unique_Transaction_Cities (int64) has range: 4.00 - 19.00, 0 nan values
