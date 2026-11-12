# OpenMLE-fast task

Task ID: `blinkit-sales-dataset@2`

Native metric: `BlinkitSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2597 bytes)
- `data/sample_submission.csv` (87023 bytes); columns: ["row_id", "Sales"]
- `data/test.csv` (345105 bytes); columns: ["row_id", "Item Identifier", "ItemKey", "Item Type", "ItemContentKey", "Item Fat Content", "Item Visibility", "Item Weight", "Outlet Establishment Year", "Outlet Size", "Outlet Type", "Tier", "city_count", "metro_flag"]
- `data/train.csv` (480986 bytes); columns: ["row_id", "Item Identifier", "ItemKey", "Item Type", "ItemContentKey", "Item Fat Content", "Item Visibility", "Item Weight", "Outlet Establishment Year", "Outlet Size", "Outlet Type", "Tier", "city_count", "metro_flag", "Sales"]

## Public description

```
description.txt (56 lines)
sample_submission.csv (3726 lines)
test.csv (3726 lines)
train.csv (4799 lines)```

-> sample_submission.csv has 3725 rows and 2 columns.
Here is some information about the columns:
Sales (float64) has range: 31.61 - 266.83, 0 nan values
row_id (int64) has range: 0.00 - 8522.00, 0 nan values

-> test.csv has 3725 rows and 14 columns.
Here is some information about the columns:
Item Fat Content (object) has 2 unique values: ['Regular', 'Low Fat']
Item Identifier (object) has 1526 unique values. Some example values: ['DRI03', 'FDR37', 'FDP25', 'FDL48']
Item Type (object) has 16 unique values. Some example values: ['Snack Foods', 'Fruits and Vegetables', 'Household', 'Frozen Foods']
Item Visibility (float64) has range: 0.00 - 0.19, 0 nan values
Item Weight (float64) has range: 4.55 - 21.35, 935 nan values
ItemContentKey (int64) has 2 unique values: [1, 2]
ItemKey (int64) has range: 1.00 - 16.00, 0 nan values
Outlet Establishment Year (int64) has 4 unique values: [2012, 2016, 2018, 2017]
Outlet Size (object) has 2 unique values: ['Medium', 'Small']
Outlet Type (object) has 2 unique values: ['Supermarket Type1', 'Supermarket Type3']
Tier (object) has 3 unique values: ['Tier 1', 'Tier 3', 'Tier 2']
city_count (float64) has 2 unique values: [1.0, 3.0, nan]
metro_flag (float64) has 1 unique values: [1.0, nan]
row_id (int64) has range: 0.00 - 8522.00, 0 nan values

-> train.csv has 4798 rows and 15 columns.
Here is some information about the columns:
Item Fat Content (object) has 2 unique values: ['Low Fat', 'Regular']
Item Identifier (object) has 1541 unique values. Some example values: ['FDS13', 'NCF42', 'FDR52', 'FDL13']
Item Type (object) has 16 unique values. Some example values: ['Fruits and Vegetables', 'Snack Foods', 'Household', 'Frozen Foods']
Item Visibility (float64) has range: 0.00 - 0.33, 0 nan values
Item Weight (float64) has range: 4.55 - 21.35, 528 nan values
ItemContentKey (int64) has 2 unique values: [2, 1]
ItemKey (int64) has range: 1.00 - 16.00, 0 nan values
Outlet Establishment Year (int64) has 6 unique values: [2022, 2014, 2015, 2020, 2011, 2018]
Outlet Size (object) has 3 unique values: ['Medium', 'High', 'Small']
Outlet Type (object) has 3 unique values: ['Supermarket Type2', 'Supermarket Type1', 'Grocery Store']
Sales (float64) has range: 31.49 - 266.89, 0 nan values
Tier (object) has 3 unique values: ['Tier 3', 'Tier 2', 'Tier 1']
city_count (float64) has 3 unique values: [nan, 1.0, 3.0, 2.0]
metro_flag (float64) has 2 unique values: [nan, 0.0, 1.0]
row_id (int64) has range: 1.00 - 8245.00, 0 nan values
