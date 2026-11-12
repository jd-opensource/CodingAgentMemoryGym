# OpenMLE-fast task

Task ID: `crop-based-on-npk@1`

Native metric: `CropRecommendationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1144 bytes)
- `data/sample_submission.csv` (5652 bytes); columns: ["row_id", "crop"]
- `data/test.csv` (12009 bytes); columns: ["row_id", "N", "P", "K", "ph"]
- `data/train.csv` (64214 bytes); columns: ["N", "P", "K", "ph", "crop", "row_id"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (441 lines)
test.csv (441 lines)
train.csv (1761 lines)```

-> sample_submission.csv has 440 rows and 2 columns.
Here is some information about the columns:
crop (object) has 22 unique values. Some example values: ['watermelon', 'coffee', 'papaya', 'orange']
row_id (int64) has range: 0.00 - 439.00, 0 nan values

-> test.csv has 440 rows and 5 columns.
Here is some information about the columns:
K (int64) has range: 7.00 - 205.00, 0 nan values
N (int64) has range: 0.00 - 136.00, 0 nan values
P (int64) has range: 5.00 - 145.00, 0 nan values
ph (float64) has range: 3.81 - 9.93, 0 nan values
row_id (int64) has range: 0.00 - 439.00, 0 nan values

-> train.csv has 1760 rows and 6 columns.
Here is some information about the columns:
K (int64) has range: 5.00 - 205.00, 0 nan values
N (int64) has range: 0.00 - 140.00, 0 nan values
P (int64) has range: 5.00 - 145.00, 0 nan values
crop (object) has 22 unique values. Some example values: ['apple', 'banana', 'blackgram', 'chickpea']
ph (float64) has range: 3.50 - 9.94, 0 nan values
row_id (int64) has range: 440.00 - 2199.00, 0 nan values
