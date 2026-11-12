# OpenMLE-fast task

Task ID: `dry-bean-dataset@1`

Native metric: `DryBeanMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2715 bytes)
- `data/sample_submission.csv` (37453 bytes); columns: ["Id", "Class"]
- `data/test.csv` (746232 bytes); columns: ["Id", "Area", "Perimeter", "MajorAxisLength", "MinorAxisLength", "AspectRation", "Eccentricity", "ConvexArea", "EquivDiameter", "Extent", "Solidity", "roundness", "Compactness", "ShapeFactor1", "ShapeFactor2", "ShapeFactor3", "ShapeFactor4"]
- `data/train.csv` (3058530 bytes); columns: ["Id", "Area", "Perimeter", "MajorAxisLength", "MinorAxisLength", "AspectRation", "Eccentricity", "ConvexArea", "EquivDiameter", "Extent", "Solidity", "roundness", "Compactness", "ShapeFactor1", "ShapeFactor2", "ShapeFactor3", "ShapeFactor4", "Class"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (2722 lines)
test.csv (2722 lines)
train.csv (10891 lines)```

-> sample_submission.csv has 2721 rows and 2 columns.
Here is some information about the columns:
Class (object) has 7 unique values: ['SIRA', 'BARBUNYA', 'HOROZ', 'SEKER', 'DERMASON', 'CALI', 'BOMBAY']
Id (int64) has range: 100002.00 - 113608.00, 0 nan values

-> test.csv has 2721 rows and 17 columns.
Here is some information about the columns:
Area (int64) has range: 20942.00 - 233751.00, 0 nan values
AspectRation (float64) has range: 1.04 - 2.36, 0 nan values
Compactness (float64) has range: 0.65 - 0.98, 0 nan values
ConvexArea (int64) has range: 21191.00 - 237344.00, 0 nan values
Eccentricity (float64) has range: 0.28 - 0.91, 0 nan values
EquivDiameter (float64) has range: 163.29 - 545.55, 0 nan values
Extent (float64) has range: 0.57 - 0.84, 0 nan values
Id (int64) has range: 100002.00 - 113608.00, 0 nan values
MajorAxisLength (float64) has range: 191.18 - 713.37, 0 nan values
MinorAxisLength (float64) has range: 130.74 - 449.34, 0 nan values
Perimeter (float64) has range: 530.68 - 1849.37, 0 nan values
ShapeFactor1 (float64) has range: 0.00 - 0.01, 0 nan values
ShapeFactor2 (float64) has range: 0.00 - 0.00, 0 nan values
ShapeFactor3 (float64) has range: 0.42 - 0.96, 0 nan values
ShapeFactor4 (float64) has range: 0.96 - 1.00, 0 nan values
Solidity (float64) has range: 0.95 - 0.99, 0 nan values
roundness (float64) has range: 0.56 - 0.98, 0 nan values

-> train.csv has 10890 rows and 18 columns.
Here is some information about the columns:
Area (int64) has range: 20420.00 - 254616.00, 0 nan values
AspectRation (float64) has range: 1.02 - 2.43, 0 nan values
Class (object) has 7 unique values: ['SEKER', 'BARBUNYA', 'BOMBAY', 'CALI', 'HOROZ', 'SIRA', 'DERMASON']
Compactness (float64) has range: 0.64 - 0.99, 0 nan values
ConvexArea (int64) has range: 20684.00 - 263261.00, 0 nan values
Eccentricity (float64) has range: 0.22 - 0.91, 0 nan values
EquivDiameter (float64) has range: 161.24 - 569.37, 0 nan values
Extent (float64) has range: 0.56 - 0.87, 0 nan values
Id (int64) has range: 100000.00 - 113610.00, 0 nan values
MajorAxisLength (float64) has range: 183.60 - 738.86, 0 nan values
MinorAxisLength (float64) has range: 122.51 - 460.20, 0 nan values
Perimeter (float64) has range: 524.74 - 1985.37, 0 nan values
ShapeFactor1 (float64) has range: 0.00 - 0.01, 0 nan values
ShapeFactor2 (float64) has range: 0.00 - 0.00, 0 nan values
ShapeFactor3 (float64) has range: 0.41 - 0.97, 0 nan values
ShapeFactor4 (float64) has range: 0.95 - 1.00, 0 nan values
Solidity (float64) has range: 0.92 - 0.99, 0 nan values
roundness (float64) has range: 0.49 - 0.99, 0 nan values
