# OpenMLE-fast task

Task ID: `used-car-price-prediction-dataset@1`

Native metric: `UsedCarPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3332 bytes)
- `data/sample_submission.csv` (22155 bytes); columns: ["id", "price"]
- `data/test.csv` (151774 bytes); columns: ["id", "brand", "model", "model_year", "milage", "fuel_type", "engine", "transmission", "ext_col", "int_col", "accident", "clean_title"]
- `data/train.csv` (480260 bytes); columns: ["id", "brand", "model", "model_year", "milage", "fuel_type", "engine", "transmission", "ext_col", "int_col", "accident", "clean_title", "price"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (1003 lines)
test.csv (1003 lines)
train.csv (3008 lines)```

-> sample_submission.csv has 1002 rows and 2 columns.
Here is some information about the columns:
id (object) has 1002 unique values. Some example values: ['ID000347', 'ID002303', 'ID000387', 'ID002939']
price (float64) has range: 26283.54 - 35516.46, 0 nan values

-> test.csv has 1002 rows and 12 columns.
Here is some information about the columns:
accident (object) has 2 unique values: ['None reported', 'At least 1 accident or damage reported', nan]
brand (object) has 49 unique values. Some example values: ['Ford', 'BMW', 'Mercedes-Benz', 'Chevrolet']
clean_title (object) has 1 unique values: ['Yes', nan]
engine (object) has 546 unique values. Some example values: ['2.0L I4 16V GDI DOHC Turbo', '420.0HP 6.2L 8 Cylinder Engine Gasoline Fuel', '–', '355.0HP 5.3L 8 Cylinder Engine Gasoline Fuel']
ext_col (object) has 135 unique values. Some example values: ['White', 'Black', 'Gray', 'Blue']
fuel_type (object) has 6 unique values: ['–', 'Gasoline', 'E85 Flex Fuel', nan, 'Hybrid', 'Plug-In Hybrid', 'Diesel']
id (object) has 1002 unique values. Some example values: ['ID000347', 'ID002303', 'ID000387', 'ID002939']
int_col (object) has 62 unique values. Some example values: ['Black', 'Beige', 'Gray', '–']
milage (object) has 851 unique values. Some example values: ['45,000 mi.', '26,000 mi.', '55,000 mi.', '106,000 mi.']
model (object) has 743 unique values. Some example values: ['M3 Base', 'Corvette Base', 'F-150 XLT', '1500 Laramie']
model_year (int64) has range: 1974.00 - 2024.00, 0 nan values
transmission (object) has 38 unique values. Some example values: ['A/T', 'Transmission w/Dual Shift Mode', '8-Speed A/T', '6-Speed A/T']

-> train.csv has 3007 rows and 13 columns.
Here is some information about the columns:
accident (object) has 2 unique values: ['None reported', 'At least 1 accident or damage reported', nan]
brand (object) has 56 unique values. Some example values: ['Ford', 'BMW', 'Mercedes-Benz', 'Chevrolet']
clean_title (object) has 1 unique values: ['Yes', nan]
engine (object) has 1006 unique values. Some example values: ['355.0HP 5.3L 8 Cylinder Engine Gasoline Fuel', '300.0HP 3.0L Straight 6 Cylinder Engine Gasoline Fuel', '240.0HP 2.0L 4 Cylinder Engine Gasoline Fuel', '285.0HP 3.6L V6 Cylinder Engine Gasoline Fuel']
ext_col (object) has 248 unique values. Some example values: ['Black', 'White', 'Gray', 'Silver']
fuel_type (object) has 7 unique values: ['–', 'Gasoline', 'Hybrid', 'Diesel', 'E85 Flex Fuel', nan, 'Plug-In Hybrid', 'not supported']
id (object) has 3007 unique values. Some example values: ['ID002261', 'ID001681', 'ID000301', 'ID002490']
int_col (object) has 131 unique values. Some example values: ['Black', 'Beige', 'Gray', 'Brown']
milage (object) has 2192 unique values. Some example values: ['110,000 mi.', '120,000 mi.', '48,000 mi.', '92,000 mi.']
model (object) has 1596 unique values. Some example values: ['M3 Base', 'F-150 XLT', 'Wrangler Sport', 'Mustang GT Premium']
model_year (int64) has range: 1992.00 - 2024.00, 0 nan values
price (float64) has range: 2000.00 - 2954083.00, 0 nan values
transmission (object) has 58 unique values. Some example values: ['A/T', '8-Speed A/T', 'Transmission w/Dual Shift Mode', '6-Speed A/T']
