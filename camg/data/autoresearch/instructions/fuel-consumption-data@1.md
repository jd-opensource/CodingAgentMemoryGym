# OpenMLE-fast task

Task ID: `fuel-consumption-data@1`

Native metric: `CO2EmissionsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1950 bytes)
- `data/sample_submission.csv` (7956 bytes); columns: ["id", "CO2EMISSIONS"]
- `data/test.csv` (12274 bytes); columns: ["id", "MODELYEAR", "MAKE", "VEHICLECLASS", "ENGINESIZE", "CYLINDERS", "TRANSMISSION", "FUELTYPE"]
- `data/train.csv` (44361 bytes); columns: ["id", "MODELYEAR", "MAKE", "VEHICLECLASS", "ENGINESIZE", "CYLINDERS", "TRANSMISSION", "FUELTYPE", "CO2EMISSIONS"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (246 lines)
test.csv (246 lines)
train.csv (823 lines)```

-> sample_submission.csv has 245 rows and 2 columns.
Here is some information about the columns:
CO2EMISSIONS (float64) has range: 108.00 - 457.73, 0 nan values
id (object) has 245 unique values. Some example values: ['r00004_640081', 'r00007_371376', 'r00008_513150', 'r00013_804681']

-> test.csv has 245 rows and 8 columns.
Here is some information about the columns:
CYLINDERS (int64) has 5 unique values: [6, 12, 8, 4, 5]
ENGINESIZE (float64) has range: 1.00 - 6.70, 0 nan values
FUELTYPE (object) has 4 unique values: ['Z', 'D', 'X', 'E']
MAKE (object) has 35 unique values. Some example values: ['FORD', 'CHEVROLET', 'BMW', 'GMC']
MODELYEAR (int64) has 1 unique values: [2014]
TRANSMISSION (object) has 17 unique values. Some example values: ['AS6', 'A6', 'M6', 'A8']
VEHICLECLASS (object) has 16 unique values. Some example values: ['MID-SIZE', 'SUV - SMALL', 'COMPACT', 'SUV - STANDARD']
id (object) has 245 unique values. Some example values: ['r00004_640081', 'r00007_371376', 'r00008_513150', 'r00013_804681']

-> train.csv has 822 rows and 9 columns.
Here is some information about the columns:
CO2EMISSIONS (int64) has range: 108.00 - 488.00, 0 nan values
CYLINDERS (int64) has 7 unique values: [4, 6, 12, 8, 10, 3, 5]
ENGINESIZE (float64) has range: 1.00 - 8.40, 0 nan values
FUELTYPE (object) has 4 unique values: ['Z', 'D', 'X', 'E']
MAKE (object) has 39 unique values. Some example values: ['CHEVROLET', 'FORD', 'MERCEDES-BENZ', 'BMW']
MODELYEAR (int64) has 1 unique values: [2014]
TRANSMISSION (object) has 22 unique values. Some example values: ['A6', 'AS6', 'M6', 'AS8']
VEHICLECLASS (object) has 16 unique values. Some example values: ['MID-SIZE', 'COMPACT', 'SUV - SMALL', 'SUV - STANDARD']
id (object) has 822 unique values. Some example values: ['r01066_650905', 'r00000_729556', 'r00001_770792', 'r00002_756742']
