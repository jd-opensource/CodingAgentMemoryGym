# OpenMLE-fast task

Task ID: `sales-data@1`

Native metric: `SalesDemandRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3290 bytes)
- `data/sample_submission.csv` (746052 bytes); columns: ["Id", "Order_Quantity"]
- `data/test.csv` (4107868 bytes); columns: ["Date", "Day", "Month", "Year", "Customer_Age", "Age_Group", "Customer_Gender", "Country", "State", "Product_Category", "Sub_Category", "Product", "Unit_Cost", "Unit_Price", "Id"]
- `data/train.csv` (11254687 bytes); columns: ["Date", "Day", "Month", "Year", "Customer_Age", "Age_Group", "Customer_Gender", "Country", "State", "Product_Category", "Sub_Category", "Product", "Order_Quantity", "Unit_Cost", "Unit_Price", "Id"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (29399 lines)
test.csv (29399 lines)
train.csv (78285 lines)```

-> sample_submission.csv has 29398 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: -9222740343435964416.00 - 9220467392617381888.00, 0 nan values
Order_Quantity (float64) has 1 unique values: [11.0]

-> test.csv has 29398 rows and 15 columns.
Here is some information about the columns:
Age_Group (object) has 4 unique values: ['Adults (35-64)', 'Young Adults (25-34)', 'Youth (<25)', 'Seniors (64+)']
Country (object) has 6 unique values: ['Australia', 'Canada', 'United States', 'France', 'Germany', 'United Kingdom']
Customer_Age (int64) has range: 17.00 - 87.00, 0 nan values
Customer_Gender (object) has 2 unique values: ['M', 'F']
Date (object) has 212 unique values. Some example values: ['2016-03-01', '2016-06-14', '2016-02-20', '2016-04-03']
Day (int64) has range: 1.00 - 31.00, 0 nan values
Id (int64) has range: -9222740343435964416.00 - 9220467392617381888.00, 0 nan values
Month (object) has 7 unique values: ['March', 'May', 'February', 'January', 'June', 'July', 'April']
Product (object) has 130 unique values. Some example values: ['Water Bottle - 30 oz.', 'Patch Kit/8 Patches', 'Mountain Tire Tube', 'AWC Logo Cap']
Product_Category (object) has 3 unique values: ['Accessories', 'Clothing', 'Bikes']
State (object) has 46 unique values. Some example values: ['California', 'British Columbia', 'England', 'Washington']
Sub_Category (object) has 17 unique values. Some example values: ['Tires and Tubes', 'Bottles and Cages', 'Helmets', 'Road Bikes']
Unit_Cost (int64) has range: 1.00 - 2171.00, 0 nan values
Unit_Price (int64) has range: 2.00 - 3578.00, 0 nan values
Year (int64) has 1 unique values: [2016]

-> train.csv has 78284 rows and 16 columns.
Here is some information about the columns:
Age_Group (object) has 4 unique values: ['Youth (<25)', 'Adults (35-64)', 'Young Adults (25-34)', 'Seniors (64+)']
Country (object) has 6 unique values: ['Canada', 'Australia', 'United States', 'Germany', 'France', 'United Kingdom']
Customer_Age (int64) has range: 17.00 - 87.00, 0 nan values
Customer_Gender (object) has 2 unique values: ['M', 'F']
Date (object) has 942 unique values. Some example values: ['2014-03-01', '2015-12-07', '2013-12-07', '2014-06-14']
Day (int64) has range: 1.00 - 31.00, 0 nan values
Id (int64) has range: -9223275988800667648.00 - 9223369899504086016.00, 0 nan values
Month (object) has 12 unique values. Some example values: ['December', 'November', 'October', 'September']
Order_Quantity (int64) has range: 1.00 - 32.00, 0 nan values
Product (object) has 130 unique values. Some example values: ['Water Bottle - 30 oz.', 'Patch Kit/8 Patches', 'Mountain Tire Tube', 'AWC Logo Cap']
Product_Category (object) has 3 unique values: ['Accessories', 'Clothing', 'Bikes']
State (object) has 53 unique values. Some example values: ['California', 'British Columbia', 'England', 'Washington']
Sub_Category (object) has 17 unique values. Some example values: ['Tires and Tubes', 'Bottles and Cages', 'Helmets', 'Road Bikes']
Unit_Cost (int64) has range: 1.00 - 2171.00, 0 nan values
Unit_Price (int64) has range: 2.00 - 3578.00, 0 nan values
Year (int64) has 3 unique values: [2013, 2015, 2014]
