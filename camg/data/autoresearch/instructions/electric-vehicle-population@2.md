# OpenMLE-fast task

Task ID: `electric-vehicle-population@2`

Native metric: `ElectricVehicleCafvEligibilityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3791 bytes)
- `data/sample_submission.csv` (599616 bytes); columns: ["DOL Vehicle ID", "CAFV_Eligible"]
- `data/test.csv` (4159841 bytes); columns: ["VIN (1-10)", "County", "City", "State", "Postal Code", "Model Year", "Make", "Model", "Electric Vehicle Type", "Base MSRP", "Legislative District", "DOL Vehicle ID", "Vehicle Location", "Electric Utility", "2020 Census Tract"]
- `data/train.csv` (15028324 bytes); columns: ["VIN (1-10)", "County", "City", "State", "Postal Code", "Model Year", "Make", "Model", "Electric Vehicle Type", "Base MSRP", "Legislative District", "DOL Vehicle ID", "Vehicle Location", "Electric Utility", "2020 Census Tract", "CAFV_Eligible"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (19855 lines)
test.csv (19855 lines)
train.csv (75512 lines)```

-> sample_submission.csv has 19854 rows and 2 columns.
Here is some information about the columns:
CAFV_Eligible (float64) has range: 0.00 - 1.00, 0 nan values
DOL Vehicle ID (int64) has range: 209460856.00 - 285335354.00, 0 nan values

-> test.csv has 19854 rows and 15 columns.
Here is some information about the columns:
2020 Census Tract (float64) has range: 1001020100.00 - 53077940008.00, 0 nan values
Base MSRP (float64) has 1 unique values: [0.0, nan]
City (object) has 381 unique values. Some example values: ['Seattle', 'Tukwila', 'Renton', 'Vancouver']
County (object) has 62 unique values. Some example values: ['King', 'Snohomish', 'Pierce', 'Clark']
DOL Vehicle ID (int64) has range: 209460856.00 - 285335354.00, 0 nan values
Electric Utility (object) has 66 unique values. Some example values: ['PUGET SOUND ENERGY INC||CITY OF TACOMA - (WA)', 'PUGET SOUND ENERGY INC', 'CITY OF SEATTLE - (WA)|CITY OF TACOMA - (WA)', 'BONNEVILLE POWER ADMINISTRATION||PUD NO 1 OF CLARK COUNTY - (WA)']
Electric Vehicle Type (object) has 2 unique values: ['Plug-in Hybrid Electric Vehicle (PHEV)', 'Battery Electric Vehicle (BEV)']
Legislative District (float64) has range: 1.00 - 49.00, 31 nan values
Make (object) has 21 unique values. Some example values: ['JEEP', 'TOYOTA', 'KIA', 'CHRYSLER']
Model (object) has 45 unique values. Some example values: ['WRANGLER', 'RAV4 PRIME', 'PACIFICA', 'X5']
Model Year (int64) has 3 unique values: [2023, 2024, 2025]
Postal Code (float64) has range: 4444.00 - 99403.00, 0 nan values
State (object) has 20 unique values. Some example values: ['WA', 'VA', 'TX', 'CA']
VIN (1-10) (object) has 1776 unique values. Some example values: ['1C4RJXN60R', '2C4RC1L72P', '2C4RC1L7XP', '2C4RC1L78P']
Vehicle Location (object) has 470 unique values. Some example values: ['POINT (-122.29179 47.43473)', 'POINT (-122.20489 47.47532)', 'POINT (-122.13158 47.67858)', 'POINT (-122.31676 47.68156)']

-> train.csv has 75511 rows and 16 columns.
Here is some information about the columns:
2020 Census Tract (float64) has range: 1081041901.00 - 55009020504.00, 3 nan values
Base MSRP (float64) has range: 0.00 - 845000.00, 0 nan values
CAFV_Eligible (int64) has 2 unique values: [1, 0]
City (object) has 577 unique values. Some example values: ['Seattle', 'Bellevue', 'Vancouver', 'Redmond']
County (object) has 140 unique values. Some example values: ['King', 'Snohomish', 'Pierce', 'Clark']
DOL Vehicle ID (int64) has range: 4385.00 - 479254772.00, 0 nan values
Electric Utility (object) has 72 unique values. Some example values: ['PUGET SOUND ENERGY INC||CITY OF TACOMA - (WA)', 'PUGET SOUND ENERGY INC', 'CITY OF SEATTLE - (WA)|CITY OF TACOMA - (WA)', 'BONNEVILLE POWER ADMINISTRATION||PUD NO 1 OF CLARK COUNTY - (WA)']
Electric Vehicle Type (object) has 2 unique values: ['Battery Electric Vehicle (BEV)', 'Plug-in Hybrid Electric Vehicle (PHEV)']
Legislative District (float64) has range: 1.00 - 49.00, 200 nan values
Make (object) has 32 unique values. Some example values: ['TESLA', 'NISSAN', 'CHEVROLET', 'TOYOTA']
Model (object) has 88 unique values. Some example values: ['MODEL 3', 'LEAF', 'MODEL S', 'BOLT EV']
Model Year (int64) has range: 1999.00 - 2022.00, 0 nan values
Postal Code (float64) has range: 2110.00 - 99403.00, 3 nan values
State (object) has 40 unique values. Some example values: ['WA', 'CA', 'VA', 'MD']
VIN (1-10) (object) has 5773 unique values. Some example values: ['5YJ3E1EB1J', '5YJ3E1EB4J', '5YJ3E1EB6J', '5YJ3E1EB8J']
Vehicle Location (object) has 691 unique values. Some example values: ['POINT (-122.13158 47.67858)', 'POINT (-122.31676 47.68156)', 'POINT (-122.2066 47.67887)', 'POINT (-122.35436 47.67596)']
