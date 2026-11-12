# OpenMLE-fast task

Task ID: `water-potability-prediction@1`

Native metric: `WaterPotabilityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1684 bytes)
- `data/sample_submission.csv` (13657 bytes); columns: ["row_id", "Potability"]
- `data/test.csv` (158986 bytes); columns: ["row_id", "ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
- `data/train.csv` (368156 bytes); columns: ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity", "Potability"]

## Public description

```
description.txt (35 lines)
sample_submission.csv (983 lines)
test.csv (983 lines)
train.csv (2295 lines)```

-> sample_submission.csv has 982 rows and 2 columns.
Here is some information about the columns:
Potability (float64) has range: 0.00 - 1.00, 0 nan values
row_id (int64) has range: 0.00 - 981.00, 0 nan values

-> test.csv has 982 rows and 10 columns.
Here is some information about the columns:
Chloramines (float64) has range: 0.53 - 12.65, 0 nan values
Conductivity (float64) has range: 217.36 - 674.44, 0 nan values
Hardness (float64) has range: 73.49 - 308.25, 0 nan values
Organic_carbon (float64) has range: 4.47 - 28.30, 0 nan values
Solids (float64) has range: 320.94 - 61227.20, 0 nan values
Sulfate (float64) has range: 129.00 - 458.44, 262 nan values
Trihalomethanes (float64) has range: 15.68 - 120.03, 47 nan values
Turbidity (float64) has range: 1.45 - 6.31, 0 nan values
ph (float64) has range: 0.98 - 13.54, 142 nan values
row_id (int64) has range: 0.00 - 981.00, 0 nan values

-> train.csv has 2294 rows and 10 columns.
Here is some information about the columns:
Chloramines (float64) has range: 0.35 - 13.13, 0 nan values
Conductivity (float64) has range: 181.48 - 753.34, 0 nan values
Hardness (float64) has range: 47.43 - 323.12, 0 nan values
Organic_carbon (float64) has range: 2.20 - 27.01, 0 nan values
Potability (int64) has 2 unique values: [0, 1]
Solids (float64) has range: 728.75 - 53735.90, 0 nan values
Sulfate (float64) has range: 180.21 - 481.03, 519 nan values
Trihalomethanes (float64) has range: 0.74 - 124.00, 115 nan values
Turbidity (float64) has range: 1.49 - 6.74, 0 nan values
ph (float64) has range: 0.00 - 14.00, 349 nan values
