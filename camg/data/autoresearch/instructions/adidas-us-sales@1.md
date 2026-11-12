# OpenMLE-fast task

Task ID: `adidas-us-sales@1`

Native metric: `AdidasUSSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2554 bytes)
- `data/sample_submission.csv` (97812 bytes); columns: ["row_id", "units_sold"]
- `data/test.csv` (391137 bytes); columns: ["row_id", "retailer", "retailer_id", "invoice_date", "region", "state", "city", "product", "sales_method", "price_per_unit"]
- `data/train.csv` (522561 bytes); columns: ["row_id", "retailer", "retailer_id", "invoice_date", "region", "state", "city", "product", "sales_method", "price_per_unit", "units_sold"]

## Public description

```
description.txt (55 lines)
sample_submission.csv (4198 lines)
test.csv (4198 lines)
train.csv (5441 lines)```

-> sample_submission.csv has 4197 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 1.00 - 9637.00, 0 nan values
units_sold (float64) has range: 3.63 - 1273.79, 0 nan values

-> test.csv has 4197 rows and 10 columns.
Here is some information about the columns:
city (object) has 41 unique values. Some example values: ['Portland', 'Birmingham', 'Dallas', 'Philadelphia']
invoice_date (object) has 184 unique values. Some example values: ['2021-08-17', '2021-11-17', '2021-07-16', '2021-12-16']
price_per_unit (int64) has range: 7.00 - 110.00, 0 nan values
product (object) has 6 unique values: ["Women's Apparel", "Men's Athletic Footwear", "Men's Street Footwear", "Women's Street Footwear", "Women's Athletic Footwear", "Men's Apparel"]
region (object) has 5 unique values: ['Midwest', 'Southeast', 'Northeast', 'West', 'South']
retailer (object) has 6 unique values: ['Foot Locker', 'Sports Direct', 'West Gear', "Kohl's", 'Amazon', 'Walmart']
retailer_id (int64) has 3 unique values: [1185732, 1197831, 1128299]
row_id (int64) has range: 1.00 - 9637.00, 0 nan values
sales_method (object) has 3 unique values: ['Online', 'Outlet', 'In-store']
state (object) has 43 unique values. Some example values: ['Texas', 'Alabama', 'Pennsylvania', 'Maine']

-> train.csv has 5440 rows and 11 columns.
Here is some information about the columns:
city (object) has 50 unique values. Some example values: ['New York', 'Las Vegas', 'Los Angeles', 'Knoxville']
invoice_date (object) has 540 unique values. Some example values: ['2021-01-17', '2021-03-16', '2021-04-17', '2021-01-24']
price_per_unit (int64) has range: 7.00 - 110.00, 0 nan values
product (object) has 6 unique values: ["Men's Street Footwear", "Women's Apparel", "Men's Athletic Footwear", "Women's Street Footwear", "Women's Athletic Footwear", "Men's Apparel"]
region (object) has 5 unique values: ['Northeast', 'West', 'Southeast', 'South', 'Midwest']
retailer (object) has 6 unique values: ['Foot Locker', 'West Gear', 'Walmart', 'Sports Direct', "Kohl's", 'Amazon']
retailer_id (int64) has 4 unique values: [1185732, 1128299, 1197831, 1189833]
row_id (int64) has range: 2.00 - 9636.00, 0 nan values
sales_method (object) has 3 unique values: ['Outlet', 'Online', 'In-store']
state (object) has 49 unique values. Some example values: ['California', 'New York', 'Florida', 'Nevada']
units_sold (int64) has range: 6.00 - 1275.00, 0 nan values
