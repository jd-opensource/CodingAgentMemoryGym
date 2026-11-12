# OpenMLE-fast task

Task ID: `packagingsuggestion@1`

Native metric: `EcoPackagingRecommendationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1667 bytes)
- `data/sample_submission.csv` (15420 bytes); columns: ["row_id", "Packaging_Option"]
- `data/test.csv` (28177 bytes); columns: ["row_id", "Material_Type", "Product_Weight_g", "Fragility", "Recyclable", "Transport_Mode", "LCA_Emission_kgCO2"]
- `data/train.csv` (147836 bytes); columns: ["Material_Type", "Product_Weight_g", "Fragility", "Recyclable", "Transport_Mode", "LCA_Emission_kgCO2", "Packaging_Option"]

## Public description

```
description.txt (34 lines)
sample_submission.csv (802 lines)
test.csv (802 lines)
train.csv (3200 lines)```

-> sample_submission.csv has 801 rows and 2 columns.
Here is some information about the columns:
Packaging_Option (object) has 6 unique values: ['Mushroom Foam', 'Paper Wrap', 'Minimalist Pouch', 'Cornstarch Wrap', 'Recycled Cardboard', 'Bio Bubble Wrap']
row_id (int64) has range: 0.00 - 800.00, 0 nan values

-> test.csv has 801 rows and 7 columns.
Here is some information about the columns:
Fragility (object) has 3 unique values: ['Medium', 'Low', 'High']
LCA_Emission_kgCO2 (float64) has range: 0.08 - 4.17, 0 nan values
Material_Type (object) has 6 unique values: ['Plastic', 'Metal', 'Ceramic', 'Paper', 'Bioplastic', 'Glass']
Product_Weight_g (int64) has range: 100.00 - 1998.00, 0 nan values
Recyclable (object) has 2 unique values: ['Yes', 'No']
Transport_Mode (object) has 3 unique values: ['Air', 'Land', 'Sea']
row_id (int64) has range: 0.00 - 800.00, 0 nan values

-> train.csv has 3199 rows and 7 columns.
Here is some information about the columns:
Fragility (object) has 3 unique values: ['Medium', 'High', 'Low']
LCA_Emission_kgCO2 (float64) has range: 0.07 - 4.20, 0 nan values
Material_Type (object) has 6 unique values: ['Bioplastic', 'Ceramic', 'Glass', 'Paper', 'Plastic', 'Metal']
Packaging_Option (object) has 6 unique values: ['Paper Wrap', 'Bio Bubble Wrap', 'Recycled Cardboard', 'Cornstarch Wrap', 'Minimalist Pouch', 'Mushroom Foam']
Product_Weight_g (int64) has range: 100.00 - 2000.00, 0 nan values
Recyclable (object) has 2 unique values: ['Yes', 'No']
Transport_Mode (object) has 3 unique values: ['Sea', 'Air', 'Land']
