# OpenMLE-fast task

Task ID: `zomato-dataset@1`

Native metric: `ZomatoRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3310 bytes)
- `data/sample_submission.csv` (38200 bytes); columns: ["Restaurant ID", "Aggregate rating"]
- `data/test.csv` (217773 bytes); columns: ["Restaurant ID", "Country Code", "City", "Locality", "Locality Verbose", "Longitude", "Latitude", "Cuisines", "Average Cost for two", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Switch to order menu", "Price range", "Votes"]
- `data/train.csv` (899565 bytes); columns: ["Restaurant ID", "Country Code", "City", "Locality", "Locality Verbose", "Longitude", "Latitude", "Cuisines", "Average Cost for two", "Currency", "Has Table booking", "Has Online delivery", "Is delivering now", "Switch to order menu", "Price range", "Votes", "Aggregate rating"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (1473 lines)
test.csv (1473 lines)
train.csv (5932 lines)```

-> sample_submission.csv has 1472 rows and 2 columns.
Here is some information about the columns:
Aggregate rating (float64) has range: 0.02 - 5.00, 0 nan values
Restaurant ID (int64) has range: 64.00 - 18493989.00, 0 nan values

-> test.csv has 1472 rows and 16 columns.
Here is some information about the columns:
Average Cost for two (int64) has range: 0.00 - 800000.00, 0 nan values
City (object) has 88 unique values. Some example values: ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad']
Country Code (int64) has range: 1.00 - 216.00, 0 nan values
Cuisines (object) has 515 unique values. Some example values: ['North Indian', 'North Indian, Chinese', 'North Indian, Mughlai', 'Cafe']
Currency (object) has 12 unique values. Some example values: ['Indian Rupees(Rs.)', 'Dollar($)', 'Pounds(\x8c£)', 'Brazilian Real(R$)']
Has Online delivery (object) has 2 unique values: ['Yes', 'No']
Has Table booking (object) has 2 unique values: ['No', 'Yes']
Is delivering now (object) has 2 unique values: ['No', 'Yes']
Latitude (float64) has range: -41.33 - 55.96, 0 nan values
Locality (object) has 524 unique values. Some example values: ['Connaught Place', 'Rajouri Garden', 'Rajinder Nagar', 'Satyaniketan']
Locality Verbose (object) has 540 unique values. Some example values: ['Connaught Place, New Delhi', 'Rajouri Garden, New Delhi', 'Rajinder Nagar, New Delhi', 'Satyaniketan, New Delhi']
Longitude (float64) has range: -157.83 - 174.79, 0 nan values
Price range (int64) has 4 unique values: [3, 1, 2, 4]
Restaurant ID (int64) has range: 64.00 - 18493989.00, 0 nan values
Switch to order menu (object) has 1 unique values: ['No']
Votes (int64) has range: 4.00 - 10934.00, 0 nan values

-> train.csv has 5931 rows and 17 columns.
Here is some information about the columns:
Aggregate rating (float64) has range: 1.80 - 4.90, 0 nan values
Average Cost for two (int64) has range: 0.00 - 800000.00, 0 nan values
City (object) has 141 unique values. Some example values: ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad']
Country Code (int64) has range: 1.00 - 216.00, 0 nan values
Cuisines (object) has 1494 unique values. Some example values: ['North Indian', 'North Indian, Chinese', 'North Indian, Mughlai', 'Cafe']
Currency (object) has 12 unique values. Some example values: ['Indian Rupees(Rs.)', 'Dollar($)', 'Pounds(\x8c£)', 'Rand(R)']
Has Online delivery (object) has 2 unique values: ['No', 'Yes']
Has Table booking (object) has 2 unique values: ['No', 'Yes']
Is delivering now (object) has 2 unique values: ['No', 'Yes']
Latitude (float64) has range: -41.30 - 55.98, 0 nan values
Locality (object) has 1068 unique values. Some example values: ['Connaught Place', 'Rajouri Garden', 'Malviya Nagar', 'Pitampura']
Locality Verbose (object) has 1118 unique values. Some example values: ['Connaught Place, New Delhi', 'Rajouri Garden, New Delhi', 'Malviya Nagar, New Delhi', 'Pitampura, New Delhi']
Longitude (float64) has range: -157.95 - 174.83, 0 nan values
Price range (int64) has 4 unique values: [1, 2, 3, 4]
Restaurant ID (int64) has range: 53.00 - 18496057.00, 0 nan values
Switch to order menu (object) has 1 unique values: ['No']
Votes (int64) has range: 4.00 - 9667.00, 0 nan values
