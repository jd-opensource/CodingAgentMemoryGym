# OpenMLE-fast task

Task ID: `housing-price-dataset@1`

Native metric: `KingCountyHomePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3207 bytes)
- `data/sample_submission.csv` (129642 bytes); columns: ["id", "price"]
- `data/test.csv` (482472 bytes); columns: ["id", "date", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"]
- `data/train.csv` (1865793 bytes); columns: ["id", "date", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15", "price"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (4753 lines)
test.csv (4753 lines)
train.csv (16862 lines)```

-> sample_submission.csv has 4752 rows and 2 columns.
Here is some information about the columns:
id (object) has 4752 unique values. Some example values: ['KC021606', 'KC000008', 'KC000009', 'KC000010']
price (float64) has range: 80546.25 - 3044679.28, 0 nan values

-> test.csv has 4752 rows and 20 columns.
Here is some information about the columns:
bathrooms (float64) has range: 0.00 - 6.50, 0 nan values
bedrooms (int64) has range: 0.00 - 9.00, 0 nan values
condition (int64) has 5 unique values: [3, 4, 5, 2, 1]
date (object) has 78 unique values. Some example values: ['20150427T000000', '20150325T000000', '20150422T000000', '20150414T000000']
floors (float64) has 6 unique values: [1.0, 2.0, 1.5, 2.5, 3.0, 3.5]
grade (int64) has range: 4.00 - 13.00, 0 nan values
id (object) has 4752 unique values. Some example values: ['KC021606', 'KC000008', 'KC000009', 'KC000010']
lat (float64) has range: 47.16 - 47.78, 0 nan values
long (float64) has range: -122.51 - -121.31, 0 nan values
sqft_above (int64) has range: 390.00 - 6720.00, 0 nan values
sqft_basement (int64) has range: 0.00 - 2390.00, 0 nan values
sqft_living (int64) has range: 390.00 - 8000.00, 0 nan values
sqft_living15 (int64) has range: 399.00 - 5500.00, 0 nan values
sqft_lot (int64) has range: 609.00 - 1651359.00, 0 nan values
sqft_lot15 (int64) has range: 748.00 - 858132.00, 0 nan values
view (int64) has 5 unique values: [0, 2, 3, 4, 1]
waterfront (int64) has 2 unique values: [0, 1]
yr_built (int64) has range: 1900.00 - 2015.00, 0 nan values
yr_renovated (int64) has range: 0.00 - 2015.00, 0 nan values
zipcode (int64) has range: 98001.00 - 98199.00, 0 nan values

-> train.csv has 16861 rows and 21 columns.
Here is some information about the columns:
bathrooms (float64) has range: 0.00 - 8.00, 0 nan values
bedrooms (int64) has range: 0.00 - 33.00, 0 nan values
condition (int64) has 5 unique values: [3, 5, 4, 1, 2]
date (object) has 294 unique values. Some example values: ['20140623T000000', '20140625T000000', '20140626T000000', '20140708T000000']
floors (float64) has 6 unique values: [1.0, 2.0, 1.5, 3.0, 2.5, 3.5]
grade (int64) has range: 1.00 - 13.00, 0 nan values
id (object) has 16861 unique values. Some example values: ['KC021612', 'KC000000', 'KC000001', 'KC000002']
lat (float64) has range: 47.16 - 47.78, 0 nan values
long (float64) has range: -122.52 - -121.31, 0 nan values
price (float64) has range: 75000.00 - 7700000.00, 0 nan values
sqft_above (int64) has range: 290.00 - 9410.00, 0 nan values
sqft_basement (int64) has range: 0.00 - 4820.00, 0 nan values
sqft_living (int64) has range: 290.00 - 13540.00, 0 nan values
sqft_living15 (int64) has range: 460.00 - 6210.00, 0 nan values
sqft_lot (int64) has range: 520.00 - 1074218.00, 0 nan values
sqft_lot15 (int64) has range: 651.00 - 871200.00, 0 nan values
view (int64) has 5 unique values: [0, 3, 4, 2, 1]
waterfront (int64) has 2 unique values: [0, 1]
yr_built (int64) has range: 1900.00 - 2015.00, 0 nan values
yr_renovated (int64) has range: 0.00 - 2015.00, 0 nan values
zipcode (int64) has range: 98001.00 - 98199.00, 0 nan values
