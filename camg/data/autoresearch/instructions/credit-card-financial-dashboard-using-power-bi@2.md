# OpenMLE-fast task

Task ID: `credit-card-financial-dashboard-using-power-bi@2`

Native metric: `CreditCardSatisfactionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5005 bytes)
- `data/sample_submission.csv` (24299 bytes); columns: ["Client_Num", "Cust_Satisfaction_Score"]
- `data/test.csv` (331040 bytes); columns: ["Client_Num", "Card_Category", "Annual_Fees", "Activation_30_Days", "Customer_Acq_Cost", "Week_Start_Date", "Week_Num", "Qtr", "Credit_Limit", "Total_Revolving_Bal", "Total_Trans_Amt", "Total_Trans_Vol", "Avg_Utilization_Ratio", "Use Chip", "Exp Type", "Interest_Earned", "Delinquent_Acc", "Customer_Age", "Gender", "Dependent_Count", "Education_Level", "Marital_Status", "state_cd", "Zipcode", "Car_Owner", "House_Owner", "Personal_loan", "contact", "Customer_Job", "Income"]
- `data/train.csv` (1340667 bytes); columns: ["Client_Num", "Card_Category", "Annual_Fees", "Activation_30_Days", "Customer_Acq_Cost", "Week_Start_Date", "Week_Num", "Qtr", "Credit_Limit", "Total_Revolving_Bal", "Total_Trans_Amt", "Total_Trans_Vol", "Avg_Utilization_Ratio", "Use Chip", "Exp Type", "Interest_Earned", "Delinquent_Acc", "Customer_Age", "Gender", "Dependent_Count", "Education_Level", "Marital_Status", "state_cd", "Zipcode", "Car_Owner", "House_Owner", "Personal_loan", "contact", "Customer_Job", "Income", "Cust_Satisfaction_Score"]

## Public description

```
description.txt (37 lines)
sample_submission.csv (2023 lines)
test.csv (2023 lines)
train.csv (8087 lines)```

-> sample_submission.csv has 2022 rows and 2 columns.
Here is some information about the columns:
Client_Num (int64) has range: 708082083.00 - 827888433.00, 0 nan values
Cust_Satisfaction_Score (int64) has 5 unique values: [1, 3, 4, 5, 2]

-> test.csv has 2022 rows and 30 columns.
Here is some information about the columns:
Activation_30_Days (int64) has 2 unique values: [1, 0]
Annual_Fees (int64) has range: 95.00 - 500.00, 0 nan values
Avg_Utilization_Ratio (float64) has range: 0.00 - 0.99, 0 nan values
Car_Owner (object) has 2 unique values: ['no', 'yes']
Card_Category (object) has 4 unique values: ['Blue', 'Silver', 'Gold', 'Platinum']
Client_Num (int64) has range: 708082083.00 - 827888433.00, 0 nan values
Credit_Limit (float64) has range: 1438.30 - 34516.00, 0 nan values
Customer_Acq_Cost (int64) has range: 40.00 - 171.00, 0 nan values
Customer_Age (int64) has range: 21.00 - 73.00, 0 nan values
Customer_Job (object) has 6 unique values: ['Selfemployeed', 'Blue-collar', 'Govt', 'Businessman', 'White-collar', 'Retirees']
Delinquent_Acc (int64) has 2 unique values: [0, 1]
Dependent_Count (int64) has 6 unique values: [0, 1, 2, 3, 4, 5]
Education_Level (object) has 6 unique values: ['High School', 'Graduate', 'Uneducated', 'Doctorate', 'Unknown', 'Post-Graduate']
Exp Type (object) has 6 unique values: ['Bills', 'Grocery', 'Food', 'Fuel', 'Travel', 'Entertainment']
Gender (object) has 2 unique values: ['M', 'F']
House_Owner (object) has 2 unique values: ['no', 'yes']
Income (int64) has range: 1250.00 - 239791.00, 0 nan values
Interest_Earned (float64) has range: 51.24 - 4785.00, 0 nan values
Marital_Status (object) has 3 unique values: ['Married', 'Single', 'Unknown']
Personal_loan (object) has 2 unique values: ['no', 'yes']
Qtr (object) has 4 unique values: ['Q2', 'Q4', 'Q1', 'Q3']
Total_Revolving_Bal (int64) has range: 0.00 - 2517.00, 0 nan values
Total_Trans_Amt (int64) has range: 510.00 - 18484.00, 0 nan values
Total_Trans_Vol (int64) has range: 13.00 - 128.00, 0 nan values
Use Chip (object) has 3 unique values: ['Swipe', 'Chip', 'Online']
Week_Num (object) has 52 unique values. Some example values: ['Week-37', 'Week-45', 'Week-24', 'Week-15']
Week_Start_Date (object) has 52 unique values. Some example values: ['10-09-2023', '05-11-2023', '11-06-2023', '09-04-2023']
Zipcode (int64) has range: 53010.00 - 99504.00, 0 nan values
contact (object) has 3 unique values: ['cellular', 'unknown', 'telephone']
state_cd (object) has 26 unique values. Some example values: ['CA', 'TX', 'NY', 'FL']

-> train.csv has 8086 rows and 31 columns.
Here is some information about the columns:
Activation_30_Days (int64) has 2 unique values: [1, 0]
Annual_Fees (int64) has range: 95.00 - 500.00, 0 nan values
Avg_Utilization_Ratio (float64) has range: 0.00 - 1.00, 0 nan values
Car_Owner (object) has 2 unique values: ['yes', 'no']
Card_Category (object) has 4 unique values: ['Blue', 'Silver', 'Gold', 'Platinum']
Client_Num (int64) has range: 708083283.00 - 827890758.00, 0 nan values
Credit_Limit (float64) has range: 1438.30 - 34516.00, 0 nan values
Cust_Satisfaction_Score (int64) has 5 unique values: [5, 2, 3, 1, 4]
Customer_Acq_Cost (int64) has range: 40.00 - 172.00, 0 nan values
Customer_Age (int64) has range: 21.00 - 67.00, 0 nan values
Customer_Job (object) has 6 unique values: ['Selfemployeed', 'Blue-collar', 'Businessman', 'White-collar', 'Govt', 'Retirees']
Delinquent_Acc (int64) has 2 unique values: [0, 1]
Dependent_Count (int64) has 6 unique values: [4, 0, 3, 1, 2, 5]
Education_Level (object) has 6 unique values: ['High School', 'Graduate', 'Doctorate', 'Unknown', 'Uneducated', 'Post-Graduate']
Exp Type (object) has 6 unique values: ['Grocery', 'Bills', 'Entertainment', 'Travel', 'Food', 'Fuel']
Gender (object) has 2 unique values: ['F', 'M']
House_Owner (object) has 2 unique values: ['yes', 'no']
Income (int64) has range: 1250.00 - 239639.00, 0 nan values
Interest_Earned (float64) has range: 42.14 - 4738.31, 0 nan values
Marital_Status (object) has 3 unique values: ['Unknown', 'Single', 'Married']
Personal_loan (object) has 2 unique values: ['no', 'yes']
Qtr (object) has 4 unique values: ['Q3', 'Q1', 'Q4', 'Q2']
Total_Revolving_Bal (int64) has range: 0.00 - 2517.00, 0 nan values
Total_Trans_Amt (int64) has range: 530.00 - 17744.00, 0 nan values
Total_Trans_Vol (int64) has range: 10.00 - 139.00, 0 nan values
Use Chip (object) has 3 unique values: ['Swipe', 'Chip', 'Online']
Week_Num (object) has 52 unique values. Some example values: ['Week-32', 'Week-7', 'Week-42', 'Week-8']
Week_Start_Date (object) has 52 unique values. Some example values: ['06-08-2023', '12-02-2023', '15-10-2023', '19-02-2023']
Zipcode (int64) has range: 53010.00 - 99504.00, 0 nan values
contact (object) has 3 unique values: ['cellular', 'unknown', 'telephone']
state_cd (object) has 28 unique values. Some example values: ['CA', 'TX', 'NY', 'FL']
