# OpenMLE-fast task

Task ID: `crop-recommendation-dataset@1`

Native metric: `CropRecommendationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1484 bytes)
- `data/sample_submission.csv` (5569 bytes); columns: ["id", "label"]
- `data/test.csv` (27946 bytes); columns: ["id", "N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
- `data/train.csv` (126180 bytes); columns: ["id", "N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (441 lines)
test.csv (441 lines)
train.csv (1761 lines)```

-> sample_submission.csv has 440 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 12.00 - 2199.00, 0 nan values
label (object) has 22 unique values. Some example values: ['cotton', 'mango', 'coffee', 'mungbean']

-> test.csv has 440 rows and 8 columns.
Here is some information about the columns:
K (int64) has range: 5.00 - 205.00, 0 nan values
N (int64) has range: 0.00 - 139.00, 0 nan values
P (int64) has range: 5.00 - 145.00, 0 nan values
humidity (float64) has range: 14.70 - 99.98, 0 nan values
id (int64) has range: 12.00 - 2199.00, 0 nan values
ph (float64) has range: 3.50 - 9.94, 0 nan values
rainfall (float64) has range: 20.76 - 295.92, 0 nan values
temperature (float64) has range: 9.85 - 43.36, 0 nan values

-> train.csv has 1760 rows and 9 columns.
Here is some information about the columns:
K (int64) has range: 5.00 - 205.00, 0 nan values
N (int64) has range: 0.00 - 140.00, 0 nan values
P (int64) has range: 5.00 - 145.00, 0 nan values
humidity (float64) has range: 14.26 - 99.85, 0 nan values
id (int64) has range: 0.00 - 2198.00, 0 nan values
label (object) has 22 unique values. Some example values: ['jute', 'coffee', 'maize', 'pigeonpeas']
ph (float64) has range: 3.51 - 9.93, 0 nan values
rainfall (float64) has range: 20.21 - 298.56, 0 nan values
temperature (float64) has range: 8.83 - 43.68, 0 nan values
