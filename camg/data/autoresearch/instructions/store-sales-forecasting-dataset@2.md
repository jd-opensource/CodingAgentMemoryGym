# OpenMLE-fast task

Task ID: `store-sales-forecasting-dataset@2`

Native metric: `StoreSalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4325 bytes)
- `data/sample_submission.csv` (10195 bytes); columns: ["id", "lead_time_days"]
- `data/test.csv` (99823 bytes); columns: ["id", "Row ID", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount"]
- `data/train.csv` (373578 bytes); columns: ["id", "Row ID", "Order ID", "Order Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "lead_time_days"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (451 lines)
test.csv (451 lines)
train.csv (1672 lines)```

-> sample_submission.csv has 450 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1672.00 - 2121.00, 0 nan values
lead_time_days (float64) has range: 0.00 - 7.00, 0 nan values

-> test.csv has 450 rows and 20 columns.
Here is some information about the columns:
Category (object) has 1 unique values: ['Furniture']
City (object) has 147 unique values. Some example values: ['New York City', 'Philadelphia', 'Los Angeles', 'Seattle']
Country (object) has 1 unique values: ['United States']
Customer ID (object) has 308 unique values. Some example values: ['SV-20365', 'Dp-13240', 'ML-17410', 'AC-10615']
Customer Name (object) has 308 unique values. Some example values: ['Seth Vernon', 'Dean percer', 'Maris LaWare', 'Ann Chong']
Discount (float64) has range: 0.00 - 0.70, 0 nan values
Order Date (object) has 142 unique values. Some example values: ['2017-10-30', '2017-11-19', '2017-09-15', '2017-10-02']
Order ID (object) has 367 unique values. Some example values: ['CA-2017-125451', 'US-2017-162558', 'CA-2017-100111', 'CA-2017-163860']
Postal Code (int64) has range: 1841.00 - 99207.00, 0 nan values
Product ID (object) has 262 unique values. Some example values: ['FUR-CH-10003061', 'FUR-TA-10001676', 'FUR-CH-10004860', 'FUR-FU-10001424']
Product Name (object) has 264 unique values. Some example values: ['Global Leather Task Chair, Black', 'Hon 61000 Series Interactive Training Tables', 'Global Low Back Tilter Chair', 'Dax Clear Box Frame']
Quantity (int64) has range: 1.00 - 14.00, 0 nan values
Region (object) has 4 unique values: ['East', 'West', 'South', 'Central']
Row ID (int64) has range: 24.00 - 9902.00, 0 nan values
Sales (float64) has range: 2.03 - 4416.17, 0 nan values
Segment (object) has 3 unique values: ['Consumer', 'Home Office', 'Corporate']
Ship Mode (object) has 4 unique values: ['First Class', 'Standard Class', 'Second Class', 'Same Day']
State (object) has 40 unique values. Some example values: ['California', 'New York', 'Pennsylvania', 'Texas']
Sub-Category (object) has 4 unique values: ['Furnishings', 'Tables', 'Chairs', 'Bookcases']
id (int64) has range: 1672.00 - 2121.00, 0 nan values

-> train.csv has 1671 rows and 21 columns.
Here is some information about the columns:
Category (object) has 1 unique values: ['Furniture']
City (object) has 334 unique values. Some example values: ['New York City', 'Los Angeles', 'San Francisco', 'Philadelphia']
Country (object) has 1 unique values: ['United States']
Customer ID (object) has 647 unique values. Some example values: ['CJ-12010', 'GB-14530', 'KL-16555', 'SC-20095']
Customer Name (object) has 647 unique values. Some example values: ['Caroline Jumper', 'George Bell', 'Kelly Lampkin', 'Sanjit Chand']
Discount (float64) has range: 0.00 - 0.70, 0 nan values
Order Date (object) has 747 unique values. Some example values: ['2016-09-05', '2016-12-25', '2016-12-01', '2016-11-04']
Order ID (object) has 1397 unique values. Some example values: ['CA-2014-145387', 'CA-2015-104346', 'CA-2016-157749', 'US-2015-129007']
Postal Code (int64) has range: 1040.00 - 99301.00, 0 nan values
Product ID (object) has 371 unique values. Some example values: ['FUR-FU-10004270', 'FUR-CH-10002647', 'FUR-CH-10002880', 'FUR-CH-10001146']
Product Name (object) has 376 unique values. Some example values: ['KI Adjustable-Height Table', 'Situations Contoured Folding Chairs, 4/Set', 'Staple-based wall hangings', 'Global High-Back Leather Tilter, Burgundy']
Quantity (int64) has range: 1.00 - 14.00, 0 nan values
Region (object) has 4 unique values: ['South', 'Central', 'East', 'West']
Row ID (int64) has range: 1.00 - 9991.00, 0 nan values
Sales (float64) has range: 1.89 - 4404.90, 0 nan values
Segment (object) has 3 unique values: ['Home Office', 'Consumer', 'Corporate']
Ship Mode (object) has 4 unique values: ['Standard Class', 'First Class', 'Second Class', 'Same Day']
State (object) has 47 unique values. Some example values: ['California', 'New York', 'Texas', 'Illinois']
Sub-Category (object) has 4 unique values: ['Chairs', 'Furnishings', 'Bookcases', 'Tables']
id (int64) has range: 1.00 - 1671.00, 0 nan values
lead_time_days (int64) has 8 unique values: [4, 5, 3, 1, 2, 6, 0, 7]
