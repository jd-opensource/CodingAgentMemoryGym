# OpenMLE-fast task

Task ID: `black-friday-sale@1`

Native metric: `BlackFridayPurchaseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2205 bytes)
- `data/sample_submission.csv` (2630325 bytes); columns: ["Row_ID", "Purchase"]
- `data/test.csv` (5281448 bytes); columns: ["Row_ID", "User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3"]
- `data/train.csv` (20854498 bytes); columns: ["User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3", "Purchase"]

## Public description

```
description.txt (52 lines)
sample_submission.csv (110015 lines)
test.csv (110015 lines)
train.csv (440055 lines)```

-> sample_submission.csv has 110014 rows and 2 columns.
Here is some information about the columns:
Purchase (float64) has range: 12.00 - 23960.00, 0 nan values
Row_ID (int64) has range: 0.00 - 110013.00, 0 nan values

-> test.csv has 110014 rows and 12 columns.
Here is some information about the columns:
Age (object) has 7 unique values: ['0-17', '55+', '26-35', '46-50', '51-55', '36-45', '18-25']
City_Category (object) has 3 unique values: ['A', 'C', 'B']
Gender (object) has 2 unique values: ['F', 'M']
Marital_Status (int64) has 2 unique values: [0, 1]
Occupation (int64) has range: 0.00 - 20.00, 0 nan values
Product_Category_1 (int64) has range: 1.00 - 20.00, 0 nan values
Product_Category_2 (float64) has range: 2.00 - 18.00, 35027 nan values
Product_Category_3 (float64) has range: 3.00 - 18.00, 78810 nan values
Product_ID (object) has 3298 unique values. Some example values: ['P00117942', 'P00128942', 'P00062842', 'P00161942']
Row_ID (int64) has range: 0.00 - 110013.00, 0 nan values
Stay_In_Current_City_Years (object) has 5 unique values: ['2', '4+', '3', '1', '0']
User_ID (int64) has range: 1000001.00 - 1006040.00, 0 nan values

-> train.csv has 440054 rows and 12 columns.
Here is some information about the columns:
Age (object) has 7 unique values: ['0-17', '26-35', '46-50', '51-55', '36-45', '18-25', '55+']
City_Category (object) has 3 unique values: ['A', 'B', 'C']
Gender (object) has 2 unique values: ['F', 'M']
Marital_Status (int64) has 2 unique values: [0, 1]
Occupation (int64) has range: 0.00 - 20.00, 0 nan values
Product_Category_1 (int64) has range: 1.00 - 20.00, 0 nan values
Product_Category_2 (float64) has range: 2.00 - 18.00, 138611 nan values
Product_Category_3 (float64) has range: 3.00 - 18.00, 304437 nan values
Product_ID (object) has 3421 unique values. Some example values: ['P00265242', 'P00025442', 'P00110742', 'P00112142']
Purchase (int64) has range: 12.00 - 23961.00, 0 nan values
Stay_In_Current_City_Years (object) has 5 unique values: ['2', '3', '1', '4+', '0']
User_ID (int64) has range: 1000001.00 - 1006040.00, 0 nan values
