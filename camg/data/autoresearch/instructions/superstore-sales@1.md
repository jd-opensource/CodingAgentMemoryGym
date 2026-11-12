# OpenMLE-fast task

Task ID: `superstore-sales@1`

Native metric: `SuperstoreSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4194 bytes)
- `data/sample_submission.csv` (1714 bytes); columns: ["ID", "Sales"]
- `data/test.csv` (16085 bytes); columns: ["ID", "Row_ID", "Order_ID", "Order_Date", "Ship_Date", "Ship_Mode", "Customer_ID", "Customer_Name", "Segment", "Country", "City", "State", "Postal_Code", "Region", "Product_ID", "Category", "Sub_Category", "Product_Name"]
- `data/train.csv` (2119327 bytes); columns: ["Row_ID", "Order_ID", "Order_Date", "Ship_Date", "Ship_Mode", "Customer_ID", "Customer_Name", "Segment", "Country", "City", "State", "Postal_Code", "Region", "Product_ID", "Category", "Sub_Category", "Product_Name", "Sales"]

## Public description

```
description.txt (55 lines)
sample_submission.csv (74 lines)
test.csv (74 lines)
train.csv (9728 lines)```

-> sample_submission.csv has 73 rows and 2 columns.
Here is some information about the columns:
ID (int64) has range: 198.00 - 9605.00, 0 nan values
Sales (float64) has range: 1.87 - 1934.43, 0 nan values

-> test.csv has 73 rows and 18 columns.
Here is some information about the columns:
Category (object) has 3 unique values: ['Office Supplies', 'Technology', 'Furniture']
City (object) has 47 unique values. Some example values: ['New York City', 'Philadelphia', 'Seattle', 'Chicago']
Country (object) has 1 unique values: ['United States']
Customer_ID (object) has 70 unique values. Some example values: ['ON-18715', 'EB-13840', 'SR-20425', 'JE-15745']
Customer_Name (object) has 70 unique values. Some example values: ['Odella Nelson', 'Ellis Ballard', 'Sharelle Roach', 'Joel Eaton']
ID (int64) has range: 198.00 - 9605.00, 0 nan values
Order_Date (object) has 71 unique values. Some example values: ['6/10/2015', '16/12/2017', '8/6/2018', '22/06/2015']
Order_ID (object) has 73 unique values. Some example values: ['CA-2018-107720', 'US-2018-155299', 'CA-2015-142048', 'CA-2015-134677']
Postal_Code (float64) has range: 6040.00 - 98502.00, 0 nan values
Product_ID (object) has 47 unique values. Some example values: ['OFF-BI-10004099', 'OFF-PA-10004092', 'FUR-FU-10003096', 'OFF-BI-10004876']
Product_Name (object) has 47 unique values. Some example values: ['GBC VeloBinder Strips', 'Tops Green Bar Computer Printout Paper', 'Master Giant Foot Doorstop, Safety Yellow', 'Wilson Jones Suede Grain Vinyl Binders']
Region (object) has 4 unique values: ['East', 'Central', 'West', 'South']
Row_ID (int64) has range: 198.00 - 9605.00, 0 nan values
Segment (object) has 3 unique values: ['Home Office', 'Corporate', 'Consumer']
Ship_Date (object) has 72 unique values. Some example values: ['13/11/2018', '12/6/2018', '25/06/2015', '10/10/2015']
Ship_Mode (object) has 4 unique values: ['Standard Class', 'First Class', 'Second Class', 'Same Day']
State (object) has 25 unique values. Some example values: ['New York', 'Texas', 'Pennsylvania', 'California']
Sub_Category (object) has 15 unique values. Some example values: ['Paper', 'Binders', 'Machines', 'Bookcases']

-> train.csv has 9727 rows and 18 columns.
Here is some information about the columns:
Category (object) has 3 unique values: ['Furniture', 'Office Supplies', 'Technology']
City (object) has 527 unique values. Some example values: ['New York City', 'Los Angeles', 'Philadelphia', 'San Francisco']
Country (object) has 1 unique values: ['United States']
Customer_ID (object) has 793 unique values. Some example values: ['WB-21850', 'MA-17560', 'JL-15835', 'PP-18955']
Customer_Name (object) has 793 unique values. Some example values: ['William Brown', 'Matt Abelman', 'John Lee', 'Paul Prost']
Order_Date (object) has 1225 unique values. Some example values: ['5/9/2017', '10/11/2017', '1/12/2018', '2/12/2018']
Order_ID (object) has 4849 unique values. Some example values: ['CA-2018-100111', 'CA-2018-157987', 'CA-2017-165330', 'US-2017-108504']
Postal_Code (float64) has range: 1040.00 - 99301.00, 11 nan values
Product_ID (object) has 1814 unique values. Some example values: ['OFF-PA-10001970', 'TEC-AC-10003832', 'FUR-FU-10004270', 'TEC-AC-10002049']
Product_Name (object) has 1803 unique values. Some example values: ['Staple envelope', 'Staples', 'Easy-staple paper', 'Avery Non-Stick Binders']
Region (object) has 4 unique values: ['South', 'West', 'Central', 'East']
Row_ID (int64) has range: 1.00 - 9800.00, 0 nan values
Sales (float64) has range: 0.44 - 22638.48, 0 nan values
Segment (object) has 3 unique values: ['Consumer', 'Corporate', 'Home Office']
Ship_Date (object) has 1322 unique values. Some example values: ['26/09/2018', '6/12/2018', '16/12/2016', '21/11/2018']
Ship_Mode (object) has 4 unique values: ['Second Class', 'Standard Class', 'First Class', 'Same Day']
State (object) has 49 unique values. Some example values: ['California', 'New York', 'Texas', 'Pennsylvania']
Sub_Category (object) has 17 unique values. Some example values: ['Binders', 'Paper', 'Furnishings', 'Phones']
