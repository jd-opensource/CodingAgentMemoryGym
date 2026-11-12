# OpenMLE-fast task

Task ID: `water-quality-and-potability@1`

Native metric: `WaterPotabilityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1916 bytes)
- `data/sample_submission.csv` (24805 bytes); columns: ["Id", "Potability"]
- `data/test.csv` (137429 bytes); columns: ["Id", "ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
- `data/train.csv` (415946 bytes); columns: ["Id", "ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity", "Potability"]

## Public description

```
description.txt (37 lines)
sample_submission.csv (821 lines)
test.csv (821 lines)
train.csv (2457 lines)```

-> sample_submission.csv has 820 rows and 2 columns.
Here is some information about the columns:
Id (object) has 820 unique values. Some example values: ['WQ05236973', 'WQ04993854', 'WQ03596114', 'WQ05547308']
Potability (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 820 rows and 10 columns.
Here is some information about the columns:
Chloramines (float64) has range: 0.53 - 13.04, 0 nan values
Conductivity (float64) has range: 217.36 - 669.73, 0 nan values
Hardness (float64) has range: 47.43 - 311.38, 0 nan values
Id (object) has 820 unique values. Some example values: ['WQ05236973', 'WQ04993854', 'WQ03596114', 'WQ05547308']
Organic_carbon (float64) has range: 2.20 - 28.30, 0 nan values
Solids (float64) has range: 2912.21 - 56488.67, 0 nan values
Sulfate (float64) has range: 129.00 - 476.54, 187 nan values
Trihalomethanes (float64) has range: 8.58 - 120.03, 31 nan values
Turbidity (float64) has range: 1.50 - 6.31, 0 nan values
ph (float64) has range: 0.00 - 13.54, 131 nan values

-> train.csv has 2456 rows and 11 columns.
Here is some information about the columns:
Chloramines (float64) has range: 0.35 - 13.13, 0 nan values
Conductivity (float64) has range: 181.48 - 753.34, 0 nan values
Hardness (float64) has range: 73.49 - 323.12, 0 nan values
Id (object) has 2456 unique values. Some example values: ['WQ02591408', 'WQ06984933', 'WQ06965823', 'WQ00413202']
Organic_carbon (float64) has range: 4.37 - 27.01, 0 nan values
Potability (int64) has 2 unique values: [1, 0]
Solids (float64) has range: 320.94 - 61227.20, 0 nan values
Sulfate (float64) has range: 182.40 - 481.03, 594 nan values
Trihalomethanes (float64) has range: 0.74 - 124.00, 131 nan values
Turbidity (float64) has range: 1.45 - 6.74, 0 nan values
ph (float64) has range: 0.23 - 14.00, 360 nan values
