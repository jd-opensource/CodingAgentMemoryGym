# OpenMLE-fast task

Task ID: `adidas-us-sales@2`

Native metric: `AdidasUSSalesChannelMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2279 bytes)
- `data/sample_submission.csv` (51932 bytes); columns: ["id", "sales_method"]
- `data/test.csv` (327045 bytes); columns: ["id", "retailer", "invoice_date", "region", "state", "city", "product", "price_per_unit"]
- `data/train.csv` (458068 bytes); columns: ["id", "retailer", "invoice_date", "region", "state", "city", "product", "price_per_unit", "sales_method"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (4198 lines)
test.csv (4198 lines)
train.csv (5441 lines)```

-> sample_submission.csv has 4197 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 5441.00 - 9637.00, 0 nan values
sales_method (object) has 3 unique values: ['Online', 'In-store', 'Outlet']

-> test.csv has 4197 rows and 8 columns.
Here is some information about the columns:
city (object) has 41 unique values. Some example values: ['Portland', 'Dallas', 'Birmingham', 'Philadelphia']
id (int64) has range: 5441.00 - 9637.00, 0 nan values
invoice_date (object) has 184 unique values. Some example values: ['2021-08-17', '2021-11-17', '2021-07-16', '2021-12-16']
price_per_unit (int64) has range: 7.00 - 110.00, 0 nan values
product (object) has 6 unique values: ["Men's Street Footwear", "Women's Street Footwear", "Women's Apparel", "Men's Apparel", "Men's Athletic Footwear", "Women's Athletic Footwear"]
region (object) has 5 unique values: ['Southeast', 'South', 'West', 'Midwest', 'Northeast']
retailer (object) has 6 unique values: ['Foot Locker', 'Sports Direct', 'West Gear', 'Walmart', "Kohl's", 'Amazon']
state (object) has 43 unique values. Some example values: ['Alabama', 'Texas', 'Pennsylvania', 'Maine']

-> train.csv has 5440 rows and 9 columns.
Here is some information about the columns:
city (object) has 50 unique values. Some example values: ['New York', 'Los Angeles', 'Knoxville', 'Las Vegas']
id (int64) has range: 1.00 - 5440.00, 0 nan values
invoice_date (object) has 540 unique values. Some example values: ['2021-01-17', '2021-04-17', '2021-03-16', '2021-01-24']
price_per_unit (int64) has range: 7.00 - 110.00, 0 nan values
product (object) has 6 unique values: ["Men's Apparel", "Men's Athletic Footwear", "Women's Apparel", "Men's Street Footwear", "Women's Street Footwear", "Women's Athletic Footwear"]
region (object) has 5 unique values: ['Northeast', 'West', 'Southeast', 'South', 'Midwest']
retailer (object) has 6 unique values: ['Foot Locker', 'West Gear', 'Walmart', 'Sports Direct', 'Amazon', "Kohl's"]
sales_method (object) has 3 unique values: ['Outlet', 'Online', 'In-store']
state (object) has 49 unique values. Some example values: ['California', 'New York', 'Florida', 'Nevada']
