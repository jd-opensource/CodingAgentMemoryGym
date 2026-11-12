# OpenMLE-fast task

Task ID: `diamonds@1`

Native metric: `DiamondPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1777 bytes)
- `data/sample_submission.csv` (136950 bytes); columns: ["id", "price"]
- `data/test.csv` (522307 bytes); columns: ["id", "carat", "cut", "color", "clarity", "depth", "table", "x", "y", "z"]
- `data/train.csv` (2310538 bytes); columns: ["id", "carat", "cut", "color", "clarity", "depth", "table", "x", "y", "z", "price"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (10708 lines)
test.csv (10708 lines)
train.csv (43214 lines)```

-> sample_submission.csv has 10707 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1.00 - 53937.00, 0 nan values
price (float64) has 1 unique values: [2512.0]

-> test.csv has 10707 rows and 10 columns.
Here is some information about the columns:
carat (float64) has range: 0.20 - 2.04, 0 nan values
clarity (object) has 8 unique values: ['SI2', 'SI1', 'VS1', 'VS2', 'VVS1', 'VVS2', 'I1', 'IF']
color (object) has 7 unique values: ['E', 'I', 'H', 'J', 'F', 'G', 'D']
cut (object) has 5 unique values: ['Ideal', 'Premium', 'Good', 'Very Good', 'Fair']
depth (float64) has range: 43.00 - 72.20, 0 nan values
id (int64) has range: 1.00 - 53937.00, 0 nan values
table (float64) has range: 49.00 - 73.00, 0 nan values
x (float64) has range: 3.73 - 8.25, 0 nan values
y (float64) has range: 3.68 - 8.30, 0 nan values
z (float64) has range: 1.53 - 5.27, 0 nan values

-> train.csv has 43213 rows and 11 columns.
Here is some information about the columns:
carat (float64) has range: 0.23 - 5.01, 0 nan values
clarity (object) has 8 unique values: ['SI2', 'VVS2', 'SI1', 'I1', 'VS2', 'VS1', 'VVS1', 'IF']
color (object) has 7 unique values: ['J', 'E', 'I', 'H', 'D', 'G', 'F']
cut (object) has 5 unique values: ['Good', 'Very Good', 'Ideal', 'Premium', 'Fair']
depth (float64) has range: 43.00 - 79.00, 0 nan values
id (int64) has range: 5.00 - 53940.00, 0 nan values
price (int64) has range: 335.00 - 18823.00, 0 nan values
table (float64) has range: 43.00 - 95.00, 0 nan values
x (float64) has range: 3.83 - 10.74, 0 nan values
y (float64) has range: 3.85 - 58.90, 0 nan values
z (float64) has range: 1.07 - 31.80, 0 nan values
