# OpenMLE-fast task

Task ID: `mobiles-and-laptop-sales-data@1`

Native metric: `SalesPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2852 bytes)
- `data/sample_submission.csv` (165030 bytes); columns: ["Id", "Price"]
- `data/test.csv` (833003 bytes); columns: ["Product", "Brand", "Inward Date", "Quantity Sold", "Customer Location", "Region", "Core Specification", "Processor Specification", "RAM", "ROM", "SSD", "Id"]
- `data/train.csv` (3276126 bytes); columns: ["Product", "Brand", "Inward Date", "Quantity Sold", "Customer Location", "Region", "Core Specification", "Processor Specification", "RAM", "ROM", "SSD", "Price"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (10001 lines)
test.csv (10001 lines)
train.csv (40001 lines)```

-> sample_submission.csv has 10000 rows and 2 columns.
Here is some information about the columns:
Id (object) has 10000 unique values. Some example values: ['T044326', 'T025621', 'T001990', 'T012182']
Price (float64) has range: 5040.00 - 199985.00, 0 nan values

-> test.csv has 10000 rows and 12 columns.
Here is some information about the columns:
Brand (object) has 20 unique values. Some example values: ['Google', 'Nokia', 'Apple', 'Samsung']
Core Specification (object) has 8 unique values: ['Ryzen 7', 'Ryzen 3', 'Ryzen 9', 'i9', nan, 'i7', 'i3', 'Ryzen 5', 'i5']
Customer Location (object) has 7761 unique values. Some example values: ['New Michael', 'South Michael', 'New Robert', 'Davidmouth']
Id (object) has 10000 unique values. Some example values: ['T044326', 'T025621', 'T001990', 'T012182']
Inward Date (object) has 731 unique values. Some example values: ['2024-09-05', '2024-07-11', '2023-07-17', '2024-05-04']
Processor Specification (object) has 15 unique values. Some example values: ['Apple A-Series', 'Samsung Exynos', 'MediaTek Dimensity', 'MediaTek Helio']
Product (object) has 2 unique values: ['Laptop', 'Mobile Phone']
Quantity Sold (int64) has range: 1.00 - 10.00, 0 nan values
RAM (object) has 6 unique values: ['6GB', '12GB', '16GB', '4GB', '8GB', '32GB']
ROM (object) has 5 unique values: ['128GB', '64GB', '256GB', '1TB', '512GB']
Region (object) has 5 unique values: ['North', 'South', 'Central', 'West', 'East']
SSD (object) has 4 unique values: ['256GB', '1TB', '2TB', '512GB', nan]

-> train.csv has 40000 rows and 12 columns.
Here is some information about the columns:
Brand (object) has 20 unique values. Some example values: ['Google', 'Nokia', 'Apple', 'Samsung']
Core Specification (object) has 8 unique values: [nan, 'Ryzen 3', 'Ryzen 5', 'i3', 'i7', 'Ryzen 7', 'i5', 'i9', 'Ryzen 9']
Customer Location (object) has 21735 unique values. Some example values: ['South Michael', 'North Michael', 'New James', 'New John']
Inward Date (object) has 731 unique values. Some example values: ['2024-10-26', '2023-03-31', '2023-07-25', '2024-11-19']
Price (int64) has range: 5008.00 - 199997.00, 0 nan values
Processor Specification (object) has 15 unique values. Some example values: ['MediaTek Dimensity', 'Snapdragon 8 Gen', 'Snapdragon 7s', 'Samsung Exynos']
Product (object) has 2 unique values: ['Mobile Phone', 'Laptop']
Quantity Sold (int64) has range: 1.00 - 10.00, 0 nan values
RAM (object) has 6 unique values: ['8GB', '16GB', '4GB', '12GB', '6GB', '32GB']
ROM (object) has 5 unique values: ['128GB', '256GB', '64GB', '1TB', '512GB']
Region (object) has 5 unique values: ['East', 'West', 'Central', 'North', 'South']
SSD (object) has 4 unique values: [nan, '2TB', '512GB', '256GB', '1TB']
