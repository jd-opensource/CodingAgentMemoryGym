# OpenMLE-fast task

Task ID: `online-shopping-dataset@1`

Native metric: `OnlineShoppingConversionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3562 bytes)
- `data/sample_submission.csv` (108580 bytes); columns: ["row_id", "Coupon_Status"]
- `data/test.csv` (1178240 bytes); columns: ["row_id", "CustomerID", "Gender", "Location", "Tenure_Months", "Transaction_ID", "Transaction_Date", "Product_SKU", "Product_Description", "Product_Category", "Quantity", "Avg_Price", "Delivery_Charges", "GST", "Month", "Coupon_Code", "Discount_pct"]
- `data/train.csv` (6577695 bytes); columns: ["row_id", "CustomerID", "Gender", "Location", "Tenure_Months", "Transaction_ID", "Transaction_Date", "Product_SKU", "Product_Description", "Product_Category", "Quantity", "Avg_Price", "Delivery_Charges", "GST", "Month", "Coupon_Code", "Discount_pct", "Coupon_Status"]

## Public description

```
description.txt (52 lines)
sample_submission.csv (8464 lines)
test.csv (8464 lines)
train.csv (44462 lines)```

-> sample_submission.csv has 8463 rows and 2 columns.
Here is some information about the columns:
Coupon_Status (object) has 3 unique values: ['Clicked', 'Used', 'Not Used']
row_id (int64) has range: 4062.00 - 52069.00, 0 nan values

-> test.csv has 8463 rows and 17 columns.
Here is some information about the columns:
Avg_Price (float64) has range: 0.39 - 355.74, 0 nan values
Coupon_Code (object) has 22 unique values. Some example values: ['ELEC30', 'ELEC20', 'SALE30', 'SALE20']
CustomerID (float64) has range: 12347.00 - 18250.00, 0 nan values
Delivery_Charges (float64) has range: 0.00 - 504.00, 0 nan values
Discount_pct (float64) has 2 unique values: [30.0, 20.0]
GST (float64) has 3 unique values: [0.1, 0.18, 0.05]
Gender (object) has 2 unique values: ['M', 'F']
Location (object) has 5 unique values: ['California', 'Chicago', 'New York', 'New Jersey', 'Washington DC']
Month (int64) has 2 unique values: [12, 11]
Product_Category (object) has 14 unique values. Some example values: ['Nest-USA', 'Apparel', 'Nest', 'Office']
Product_Description (object) has 167 unique values. Some example values: ['Nest Learning Thermostat 3rd Gen-USA - Stainless Steel', 'Nest Cam Outdoor Security Camera - USA', 'Nest Cam Indoor Security Camera - USA', 'Nest Thermostat E - USA']
Product_SKU (object) has 306 unique values. Some example values: ['GGOENEBJ079499', 'GGOENEBQ078999', 'GGOENEBB078899', 'GGOENEBQ086799']
Quantity (float64) has range: 1.00 - 523.00, 0 nan values
Tenure_Months (float64) has range: 2.00 - 50.00, 0 nan values
Transaction_Date (object) has 61 unique values. Some example values: ['2019-11-27', '2019-12-18', '2019-12-06', '2019-12-19']
Transaction_ID (float64) has range: 42260.00 - 48497.00, 0 nan values
row_id (int64) has range: 4062.00 - 52069.00, 0 nan values

-> train.csv has 44461 rows and 18 columns.
Here is some information about the columns:
Avg_Price (float64) has range: 0.40 - 349.00, 0 nan values
Coupon_Code (object) has 45 unique values. Some example values: ['SALE20', 'SALE10', 'ELEC10', 'SALE30']
Coupon_Status (object) has 3 unique values: ['Used', 'Not Used', 'Clicked']
CustomerID (float64) has range: 12346.00 - 18283.00, 0 nan values
Delivery_Charges (float64) has range: 0.00 - 521.36, 0 nan values
Discount_pct (float64) has 3 unique values: [10.0, 20.0, 30.0]
GST (float64) has 4 unique values: [0.1, 0.18, 0.05, 0.12]
Gender (object) has 2 unique values: ['M', 'F']
Location (object) has 5 unique values: ['Chicago', 'California', 'New York', 'New Jersey', 'Washington DC']
Month (int64) has range: 1.00 - 10.00, 0 nan values
Product_Category (object) has 20 unique values. Some example values: ['Apparel', 'Nest-USA', 'Office', 'Drinkware']
Product_Description (object) has 368 unique values. Some example values: ['Nest Learning Thermostat 3rd Gen-USA - Stainless Steel', 'Nest Cam Outdoor Security Camera - USA', 'Nest Cam Indoor Security Camera - USA', 'Google Sunglasses']
Product_SKU (object) has 1021 unique values. Some example values: ['GGOENEBJ079499', 'GGOENEBQ078999', 'GGOENEBB078899', 'GGOENEBQ079099']
Quantity (float64) has range: 1.00 - 900.00, 0 nan values
Tenure_Months (float64) has range: 2.00 - 50.00, 0 nan values
Transaction_Date (object) has 304 unique values. Some example values: ['2019-07-13', '2019-08-16', '2019-08-02', '2019-07-31']
Transaction_ID (float64) has range: 16679.00 - 42259.00, 0 nan values
row_id (int64) has range: 0.00 - 52923.00, 0 nan values
