# OpenMLE-fast task

Task ID: `wfp-food-prices-in-egypt@1`

Native metric: `EgyptFoodPriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2391 bytes)
- `data/sample_submission.csv` (2198 bytes); columns: ["row_id", "price"]
- `data/test.csv` (17957 bytes); columns: ["row_id", "series_id", "date", "market_id", "market", "admin1", "admin2", "category", "commodity_id", "commodity", "unit"]
- `data/train.csv` (228510 bytes); columns: ["series_id", "date", "market_id", "market", "admin1", "admin2", "category", "commodity_id", "commodity", "unit", "price"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (156 lines)
test.csv (156 lines)
train.csv (2336 lines)```

-> sample_submission.csv has 155 rows and 2 columns.
Here is some information about the columns:
price (float64) has range: 2.27 - 39.81, 0 nan values
row_id (int64) has range: 1.00 - 155.00, 0 nan values

-> test.csv has 155 rows and 11 columns.
Here is some information about the columns:
admin1 (object) has 1 unique values: ['Cairo']
admin2 (object) has 1 unique values: ['Abdin']
category (object) has 7 unique values: ['pulses and nuts', 'cereals and tubers', 'vegetables and fruits', 'milk and dairy', 'meat, fish and eggs', 'oil and fats', 'miscellaneous food']
commodity (object) has 14 unique values. Some example values: ['Lentils', 'Pasta', 'Tomatoes', 'Beans (fava, dry)']
commodity_id (int64) has range: 52.00 - 1303.00, 0 nan values
date (object) has 16 unique values. Some example values: ['2024-04-15', '2025-02-15', '2024-11-15', '2024-08-15']
market (object) has 1 unique values: ['Cairo (national average)']
market_id (int64) has 1 unique values: [10254]
row_id (int64) has range: 1.00 - 155.00, 0 nan values
series_id (object) has 14 unique values. Some example values: ['10254_108_KG', '10254_112_KG', '10254_114_KG', '10254_385_KG']
unit (object) has 4 unique values: ['KG', '8 pcs', '1 piece', '800 G']

-> train.csv has 2335 rows and 11 columns.
Here is some information about the columns:
admin1 (object) has 1 unique values: ['Cairo', nan]
admin2 (object) has 1 unique values: ['Abdin', nan]
category (object) has 7 unique values: ['pulses and nuts', 'cereals and tubers', 'vegetables and fruits', 'milk and dairy', 'meat, fish and eggs', 'oil and fats', 'miscellaneous food']
commodity (object) has 31 unique values. Some example values: ['Tomatoes', 'Rice', 'Lentils', 'Pasta']
commodity_id (int64) has range: 52.00 - 1303.00, 0 nan values
date (object) has 160 unique values. Some example values: ['2021-02-15', '2021-12-15', '2021-07-15', '2021-10-15']
market (object) has 2 unique values: ['Cairo (national average)', 'National Average']
market_id (int64) has 2 unique values: [10254, 226]
price (float64) has range: 0.66 - 172.37, 0 nan values
series_id (object) has 38 unique values. Some example values: ['226_58_KG', '226_207_KG', '226_107_KG', '226_108_KG']
unit (object) has 6 unique values: ['KG', '8 pcs', '1 piece', '800 G', 'L', 'Unit']
