# OpenMLE-fast task

Task ID: `real-estate-sales-2001-2020@1`

Native metric: `RealEstateSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1992 bytes)
- `data/sample_submission.csv` (442204 bytes); columns: ["Serial Number", "Sale Amount"]
- `data/test.csv` (1188638 bytes); columns: ["Serial Number", "List Year", "Town", "Address", "Assessed Value", "Property Type", "Residential Type"]
- `data/train.csv` (4892373 bytes); columns: ["Serial Number", "List Year", "Town", "Address", "Assessed Value", "Property Type", "Residential Type", "Sale Amount"]

## Public description

```
description.txt (50 lines)
sample_submission.csv (16976 lines)
test.csv (16976 lines)
train.csv (66426 lines)```

-> sample_submission.csv has 16975 rows and 2 columns.
Here is some information about the columns:
Sale Amount (float64) has range: 0.00 - 318863290.88, 0 nan values
Serial Number (int64) has range: 1901.00 - 2000500023.00, 0 nan values

-> test.csv has 16975 rows and 7 columns.
Here is some information about the columns:
Address (object) has 16664 unique values. Some example values: ['24 HANOVER STREET', '498A NIANTIC LANE', '54 DUNN AVENUE', '89 LANCE CIRCLE']
Assessed Value (int64) has range: 0.00 - 114924210.00, 0 nan values
List Year (int64) has 2 unique values: [2020, 2019]
Property Type (object) has 12 unique values. Some example values: ['Residential', 'Single Family', 'Condo', 'Nan']
Residential Type (object) has 6 unique values: ['Unknown', 'Single Family', 'Condo', 'Two Family', 'Three Family', 'Four Family']
Serial Number (int64) has range: 1901.00 - 2000500023.00, 0 nan values
Town (object) has 148 unique values. Some example values: ['Stamford', 'Stratford', 'Norwalk', 'Bridgeport']

-> train.csv has 66425 rows and 8 columns.
Here is some information about the columns:
Address (object) has 62304 unique values. Some example values: ['312 N BISHOP AVE', 'MULTI ADDRESSES', '325 LAFAYETTE ST', '2743 FAIRFIELD AVE']
Assessed Value (int64) has range: 0.00 - 105438300.00, 0 nan values
List Year (int64) has range: 2001.00 - 2018.00, 0 nan values
Property Type (object) has 6 unique values: ['Nan', 'Condo', 'Two Family', 'Three Family', 'Single Family', 'Four Family']
Residential Type (object) has 6 unique values: ['Unknown', 'Condo', 'Two Family', 'Three Family', 'Single Family', 'Four Family']
Sale Amount (float64) has range: 5025.00 - 163000000.00, 0 nan values
Serial Number (int64) has range: 81.00 - 1710011174.00, 0 nan values
Town (object) has 169 unique values. Some example values: ['Bridgeport', 'Stamford', 'New Haven', 'Danbury']
