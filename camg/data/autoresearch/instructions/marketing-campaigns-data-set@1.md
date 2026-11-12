# OpenMLE-fast task

Task ID: `marketing-campaigns-data-set@1`

Native metric: `MarketingCampaignAcceptanceMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4075 bytes)
- `data/sample_submission.csv` (10389 bytes); columns: ["ID", "Response"]
- `data/test.csv` (44462 bytes); columns: ["ID", "Year_Birth", "Education", "Marital_Status", "Income", "Kidhome", "Teenhome", "Dt_Customer", "Recency", "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "AcceptedCmp1", "AcceptedCmp2", "Complain", "Country"]
- `data/train.csv` (179788 bytes); columns: ["ID", "Year_Birth", "Education", "Marital_Status", "Income", "Kidhome", "Teenhome", "Dt_Customer", "Recency", "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "AcceptedCmp1", "AcceptedCmp2", "Response", "Complain", "Country"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (449 lines)
test.csv (449 lines)
train.csv (1793 lines)```

-> sample_submission.csv has 448 rows and 2 columns.
Here is some information about the columns:
ID (int64) has range: 0.00 - 11187.00, 0 nan values
Response (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 448 rows and 27 columns.
Here is some information about the columns:
AcceptedCmp1 (int64) has 2 unique values: [0, 1]
AcceptedCmp2 (int64) has 2 unique values: [0, 1]
AcceptedCmp3 (int64) has 2 unique values: [0, 1]
AcceptedCmp4 (int64) has 2 unique values: [0, 1]
AcceptedCmp5 (int64) has 2 unique values: [0, 1]
Complain (int64) has 2 unique values: [0, 1]
Country (object) has 8 unique values: ['CA', 'GER', 'US', 'SP', 'AUS', 'IND', 'SA', 'ME']
Dt_Customer (object) has 314 unique values. Some example values: ['2/16/13', '10/28/13', '11/2/13', '4/5/14']
Education (object) has 5 unique values: ['Graduation', 'Basic', 'PhD', 'Master', '2n Cycle']
ID (int64) has range: 0.00 - 11187.00, 0 nan values
Income (object) has 428 unique values. Some example values: ['$18,929.00 ', '$29,672.00 ', '$7,500.00 ', '$30,279.00 ']
Kidhome (int64) has 3 unique values: [0, 1, 2]
Marital_Status (object) has 7 unique values: ['Married', 'Together', 'Single', 'Divorced', 'Alone', 'Absurd', 'Widow']
MntFishProducts (int64) has range: 0.00 - 258.00, 0 nan values
MntFruits (int64) has range: 0.00 - 199.00, 0 nan values
MntGoldProds (int64) has range: 0.00 - 246.00, 0 nan values
MntMeatProducts (int64) has range: 0.00 - 1582.00, 0 nan values
MntSweetProducts (int64) has range: 0.00 - 197.00, 0 nan values
MntWines (int64) has range: 0.00 - 1492.00, 0 nan values
NumCatalogPurchases (int64) has range: 0.00 - 22.00, 0 nan values
NumDealsPurchases (int64) has range: 0.00 - 15.00, 0 nan values
NumStorePurchases (int64) has range: 0.00 - 13.00, 0 nan values
NumWebPurchases (int64) has range: 0.00 - 11.00, 0 nan values
NumWebVisitsMonth (int64) has range: 0.00 - 14.00, 0 nan values
Recency (int64) has range: 0.00 - 99.00, 0 nan values
Teenhome (int64) has 3 unique values: [1, 0, 2]
Year_Birth (int64) has range: 1893.00 - 1996.00, 0 nan values

-> train.csv has 1792 rows and 28 columns.
Here is some information about the columns:
AcceptedCmp1 (int64) has 2 unique values: [0, 1]
AcceptedCmp2 (int64) has 2 unique values: [0, 1]
AcceptedCmp3 (int64) has 2 unique values: [0, 1]
AcceptedCmp4 (int64) has 2 unique values: [0, 1]
AcceptedCmp5 (int64) has 2 unique values: [0, 1]
Complain (int64) has 2 unique values: [0, 1]
Country (object) has 8 unique values: ['SP', 'CA', 'SA', 'IND', 'GER', 'AUS', 'US', 'ME']
Dt_Customer (object) has 627 unique values. Some example values: ['8/31/12', '8/20/13', '5/22/14', '8/29/12']
Education (object) has 5 unique values: ['PhD', 'Graduation', 'Master', '2n Cycle', 'Basic']
ID (int64) has range: 9.00 - 11191.00, 0 nan values
Income (object) has 1623 unique values. Some example values: ['$7,500.00 ', '$18,690.00 ', '$37,760.00 ', '$47,025.00 ']
Kidhome (int64) has 3 unique values: [1, 0, 2]
Marital_Status (object) has 7 unique values: ['Single', 'Married', 'Widow', 'Divorced', 'Together', 'YOLO', 'Alone']
MntFishProducts (int64) has range: 0.00 - 259.00, 0 nan values
MntFruits (int64) has range: 0.00 - 199.00, 0 nan values
MntGoldProds (int64) has range: 0.00 - 362.00, 0 nan values
MntMeatProducts (int64) has range: 1.00 - 1725.00, 0 nan values
MntSweetProducts (int64) has range: 0.00 - 263.00, 0 nan values
MntWines (int64) has range: 0.00 - 1493.00, 0 nan values
NumCatalogPurchases (int64) has range: 0.00 - 28.00, 0 nan values
NumDealsPurchases (int64) has range: 0.00 - 15.00, 0 nan values
NumStorePurchases (int64) has range: 0.00 - 13.00, 0 nan values
NumWebPurchases (int64) has range: 0.00 - 27.00, 0 nan values
NumWebVisitsMonth (int64) has range: 0.00 - 20.00, 0 nan values
Recency (int64) has range: 0.00 - 99.00, 0 nan values
Response (int64) has 2 unique values: [0, 1]
Teenhome (int64) has 3 unique values: [1, 0, 2]
Year_Birth (int64) has range: 1899.00 - 1996.00, 0 nan values
