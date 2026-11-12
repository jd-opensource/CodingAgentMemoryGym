# OpenMLE-fast task

Task ID: `bigmart-sales-data@1`

Native metric: `BigMartRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2564 bytes)
- `data/sample_submission.csv` (46987 bytes); columns: ["Item_Outlet_Sales"]
- `data/test.csv` (235125 bytes); columns: ["Item_Identifier", "Item_Weight", "Item_Fat_Content", "Item_Visibility", "Item_Type", "Item_MRP", "Outlet_Identifier", "Outlet_Establishment_Year", "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"]
- `data/train.csv` (604366 bytes); columns: ["Item_Identifier", "Item_Weight", "Item_Fat_Content", "Item_Visibility", "Item_Type", "Item_MRP", "Outlet_Identifier", "Outlet_Establishment_Year", "Outlet_Size", "Outlet_Location_Type", "Outlet_Type", "Item_Outlet_Sales"]

## Public description

```
description.txt (56 lines)
sample_submission.csv (2558 lines)
test.csv (2558 lines)
train.csv (5967 lines)```

-> sample_submission.csv has 2557 rows and 1 columns.
Here is some information about the columns:
Item_Outlet_Sales (float64) has range: 71.05 - 31782.70, 0 nan values

-> test.csv has 2557 rows and 11 columns.
Here is some information about the columns:
Item_Fat_Content (object) has 5 unique values: ['Low Fat', 'Regular', 'reg', 'LF', 'low fat']
Item_Identifier (object) has 1317 unique values. Some example values: ['FDF05', 'DRE49', 'FDV60', 'FDA15']
Item_MRP (float64) has range: 31.29 - 266.59, 0 nan values
Item_Type (object) has 16 unique values. Some example values: ['Fruits and Vegetables', 'Snack Foods', 'Household', 'Frozen Foods']
Item_Visibility (float64) has range: 0.00 - 0.31, 0 nan values
Item_Weight (float64) has range: 4.55 - 21.35, 442 nan values
Outlet_Establishment_Year (int64) has 9 unique values: [2002, 1985, 2007, 1987, 1997, 1998, 2009, 1999, 2004]
Outlet_Identifier (object) has 10 unique values. Some example values: ['OUT035', 'OUT013', 'OUT045', 'OUT027']
Outlet_Location_Type (object) has 3 unique values: ['Tier 2', 'Tier 3', 'Tier 1']
Outlet_Size (object) has 3 unique values: [nan, 'Medium', 'High', 'Small']
Outlet_Type (object) has 4 unique values: ['Supermarket Type1', 'Supermarket Type3', 'Grocery Store', 'Supermarket Type2']

-> train.csv has 5966 rows and 12 columns.
Here is some information about the columns:
Item_Fat_Content (object) has 5 unique values: ['Regular', 'Low Fat', 'LF', 'reg', 'low fat']
Item_Identifier (object) has 1548 unique values. Some example values: ['NCY18', 'FDG09', 'FDB17', 'FDF52']
Item_MRP (float64) has range: 31.89 - 266.89, 0 nan values
Item_Outlet_Sales (float64) has range: 33.29 - 13086.96, 0 nan values
Item_Type (object) has 16 unique values. Some example values: ['Fruits and Vegetables', 'Snack Foods', 'Household', 'Frozen Foods']
Item_Visibility (float64) has range: 0.00 - 0.33, 0 nan values
Item_Weight (float64) has range: 4.55 - 21.35, 1021 nan values
Outlet_Establishment_Year (int64) has 9 unique values: [1997, 2007, 1985, 2004, 1998, 1987, 2009, 2002, 1999]
Outlet_Identifier (object) has 10 unique values. Some example values: ['OUT046', 'OUT018', 'OUT017', 'OUT049']
Outlet_Location_Type (object) has 3 unique values: ['Tier 1', 'Tier 2', 'Tier 3']
Outlet_Size (object) has 3 unique values: ['Small', nan, 'Medium', 'High']
Outlet_Type (object) has 4 unique values: ['Supermarket Type1', 'Supermarket Type3', 'Grocery Store', 'Supermarket Type2']
