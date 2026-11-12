# OpenMLE-fast task

Task ID: `science-data@1`

Native metric: `AmazonSubdivisionF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1246 bytes)
- `data/sample_submission.csv` (7130 bytes); columns: ["id", "Subdivision"]
- `data/test.csv` (8914 bytes); columns: ["id", "lat", "lon", "altitude"]
- `data/train.csv` (49007 bytes); columns: ["id", "lat", "lon", "altitude", "Subdivision"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (379 lines)
test.csv (379 lines)
train.csv (1513 lines)```

-> sample_submission.csv has 378 rows and 2 columns.
Here is some information about the columns:
Subdivision (object) has 43 unique values. Some example values: ['Rondônia', 'Régina', 'Cusco', 'Para']
id (object) has 378 unique values. Some example values: ['ID000377', 'ID000000', 'ID000001', 'ID000002']

-> test.csv has 378 rows and 4 columns.
Here is some information about the columns:
altitude (float64) has range: 0.00 - 747.00, 307 nan values
id (object) has 378 unique values. Some example values: ['ID000377', 'ID000000', 'ID000001', 'ID000002']
lat (float64) has range: -17.09 - 8.24, 0 nan values
lon (float64) has range: -77.50 - -46.15, 0 nan values

-> train.csv has 1512 rows and 5 columns.
Here is some information about the columns:
Subdivision (object) has 57 unique values. Some example values: ['Pará', 'Amazonas', 'Amapá', 'Loreto']
altitude (float64) has range: 0.00 - 815.00, 1173 nan values
id (object) has 1512 unique values. Some example values: ['ID001511', 'ID000000', 'ID000001', 'ID000002']
lat (float64) has range: -17.09 - 8.25, 0 nan values
lon (float64) has range: -78.77 - -45.10, 0 nan values
