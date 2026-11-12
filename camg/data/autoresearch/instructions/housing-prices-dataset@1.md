# OpenMLE-fast task

Task ID: `housing-prices-dataset@1`

Native metric: `HousingPricesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1977 bytes)
- `data/sample_submission.csv` (2197 bytes); columns: ["Id", "price"]
- `data/test.csv` (8162 bytes); columns: ["Id", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus"]
- `data/train.csv` (20637 bytes); columns: ["price", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (165 lines)
test.csv (165 lines)
train.csv (382 lines)```

-> sample_submission.csv has 164 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 1.00 - 164.00, 0 nan values
price (float64) has 1 unique values: [4340000.0]

-> test.csv has 164 rows and 13 columns.
Here is some information about the columns:
Id (int64) has range: 1.00 - 164.00, 0 nan values
airconditioning (object) has 2 unique values: ['yes', 'no']
area (int64) has range: 1905.00 - 16200.00, 0 nan values
basement (object) has 2 unique values: ['no', 'yes']
bathrooms (int64) has 3 unique values: [1, 2, 3]
bedrooms (int64) has 6 unique values: [3, 2, 4, 5, 1, 6]
furnishingstatus (object) has 3 unique values: ['semi-furnished', 'unfurnished', 'furnished']
guestroom (object) has 2 unique values: ['no', 'yes']
hotwaterheating (object) has 2 unique values: ['no', 'yes']
mainroad (object) has 2 unique values: ['yes', 'no']
parking (int64) has 4 unique values: [0, 1, 2, 3]
prefarea (object) has 2 unique values: ['no', 'yes']
stories (int64) has 4 unique values: [2, 1, 4, 3]

-> train.csv has 381 rows and 13 columns.
Here is some information about the columns:
airconditioning (object) has 2 unique values: ['no', 'yes']
area (int64) has range: 1650.00 - 13200.00, 0 nan values
basement (object) has 2 unique values: ['no', 'yes']
bathrooms (int64) has 4 unique values: [1, 2, 3, 4]
bedrooms (int64) has 6 unique values: [3, 2, 4, 5, 1, 6]
furnishingstatus (object) has 3 unique values: ['unfurnished', 'semi-furnished', 'furnished']
guestroom (object) has 2 unique values: ['no', 'yes']
hotwaterheating (object) has 2 unique values: ['no', 'yes']
mainroad (object) has 2 unique values: ['yes', 'no']
parking (int64) has 4 unique values: [0, 2, 1, 3]
prefarea (object) has 2 unique values: ['no', 'yes']
price (int64) has range: 1750000.00 - 13300000.00, 0 nan values
stories (int64) has 4 unique values: [2, 1, 3, 4]
