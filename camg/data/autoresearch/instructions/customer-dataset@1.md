# OpenMLE-fast task

Task ID: `customer-dataset@1`

Native metric: `CustomerResponseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5784 bytes)
- `data/sample_submission.csv` (48347 bytes); columns: ["Customer_ID", "Campaign_Response"]
- `data/test.csv` (307445 bytes); columns: ["Customer_ID", "Birth_Year", "Education_Level", "Marital_Status", "Annual_Income", "Kids_Home", "Teens_Home", "Customer_Since", "Last_Purchase_Recency", "Spent_Wine", "Spent_Fruits", "Spent_Meat", "Spent_Fish", "Spent_Sweets", "Spent_Gold", "Deals_Purchased", "Web_Purchases", "Catalog_Purchases", "Store_Purchases", "Monthly_Web_Visits", "Campaign1_Accepted", "Campaign2_Accepted", "Campaign3_Accepted", "Campaign4_Accepted", "Campaign5_Accepted", "Filed_Complaint", "Contact_Cost", "Revenue_Contribution", "Country", "City", "Region_Code", "Mobile_App_User", "Email_Subscriber", "Device_Type", "Referred_By_Friend", "Social_Media_User", "Membership_Tier", "Total_Amount_Spent", "Customer_Age", "Family_Size", "Senior_Citizen"]
- `data/train.csv` (1245058 bytes); columns: ["Customer_ID", "Birth_Year", "Education_Level", "Marital_Status", "Annual_Income", "Kids_Home", "Teens_Home", "Customer_Since", "Last_Purchase_Recency", "Spent_Wine", "Spent_Fruits", "Spent_Meat", "Spent_Fish", "Spent_Sweets", "Spent_Gold", "Deals_Purchased", "Web_Purchases", "Catalog_Purchases", "Store_Purchases", "Monthly_Web_Visits", "Campaign1_Accepted", "Campaign2_Accepted", "Campaign3_Accepted", "Campaign4_Accepted", "Campaign5_Accepted", "Filed_Complaint", "Contact_Cost", "Revenue_Contribution", "Country", "City", "Region_Code", "Mobile_App_User", "Email_Subscriber", "Device_Type", "Referred_By_Friend", "Social_Media_User", "Membership_Tier", "Total_Amount_Spent", "Customer_Age", "Family_Size", "Senior_Citizen", "Campaign_Response"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (2001 lines)
test.csv (2001 lines)
train.csv (8001 lines)```

-> sample_submission.csv has 2000 rows and 2 columns.
Here is some information about the columns:
Campaign_Response (float64) has range: 0.00 - 1.00, 0 nan values
Customer_ID (int64) has range: 2.00 - 10000.00, 0 nan values

-> test.csv has 2000 rows and 41 columns.
Here is some information about the columns:
Annual_Income (float64) has range: -23.39 - 109134.97, 0 nan values
Birth_Year (int64) has range: 1940.00 - 2001.00, 0 nan values
Campaign1_Accepted (int64) has 2 unique values: [0, 1]
Campaign2_Accepted (int64) has 2 unique values: [1, 0]
Campaign3_Accepted (int64) has 2 unique values: [0, 1]
Campaign4_Accepted (int64) has 2 unique values: [0, 1]
Campaign5_Accepted (int64) has 2 unique values: [1, 0]
Catalog_Purchases (int64) has range: 0.00 - 9.00, 0 nan values
City (object) has 5 unique values: ['Mumbai', 'London', 'Berlin', 'New York', 'São Paulo']
Contact_Cost (int64) has 1 unique values: [3]
Country (object) has 5 unique values: ['UK', 'Brazil', 'India', 'Germany', 'USA']
Customer_Age (int64) has range: 24.00 - 85.00, 0 nan values
Customer_ID (int64) has range: 2.00 - 10000.00, 0 nan values
Customer_Since (object) has 1311 unique values. Some example values: ['28-04-2012', '03-07-2010', '10-09-2013', '03-06-2015']
Deals_Purchased (int64) has range: 0.00 - 9.00, 0 nan values
Device_Type (object) has 3 unique values: ['Desktop', 'Mobile', 'Tablet']
Education_Level (object) has 4 unique values: ['PhD', 'Graduation', 'Basic', 'Master']
Email_Subscriber (int64) has 2 unique values: [1, 0]
Family_Size (int64) has 6 unique values: [1, 4, 3, 2, 5, 0]
Filed_Complaint (int64) has 2 unique values: [1, 0]
Kids_Home (int64) has 3 unique values: [0, 2, 1]
Last_Purchase_Recency (int64) has range: 0.00 - 99.00, 0 nan values
Marital_Status (object) has 5 unique values: ['Widow', 'Together', 'Married', 'Divorced', 'Single']
Membership_Tier (object) has 4 unique values: ['Basic', 'Silver', 'Gold', 'Platinum']
Mobile_App_User (int64) has 2 unique values: [1, 0]
Monthly_Web_Visits (int64) has range: 0.00 - 19.00, 0 nan values
Referred_By_Friend (int64) has 2 unique values: [1, 0]
Region_Code (int64) has range: 100.00 - 998.00, 0 nan values
Revenue_Contribution (int64) has 1 unique values: [11]
Senior_Citizen (int64) has 2 unique values: [0, 1]
Social_Media_User (int64) has 2 unique values: [0, 1]
Spent_Fish (int64) has range: 0.00 - 299.00, 0 nan values
Spent_Fruits (int64) has range: 0.00 - 99.00, 0 nan values
Spent_Gold (int64) has range: 0.00 - 499.00, 0 nan values
Spent_Meat (int64) has range: 1.00 - 799.00, 0 nan values
Spent_Sweets (int64) has range: 0.00 - 199.00, 0 nan values
Spent_Wine (int64) has range: 0.00 - 999.00, 0 nan values
Store_Purchases (int64) has range: 0.00 - 9.00, 0 nan values
Teens_Home (int64) has 3 unique values: [1, 2, 0]
Total_Amount_Spent (int64) has range: 210.00 - 2616.00, 0 nan values
Web_Purchases (int64) has range: 0.00 - 9.00, 0 nan values

