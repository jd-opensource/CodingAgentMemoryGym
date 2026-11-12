# OpenMLE-fast task

Task ID: `real-estate-dataset@1`

Native metric: `RealEstatePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5007 bytes)
- `data/sample_submission.csv` (76210 bytes); columns: ["Id", "price"]
- `data/test.csv` (354866 bytes); columns: ["Id", "name_nsi", "index", "environment", "quality_of_living", "safety", "transport", "services", "relax", "condition", "area", "energy_costs", "provision", "certificate", "construction_type", "orientation", "year_built", "last_reconstruction", "total_floors", "floor", "lift", "balkonies", "loggia", "cellar", "type", "rooms", "district"]
- `data/train.csv` (1509349 bytes); columns: ["Id", "name_nsi", "index", "environment", "quality_of_living", "safety", "transport", "services", "relax", "condition", "area", "energy_costs", "provision", "certificate", "construction_type", "orientation", "year_built", "last_reconstruction", "total_floors", "floor", "lift", "balkonies", "loggia", "cellar", "type", "rooms", "district", "price"]

## Public description

```
description.txt (57 lines)
sample_submission.csv (2991 lines)
test.csv (2991 lines)
train.csv (11980 lines)```

-> sample_submission.csv has 2990 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 200000.00 - 202989.00, 0 nan values
price (float64) has range: 24698.03 - 1143056.00, 0 nan values

-> test.csv has 2990 rows and 27 columns.
Here is some information about the columns:
Id (int64) has range: 200000.00 - 202989.00, 0 nan values
area (float64) has range: 1.00 - 187900.00, 157 nan values
balkonies (float64) has 3 unique values: [nan, 1.0, 3.0, 2.0]
cellar (int64) has 2 unique values: [0, 1]
certificate (object) has 8 unique values: [nan, 'none', 'B', 'A', 'D', 'C', 'G', 'E', 'F']
condition (object) has 6 unique values: ['Under construction', 'Original condition', 'New building', 'Partial reconstruction', 'Complete reconstruction', nan, 'Development project']
construction_type (object) has 7 unique values: [nan, 'Brick', 'Other', 'Panel', 'Mixed', 'Brick, Reinforced concrete', 'Cube', 'Mounted']
district (object) has 77 unique values. Some example values: ['Bratislava II', 'Bratislava IV', 'Bratislava V', 'Bratislava I']
energy_costs (float64) has range: 26.00 - 347.00, 2814 nan values
environment (float64) has range: 4.60 - 9.80, 2204 nan values
floor (float64) has range: -7.00 - 26.00, 1392 nan values
index (float64) has range: 3.70 - 9.20, 1997 nan values
last_reconstruction (float64) has range: 2001.00 - 2023.00, 2865 nan values
lift (int64) has 2 unique values: [1, 0]
loggia (float64) has 4 unique values: [1.0, nan, 2.0, 3.0, 5.0]
name_nsi (object) has 320 unique values. Some example values: ['Bratislava - mestská časť Ružinov', 'Bratislava - mestská časť Staré Mesto', 'Bratislava - mestská časť Petržalka', 'Žilina']
orientation (object) has 8 unique values: [nan, 'Southeast', 'South', 'Southwest', 'East', 'West', 'Northwest', 'Northeast', 'North']
provision (int64) has 2 unique values: [1, 0]
quality_of_living (float64) has range: 3.80 - 10.00, 2204 nan values
relax (float64) has range: 2.00 - 9.40, 2204 nan values
rooms (int64) has 5 unique values: [4, 3, 2, 1, 5]
safety (float64) has range: 2.00 - 10.00, 2204 nan values
services (float64) has range: 2.00 - 10.00, 2204 nan values
total_floors (float64) has range: 1.00 - 45.00, 1609 nan values
transport (float64) has range: 2.00 - 10.00, 2204 nan values
type (object) has 7 unique values: ['4-room apartment', '3-room apartment', '2-room apartment', '1-room apartment', 'Studio', '5 or more room apartment', 'Two-room apartment']
year_built (float64) has range: 1.00 - 19741.00, 2238 nan values

-> train.csv has 11979 rows and 28 columns.
Here is some information about the columns:
Id (int64) has range: 100000.00 - 111978.00, 0 nan values
area (float64) has range: 1.00 - 209900.00, 532 nan values
balkonies (float64) has 5 unique values: [nan, 2.0, 1.0, 3.0, 4.0, 6.0]
cellar (int64) has 2 unique values: [0, 1]
certificate (object) has 8 unique values: [nan, 'none', 'A', 'C', 'G', 'B', 'D', 'F', 'E']
condition (object) has 6 unique values: ['Complete reconstruction', 'New building', 'Original condition', 'Partial reconstruction', nan, 'Under construction', 'Development project']
construction_type (object) has 10 unique values. Some example values: ['Brick', 'Panel', 'Other', 'Mixed']
district (object) has 79 unique values. Some example values: ['Bratislava II', 'Bratislava IV', 'Bratislava V', 'Bratislava I']
energy_costs (float64) has range: 20.00 - 365.00, 11211 nan values
environment (float64) has range: 2.70 - 10.00, 8719 nan values
floor (float64) has range: -4.00 - 34.00, 5466 nan values
index (float64) has range: 3.30 - 9.50, 7915 nan values
last_reconstruction (float64) has range: 1968.00 - 2024.00, 11437 nan values
lift (int64) has 2 unique values: [0, 1]
loggia (float64) has 4 unique values: [nan, 1.0, 2.0, 3.0, 4.0]
name_nsi (object) has 555 unique values. Some example values: ['Bratislava - mestská časť Ružinov', 'Bratislava - mestská časť Staré Mesto', 'Bratislava - mestská časť Petržalka', 'Žilina']
orientation (object) has 8 unique values: [nan, 'Southwest', 'West', 'South', 'Southeast', 'East', 'Northwest', 'Northeast', 'North']
price (int64) has range: 11500.00 - 9936000.00, 0 nan values
provision (int64) has 2 unique values: [0, 1]
quality_of_living (float64) has range: 2.70 - 10.00, 8719 nan values
relax (float64) has range: 2.00 - 9.50, 8719 nan values
rooms (int64) has 5 unique values: [2, 3, 1, 4, 5]
safety (float64) has range: 2.00 - 10.00, 8719 nan values
services (float64) has range: 2.00 - 10.00, 8719 nan values
total_floors (float64) has range: 1.00 - 46.00, 6225 nan values
transport (float64) has range: 2.00 - 10.00, 8719 nan values
type (object) has 7 unique values: ['2-room apartment', '3-room apartment', 'Studio', '4-room apartment', '1-room apartment', '5 or more room apartment', 'Two-room apartment']
year_built (float64) has range: 1.00 - 2222.00, 8951 nan values
