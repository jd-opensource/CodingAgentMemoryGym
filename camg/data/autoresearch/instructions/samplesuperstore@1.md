# OpenMLE-fast task

Task ID: `samplesuperstore@1`

Native metric: `SuperstoreProfitMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2494 bytes)
- `data/sample_submission.csv` (47759 bytes); columns: ["Id", "Profit"]
- `data/test.csv` (189248 bytes); columns: ["Id", "Ship Mode", "Segment", "City", "State", "Postal Code", "Region", "Category", "Sub-Category", "Sales", "Quantity", "Discount"]
- `data/train.csv` (817784 bytes); columns: ["Id", "Ship Mode", "Segment", "City", "State", "Postal Code", "Region", "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (2000 lines)
test.csv (2000 lines)
train.csv (7995 lines)```

-> sample_submission.csv has 1999 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 9.00 - 9993.00, 0 nan values
Profit (float64) has 1 unique values: [28.851134538403805]

-> test.csv has 1999 rows and 12 columns.
Here is some information about the columns:
Category (object) has 3 unique values: ['Office Supplies', 'Technology', 'Furniture']
City (object) has 350 unique values. Some example values: ['New York City', 'Los Angeles', 'Philadelphia', 'San Francisco']
Discount (float64) has range: 0.00 - 0.80, 0 nan values
Id (int64) has range: 9.00 - 9993.00, 0 nan values
Postal Code (int64) has range: 1453.00 - 99301.00, 0 nan values
Quantity (int64) has range: 1.00 - 14.00, 0 nan values
Region (object) has 4 unique values: ['West', 'East', 'Central', 'South']
Sales (float64) has range: 0.44 - 22638.48, 0 nan values
Segment (object) has 3 unique values: ['Home Office', 'Consumer', 'Corporate']
Ship Mode (object) has 4 unique values: ['Standard Class', 'Same Day', 'First Class', 'Second Class']
State (object) has 47 unique values. Some example values: ['California', 'New York', 'Texas', 'Washington']
Sub-Category (object) has 17 unique values. Some example values: ['Binders', 'Paper', 'Furnishings', 'Phones']

-> train.csv has 7994 rows and 13 columns.
Here is some information about the columns:
Category (object) has 3 unique values: ['Office Supplies', 'Technology', 'Furniture']
City (object) has 517 unique values. Some example values: ['New York City', 'Los Angeles', 'Philadelphia', 'San Francisco']
Discount (float64) has range: 0.00 - 0.80, 0 nan values
Id (int64) has range: 1.00 - 9992.00, 0 nan values
Postal Code (int64) has range: 1040.00 - 99301.00, 0 nan values
Profit (float64) has range: -6599.98 - 6719.98, 0 nan values
Quantity (int64) has range: 1.00 - 14.00, 0 nan values
Region (object) has 4 unique values: ['Central', 'South', 'West', 'East']
Sales (float64) has range: 0.84 - 13999.96, 0 nan values
Segment (object) has 3 unique values: ['Consumer', 'Corporate', 'Home Office']
Ship Mode (object) has 4 unique values: ['Standard Class', 'Same Day', 'First Class', 'Second Class']
State (object) has 49 unique values. Some example values: ['California', 'New York', 'Texas', 'Pennsylvania']
Sub-Category (object) has 17 unique values. Some example values: ['Binders', 'Paper', 'Furnishings', 'Phones']