-> train.csv has 8000 rows and 42 columns.
Here is some information about the columns:
Annual_Income (float64) has range: -7845.63 - 104042.48, 0 nan values
Birth_Year (int64) has range: 1940.00 - 2001.00, 0 nan values
Campaign1_Accepted (int64) has 2 unique values: [1, 0]
Campaign2_Accepted (int64) has 2 unique values: [1, 0]
Campaign3_Accepted (int64) has 2 unique values: [0, 1]
Campaign4_Accepted (int64) has 2 unique values: [1, 0]
Campaign5_Accepted (int64) has 2 unique values: [0, 1]
Campaign_Response (int64) has 2 unique values: [1, 0]
Catalog_Purchases (int64) has range: 0.00 - 9.00, 0 nan values
City (object) has 5 unique values: ['Mumbai', 'London', 'New York', 'Berlin', 'São Paulo']
Contact_Cost (int64) has 1 unique values: [3]
Country (object) has 5 unique values: ['Germany', 'Brazil', 'UK', 'India', 'USA']
Customer_Age (int64) has range: 24.00 - 85.00, 0 nan values
Customer_ID (int64) has range: 1.00 - 9999.00, 0 nan values
Customer_Since (object) has 2132 unique values. Some example values: ['06-06-2011', '26-01-2015', '05-08-2015', '05-12-2012']
Deals_Purchased (int64) has range: 0.00 - 9.00, 0 nan values
Device_Type (object) has 3 unique values: ['Desktop', 'Mobile', 'Tablet']
Education_Level (object) has 4 unique values: ['Graduation', 'PhD', 'Master', 'Basic']
Email_Subscriber (int64) has 2 unique values: [0, 1]
Family_Size (int64) has 6 unique values: [2, 1, 4, 3, 5, 0]
Filed_Complaint (int64) has 2 unique values: [0, 1]
Kids_Home (int64) has 3 unique values: [1, 0, 2]
Last_Purchase_Recency (int64) has range: 0.00 - 99.00, 0 nan values
Marital_Status (object) has 5 unique values: ['Widow', 'Married', 'Together', 'Divorced', 'Single']
Membership_Tier (object) has 4 unique values: ['Silver', 'Basic', 'Platinum', 'Gold']
Mobile_App_User (int64) has 2 unique values: [1, 0]
Monthly_Web_Visits (int64) has range: 0.00 - 19.00, 0 nan values
Referred_By_Friend (int64) has 2 unique values: [1, 0]
Region_Code (int64) has range: 100.00 - 998.00, 0 nan values
Revenue_Contribution (int64) has 1 unique values: [11]
Senior_Citizen (int64) has 2 unique values: [0, 1]
Social_Media_User (int64) has 2 unique values: [1, 0]
Spent_Fish (int64) has range: 0.00 - 299.00, 0 nan values
Spent_Fruits (int64) has range: 0.00 - 99.00, 0 nan values
Spent_Gold (int64) has range: 0.00 - 499.00, 0 nan values
Spent_Meat (int64) has range: 0.00 - 799.00, 0 nan values
Spent_Sweets (int64) has range: 0.00 - 199.00, 0 nan values
Spent_Wine (int64) has range: 0.00 - 999.00, 0 nan values
Store_Purchases (int64) has range: 0.00 - 9.00, 0 nan values
Teens_Home (int64) has 3 unique values: [1, 0, 2]
Total_Amount_Spent (int64) has range: 303.00 - 2684.00, 0 nan values
Web_Purchases (int64) has range: 0.00 - 9.00, 0 nan values
