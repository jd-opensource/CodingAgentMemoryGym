# OpenMLE-fast task

Task ID: `crop-yield-prediction-dataset@1`

Native metric: `CropYieldRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1700 bytes)
- `data/sample_submission.csv` (86414 bytes); columns: ["row_id", "hg/ha_yield"]
- `data/test.csv` (162916 bytes); columns: ["Area", "Item", "Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp", "row_id"]
- `data/train.csv` (534949 bytes); columns: ["Area", "Item", "Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp", "hg/ha_yield"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (2938 lines)
test.csv (2938 lines)
train.csv (10194 lines)```

-> sample_submission.csv has 2937 rows and 2 columns.
Here is some information about the columns:
hg/ha_yield (float64) has range: 46.08 - 501599.84, 0 nan values
row_id (object) has 2937 unique values. Some example values: ['row_002936', 'row_000000', 'row_000001', 'row_000002']

-> test.csv has 2937 rows and 7 columns.
Here is some information about the columns:
Area (object) has 101 unique values. Some example values: ['Cameroon', 'Kenya', 'Colombia', 'Brazil']
Item (object) has 10 unique values. Some example values: ['Potatoes', 'Maize', 'Wheat', 'Rice, paddy']
Year (int64) has 5 unique values: [2009, 2010, 2011, 2012, 2013]
average_rain_fall_mm_per_year (float64) has range: 51.00 - 3240.00, 0 nan values
avg_temp (float64) has range: 1.30 - 30.42, 0 nan values
pesticides_tonnes (float64) has range: 0.55 - 367778.00, 0 nan values
row_id (object) has 2937 unique values. Some example values: ['row_002936', 'row_000000', 'row_000001', 'row_000002']

-> train.csv has 10193 rows and 7 columns.
Here is some information about the columns:
Area (object) has 100 unique values. Some example values: ['Cameroon', 'Kenya', 'Brazil', 'Colombia']
Item (object) has 10 unique values. Some example values: ['Potatoes', 'Maize', 'Wheat', 'Rice, paddy']
Year (int64) has range: 1990.00 - 2008.00, 0 nan values
average_rain_fall_mm_per_year (float64) has range: 51.00 - 3240.00, 0 nan values
avg_temp (float64) has range: 1.88 - 30.02, 0 nan values
hg/ha_yield (float64) has range: 50.00 - 487219.00, 0 nan values
pesticides_tonnes (float64) has range: 0.04 - 312637.00, 0 nan values
