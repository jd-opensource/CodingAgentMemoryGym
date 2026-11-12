# OpenMLE-fast task

Task ID: `real-estate-dataset@2`

Native metric: `RealEstateConditionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5005 bytes)
- `data/sample_submission.csv` (78230 bytes); columns: ["id", "condition"]
- `data/test.csv` (315234 bytes); columns: ["id", "name_nsi", "price", "index", "environment", "quality_of_living", "safety", "transport", "services", "relax", "area", "energy_costs", "provision", "certificate", "construction_type", "orientation", "year_built", "last_reconstruction", "total_floors", "floor", "lift", "balkonies", "loggia", "cellar", "type", "rooms", "district"]
- `data/train.csv` (1482233 bytes); columns: ["id", "name_nsi", "price", "index", "environment", "quality_of_living", "safety", "transport", "services", "relax", "condition", "area", "energy_costs", "provision", "certificate", "construction_type", "orientation", "year_built", "last_reconstruction", "total_floors", "floor", "lift", "balkonies", "loggia", "cellar", "type", "rooms", "district"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (2934 lines)
test.csv (2934 lines)
train.csv (11731 lines)```

-> sample_submission.csv has 2933 rows and 2 columns.
Here is some information about the columns:
condition (object) has 6 unique values: ['Complete reconstruction', 'Partial reconstruction', 'Original condition', 'New building', 'Under construction', 'Development project']
id (int64) has range: 100000.00 - 114661.00, 0 nan values

-> test.csv has 2933 rows and 27 columns.
Here is some information about the columns:
area (float64) has range: 1.00 - 693.00, 86 nan values
balkonies (float64) has 4 unique values: [nan, 1.0, 4.0, 2.0, 3.0]
cellar (int64) has 2 unique values: [0, 1]
certificate (object) has 7 unique values: [nan, 'C', 'none', 'B', 'A', 'G', 'D', 'E']
construction_type (object) has 8 unique values: [nan, 'Brick', 'Panel', 'Other', 'Mixed', 'Skeletal', 'Cube', 'Brick, Reinforced concrete', 'Panel, Brick']
district (object) has 74 unique values. Some example values: ['Bratislava II', 'Bratislava V', 'Bratislava IV', 'Bratislava I']
energy_costs (float64) has range: 21.00 - 325.00, 2710 nan values
environment (float64) has range: 2.70 - 9.90, 2109 nan values
floor (float64) has range: 1.00 - 17.00, 1278 nan values
id (int64) has range: 100000.00 - 114661.00, 0 nan values
index (float64) has range: 3.30 - 9.30, 1907 nan values
last_reconstruction (float64) has range: 2001.00 - 2024.00, 2805 nan values
lift (int64) has 2 unique values: [0, 1]
loggia (float64) has 3 unique values: [nan, 1.0, 2.0, 3.0]
name_nsi (object) has 329 unique values. Some example values: ['Bratislava - mestská časť Ružinov', 'Bratislava - mestská časť Petržalka', 'Bratislava - mestská časť Staré Mesto', 'Nitra']
orientation (object) has 8 unique values: [nan, 'Southwest', 'South', 'Southeast', 'West', 'Northwest', 'East', 'Northeast', 'North']
price (int64) has range: 11500.00 - 1580000.00, 0 nan values
provision (int64) has 2 unique values: [0, 1]
quality_of_living (float64) has range: 4.00 - 10.00, 2109 nan values
relax (float64) has range: 2.00 - 9.50, 2109 nan values
rooms (int64) has 5 unique values: [3, 2, 1, 4, 5]
safety (float64) has range: 2.00 - 10.00, 2109 nan values
services (float64) has range: 2.00 - 10.00, 2109 nan values
total_floors (float64) has range: 1.00 - 45.00, 1468 nan values
transport (float64) has range: 2.00 - 10.00, 2109 nan values
type (object) has 7 unique values: ['3-room apartment', '2-room apartment', '1-room apartment', '4-room apartment', 'Studio', '5 or more room apartment', 'Two-room apartment']
year_built (float64) has range: 1.00 - 2024.00, 2147 nan values

-> train.csv has 11730 rows and 28 columns.
Here is some information about the columns:
area (float64) has range: 1.00 - 209900.00, 301 nan values
balkonies (float64) has 5 unique values: [nan, 1.0, 2.0, 3.0, 4.0, 6.0]
cellar (int64) has 2 unique values: [0, 1]
certificate (object) has 8 unique values: [nan, 'none', 'B', 'A', 'C', 'D', 'G', 'E', 'F']
condition (object) has 6 unique values: ['Original condition', 'Partial reconstruction', 'Complete reconstruction', 'New building', 'Development project', 'Under construction']
construction_type (object) has 11 unique values. Some example values: ['Brick', 'Panel', 'Other', 'Mixed']
district (object) has 79 unique values. Some example values: ['Bratislava II', 'Bratislava IV', 'Bratislava I', 'Bratislava V']
energy_costs (float64) has range: 20.00 - 365.00, 11009 nan values
environment (float64) has range: 2.70 - 10.00, 8511 nan values
floor (float64) has range: -7.00 - 34.00, 5276 nan values
id (int64) has range: 100001.00 - 114662.00, 0 nan values
index (float64) has range: 3.30 - 9.50, 7702 nan values
last_reconstruction (float64) has range: 1968.00 - 2024.00, 11191 nan values
lift (int64) has 2 unique values: [0, 1]
loggia (float64) has 5 unique values: [nan, 1.0, 2.0, 3.0, 4.0, 5.0]
name_nsi (object) has 550 unique values. Some example values: ['Bratislava - mestská časť Ružinov', 'Bratislava - mestská časť Staré Mesto', 'Bratislava - mestská časť Petržalka', 'Žilina']
orientation (object) has 8 unique values: [nan, 'Southwest', 'Southeast', 'South', 'Northwest', 'East', 'West', 'Northeast', 'North']
price (int64) has range: 11500.00 - 9936000.00, 0 nan values
provision (int64) has 2 unique values: [0, 1]
quality_of_living (float64) has range: 2.70 - 10.00, 8511 nan values
relax (float64) has range: 2.00 - 9.40, 8511 nan values
rooms (int64) has 5 unique values: [1, 2, 3, 5, 4]
safety (float64) has range: 2.00 - 10.00, 8511 nan values
services (float64) has range: 2.00 - 10.00, 8511 nan values
total_floors (float64) has range: 1.00 - 46.00, 6062 nan values
transport (float64) has range: 2.00 - 10.00, 8511 nan values
type (object) has 7 unique values: ['1-room apartment', '2-room apartment', '3-room apartment', '5 or more room apartment', '4-room apartment', 'Studio', 'Two-room apartment']
year_built (float64) has range: 1.00 - 19741.00, 8736 nan values
