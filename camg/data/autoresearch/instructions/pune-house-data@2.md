# OpenMLE-fast task

Task ID: `pune-house-data@2`

Native metric: `RealEstateRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2671 bytes)
- `data/sample_submission.csv` (138018 bytes); columns: ["id", "rupees_per_sqft"]
- `data/test.csv` (464631 bytes); columns: ["id", "city", "area_type", "availability", "location", "size_bhk", "bath", "balcony", "total_sqft", "furnishing", "type", "parking", "ready_to_move_flag"]
- `data/train.csv` (2218623 bytes); columns: ["id", "city", "area_type", "availability", "location", "size_bhk", "bath", "balcony", "total_sqft", "furnishing", "type", "parking", "ready_to_move_flag", "rupees_per_sqft"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (5509 lines)
test.csv (5509 lines)
train.csv (22033 lines)```

-> sample_submission.csv has 5508 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 100003.00 - 127539.00, 0 nan values
rupees_per_sqft (float64) has range: 2451.06 - 14708.06, 0 nan values

-> test.csv has 5508 rows and 13 columns.
Here is some information about the columns:
area_type (object) has 4 unique values: ['Super built-up  Area', 'Plot  Area', 'Built-up  Area', 'Carpet  Area', nan]
availability (object) has 74 unique values. Some example values: ['Ready To Move', 'Ready_to_move', '18-May', '18-Dec']
balcony (float64) has 4 unique values: [1.0, 2.0, 3.0, nan, 0.0]
bath (float64) has range: 1.00 - 27.00, 26 nan values
city (object) has 3 unique values: ['bangalore', 'pune', 'delhi']
furnishing (object) has 3 unique values: [nan, 'Semi-Furnished', 'Furnished', 'Unfurnished']
id (int64) has range: 100003.00 - 127539.00, 0 nan values
location (object) has 870 unique values. Some example values: ['whitefield', 'sarjapur road', 'kanakpura road', 'electronic city']
parking (float64) has 7 unique values: [nan, 2.0, 1.0, 39.0, 3.0, 4.0, 5.0, 114.0]
ready_to_move_flag (int64) has 2 unique values: [0, 1]
size_bhk (float64) has range: 1.00 - 27.00, 1 nan values
total_sqft (float64) has range: 300.00 - 14000.00, 0 nan values
type (object) has 2 unique values: [nan, 'Builder_Floor', 'Apartment']

-> train.csv has 22032 rows and 14 columns.
Here is some information about the columns:
area_type (object) has 4 unique values: ['Super built-up  Area', 'Built-up  Area', nan, 'Plot  Area', 'Carpet  Area']
availability (object) has 83 unique values. Some example values: ['Ready To Move', 'Ready_to_move', '18-Dec', '18-May']
balcony (float64) has 4 unique values: [2.0, 1.0, nan, 0.0, 3.0]
bath (float64) has range: 1.00 - 40.00, 104 nan values
city (object) has 3 unique values: ['pune', 'bangalore', 'delhi']
furnishing (object) has 3 unique values: [nan, 'Unfurnished', 'Furnished', 'Semi-Furnished']
id (int64) has range: 100000.00 - 127537.00, 0 nan values
location (object) has 1573 unique values. Some example values: ['whitefield', 'sarjapur road', 'electronic city', 'kanakpura road']
parking (float64) has 9 unique values: [nan, 1.0, 4.0, 3.0, 114.0, 39.0, 2.0, 9.0, 10.0, 5.0]
ready_to_move_flag (int64) has 2 unique values: [1, 0]
rupees_per_sqft (float64) has range: 1933.90 - 44444.44, 0 nan values
size_bhk (float64) has range: 1.00 - 43.00, 13 nan values
total_sqft (float64) has range: 150.00 - 14220.00, 0 nan values
type (object) has 2 unique values: [nan, 'Builder_Floor', 'Apartment']
