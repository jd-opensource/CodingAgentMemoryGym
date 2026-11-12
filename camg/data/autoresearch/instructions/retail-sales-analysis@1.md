# OpenMLE-fast task

Task ID: `retail-sales-analysis@1`

Native metric: `RetailSalesForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2527 bytes)
- `data/sample_submission.csv` (419891 bytes); columns: ["row_id", "target_retail_sales_next", "target_warehouse_sales_next"]
- `data/test.csv` (2682637 bytes); columns: ["row_id", "YEAR", "MONTH", "SUPPLIER", "ITEM CODE", "ITEM DESCRIPTION", "ITEM TYPE", "RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES"]
- `data/train.csv` (21900445 bytes); columns: ["YEAR", "MONTH", "SUPPLIER", "ITEM CODE", "ITEM DESCRIPTION", "ITEM TYPE", "RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES", "target_retail_sales_next", "target_warehouse_sales_next"]

## Public description

```
description.txt (43 lines)
sample_submission.csv (28809 lines)
test.csv (28809 lines)
train.csv (229243 lines)```

-> sample_submission.csv has 28808 rows and 3 columns.
Here is some information about the columns:
row_id (int64) has range: 0.00 - 28807.00, 0 nan values
target_retail_sales_next (float64) has range: -1.00 - 1110.76, 0 nan values
target_warehouse_sales_next (float64) has range: -229.33 - 13487.00, 0 nan values

-> test.csv has 28808 rows and 10 columns.
Here is some information about the columns:
ITEM CODE (int64) has range: 2.00 - 739611.00, 0 nan values
ITEM DESCRIPTION (object) has 12347 unique values. Some example values: ['PAUL HOBBS CROSSBARN CAB - 750ML', 'HATSUMAGO SAKE JUN MAI SHU - 300ML', 'MT GAY RUM - BLACK BARREL - 750ML', 'CHOPIN VODKA - 750ML']
ITEM TYPE (object) has 5 unique values: ['WINE', 'BEER', 'LIQUOR', 'KEGS', 'NON-ALCOHOL']
MONTH (int64) has 3 unique values: [1, 7, 3]
RETAIL SALES (float64) has range: -0.34 - 2739.00, 0 nan values
RETAIL TRANSFERS (float64) has range: -6.00 - 1990.83, 0 nan values
SUPPLIER (object) has 273 unique values. Some example values: ['THE COUNTRY VINTNER, LLC DBA WINEBOW', 'REPUBLIC NATIONAL DISTRIBUTING CO', 'SOUTHERN GLAZERS WINE AND SPIRITS', 'E & J GALLO WINERY']
WAREHOUSE SALES (float64) has range: -6.00 - 18317.00, 0 nan values
YEAR (int64) has 1 unique values: [2020]
row_id (int64) has range: 0.00 - 28807.00, 0 nan values

-> train.csv has 229242 rows and 11 columns.
Here is some information about the columns:
ITEM CODE (int64) has range: 2.00 - 995692.00, 0 nan values
ITEM DESCRIPTION (object) has 25458 unique values. Some example values: ['BURGANS ALBARINO - 750ML', 'SANTA JULIA TORRONTES SUSTAINABLE - 750ML', 'LA VIELLE FERME CDV RED - 750ML', 'MCCLINTOCK HERITAGE WHITE WHISKEY - 750ML']
ITEM TYPE (object) has 5 unique values: ['WINE', 'BEER', 'LIQUOR', 'KEGS', 'NON-ALCOHOL']
MONTH (int64) has range: 1.00 - 12.00, 0 nan values
RETAIL SALES (float64) has range: -6.49 - 1752.45, 0 nan values
RETAIL TRANSFERS (float64) has range: -38.49 - 1587.99, 0 nan values
SUPPLIER (object) has 361 unique values. Some example values: ['REPUBLIC NATIONAL DISTRIBUTING CO', 'A VINTNERS SELECTIONS', 'LEGENDS LTD', 'SOUTHERN GLAZERS WINE AND SPIRITS']
WAREHOUSE SALES (float64) has range: -229.33 - 17810.87, 0 nan values
YEAR (int64) has 3 unique values: [2019, 2017, 2018]
target_retail_sales_next (float64) has range: -2.00 - 1752.45, 0 nan values
target_warehouse_sales_next (float64) has range: -229.33 - 17810.87, 0 nan values
