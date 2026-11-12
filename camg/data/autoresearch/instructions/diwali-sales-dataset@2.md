# OpenMLE-fast task

Task ID: `diwali-sales-dataset@2`

Native metric: `DiwaliOrdersQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2393 bytes)
- `data/sample_submission.csv` (14640 bytes); columns: ["row_id", "Orders"]
- `data/test.csv` (176469 bytes); columns: ["row_id", "User_ID", "Product_ID", "Gender", "Age Group", "Age", "Marital_Status", "State", "Zone", "Occupation", "Product_Category"]
- `data/train.csv` (685607 bytes); columns: ["User_ID", "Product_ID", "Gender", "Age Group", "Age", "Marital_Status", "State", "Zone", "Occupation", "Product_Category", "Orders"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (2249 lines)
test.csv (2249 lines)
train.csv (8996 lines)```

-> sample_submission.csv has 2248 rows and 2 columns.
Here is some information about the columns:
Orders (int64) has 4 unique values: [2, 4, 1, 3]
row_id (int64) has range: 0.00 - 2247.00, 0 nan values

-> test.csv has 2248 rows and 11 columns.
Here is some information about the columns:
Age (int64) has range: 12.00 - 92.00, 0 nan values
Age Group (object) has 7 unique values: ['26-35', '0-17', '18-25', '46-50', '55+', '51-55', '36-45']
Gender (object) has 2 unique values: ['F', 'M']
Marital_Status (int64) has 2 unique values: [0, 1]
Occupation (object) has 15 unique values. Some example values: ['IT Sector', 'Healthcare', 'Aviation', 'Banking']
Product_Category (object) has 18 unique values. Some example values: ['Food', 'Clothing & Apparel', 'Electronics & Gadgets', 'Footwear & Shoes']
Product_ID (object) has 1225 unique values. Some example values: ['P00184942', 'P00265242', 'P00059442', 'P00110942']
State (object) has 16 unique values. Some example values: ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Delhi']
User_ID (int64) has range: 1000004.00 - 1006040.00, 0 nan values
Zone (object) has 5 unique values: ['Western', 'Southern', 'Central', 'Northern', 'Eastern']
row_id (int64) has range: 0.00 - 2247.00, 0 nan values

-> train.csv has 8995 rows and 11 columns.
Here is some information about the columns:
Age (int64) has range: 12.00 - 92.00, 0 nan values
Age Group (object) has 7 unique values: ['55+', '26-35', '46-50', '18-25', '51-55', '36-45', '0-17']
Gender (object) has 2 unique values: ['F', 'M']
Marital_Status (int64) has 2 unique values: [0, 1]
Occupation (object) has 15 unique values. Some example values: ['IT Sector', 'Healthcare', 'Aviation', 'Banking']
Orders (int64) has 4 unique values: [1, 2, 4, 3]
Product_Category (object) has 18 unique values. Some example values: ['Clothing & Apparel', 'Food', 'Electronics & Gadgets', 'Footwear & Shoes']
Product_ID (object) has 2214 unique values. Some example values: ['P00265242', 'P00110942', 'P00237542', 'P00112142']
State (object) has 16 unique values. Some example values: ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Delhi']
User_ID (int64) has range: 1000001.00 - 1006040.00, 0 nan values
Zone (object) has 5 unique values: ['Western', 'Central', 'Southern', 'Eastern', 'Northern']
