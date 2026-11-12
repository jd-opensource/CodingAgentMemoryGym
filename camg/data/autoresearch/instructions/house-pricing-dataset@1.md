# OpenMLE-fast task

Task ID: `house-pricing-dataset@1`

Native metric: `HousePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2862 bytes)
- `data/sample_submission.csv` (41683 bytes); columns: ["id", "price"]
- `data/test.csv` (268189 bytes); columns: ["id", "date", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long"]
- `data/train.csv` (1917963 bytes); columns: ["id", "date", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (2878 lines)
test.csv (2878 lines)
train.csv (18737 lines)```

-> sample_submission.csv has 2877 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 3.00 - 21610.00, 0 nan values
price (float64) has 1 unique values: [449950.0]

-> test.csv has 2877 rows and 18 columns.
Here is some information about the columns:
bathrooms (float64) has range: 0.00 - 6.00, 0 nan values
bedrooms (int64) has 8 unique values: [3, 4, 2, 5, 6, 1, 7, 0]
condition (object) has 5 unique values: ['Average', 'Good', 'Very Good', 'Fair', 'Poor']
date (object) has 47 unique values. Some example values: ['20150427T000000', '20150414T000000', '20150428T000000', '20150422T000000']
floors (float64) has 6 unique values: [1.0, 2.0, 1.5, 2.5, 3.0, 3.5]
grade (int64) has range: 4.00 - 13.00, 0 nan values
id (int64) has range: 3.00 - 21610.00, 0 nan values
lat (float64) has range: 47.16 - 47.78, 0 nan values
long (float64) has range: -122.51 - -121.31, 0 nan values
sqft_above (int64) has range: 390.00 - 6720.00, 0 nan values
sqft_basement (int64) has range: 0.00 - 2390.00, 0 nan values
sqft_living (int64) has range: 390.00 - 8000.00, 0 nan values
sqft_lot (int64) has range: 609.00 - 1164794.00, 0 nan values
view (int64) has 5 unique values: [0, 3, 4, 2, 1]
waterfront (object) has 2 unique values: ['N', 'Y']
yr_built (int64) has range: 1900.00 - 2015.00, 0 nan values
yr_renovated (int64) has range: 0.00 - 2015.00, 0 nan values
zipcode (int64) has range: 98001.00 - 98199.00, 0 nan values

-> train.csv has 18736 rows and 19 columns.
Here is some information about the columns:
bathrooms (float64) has range: 0.00 - 8.00, 0 nan values
bedrooms (int64) has range: 0.00 - 33.00, 0 nan values
condition (object) has 5 unique values: ['Average', 'Very Good', 'Good', 'Poor', 'Fair']
date (object) has 325 unique values. Some example values: ['20140623T000000', '20140625T000000', '20140626T000000', '20140708T000000']
floors (float64) has 6 unique values: [1.0, 2.0, 1.5, 3.0, 2.5, 3.5]
grade (int64) has range: 1.00 - 13.00, 0 nan values
id (int64) has range: 1.00 - 21613.00, 0 nan values
lat (float64) has range: 47.16 - 47.78, 0 nan values
long (float64) has range: -122.52 - -121.31, 0 nan values
price (float64) has range: 75000.00 - 7700000.00, 0 nan values
sqft_above (int64) has range: 290.00 - 9410.00, 0 nan values
sqft_basement (int64) has range: 0.00 - 4820.00, 0 nan values
sqft_living (int64) has range: 290.00 - 13540.00, 0 nan values
sqft_lot (int64) has range: 520.00 - 1651359.00, 0 nan values
view (int64) has 5 unique values: [0, 3, 4, 2, 1]
waterfront (object) has 2 unique values: ['N', 'Y']
yr_built (int64) has range: 1900.00 - 2015.00, 0 nan values
yr_renovated (int64) has range: 0.00 - 2015.00, 0 nan values
zipcode (int64) has range: 98001.00 - 98199.00, 0 nan values
