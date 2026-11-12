# OpenMLE-fast task

Task ID: `fastfood-nutrition@2`

Native metric: `FastFoodSatFatMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2400 bytes)
- `data/sample_submission.csv` (581 bytes); columns: ["id", "high_satfat"]
- `data/test.csv` (5777 bytes); columns: ["restaurant", "calories", "cal_fat", "total_fat", "trans_fat", "cholesterol", "sodium", "total_carb", "fiber", "sugar", "protein", "vit_a", "vit_c", "calcium", "id"]
- `data/train.csv` (25561 bytes); columns: ["restaurant", "calories", "cal_fat", "total_fat", "trans_fat", "cholesterol", "sodium", "total_carb", "fiber", "sugar", "protein", "vit_a", "vit_c", "calcium", "high_satfat", "id"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (97 lines)
test.csv (97 lines)
train.csv (417 lines)```

-> sample_submission.csv has 96 rows and 2 columns.
Here is some information about the columns:
high_satfat (int64) has 2 unique values: [1, 0]
id (int64) has range: 45.00 - 511.00, 0 nan values

-> test.csv has 96 rows and 15 columns.
Here is some information about the columns:
cal_fat (int64) has range: 20.00 - 1270.00, 0 nan values
calcium (float64) has range: 0.00 - 80.00, 40 nan values
calories (int64) has range: 70.00 - 2430.00, 0 nan values
cholesterol (int64) has range: 0.00 - 475.00, 0 nan values
fiber (float64) has range: 0.00 - 14.00, 2 nan values
id (int64) has range: 45.00 - 511.00, 0 nan values
protein (float64) has range: 5.00 - 186.00, 1 nan values
restaurant (object) has 8 unique values: ['Arbys', 'Burger King', 'Chick Fil-A', 'Dairy Queen', 'Mcdonalds', 'Sonic', 'Subway', 'Taco Bell']
sodium (int64) has range: 100.00 - 6080.00, 0 nan values
sugar (int64) has range: 0.00 - 18.00, 0 nan values
total_carb (int64) has range: 2.00 - 121.00, 0 nan values
total_fat (int64) has range: 2.00 - 141.00, 0 nan values
trans_fat (float64) has 7 unique values: [0.0, 0.5, 2.0, 1.0, 3.0, 1.5, 4.0]
vit_a (float64) has range: 0.00 - 180.00, 41 nan values
vit_c (float64) has range: 0.00 - 200.00, 40 nan values

-> train.csv has 416 rows and 16 columns.
Here is some information about the columns:
cal_fat (int64) has range: 0.00 - 1134.00, 0 nan values
calcium (float64) has range: 0.00 - 290.00, 168 nan values
calories (int64) has range: 20.00 - 1770.00, 0 nan values
cholesterol (int64) has range: 0.00 - 805.00, 0 nan values
fiber (float64) has range: 0.00 - 17.00, 10 nan values
high_satfat (int64) has 2 unique values: [0, 1]
id (int64) has range: 0.00 - 490.00, 0 nan values
protein (float64) has range: 1.00 - 134.00, 0 nan values
restaurant (object) has 8 unique values: ['Arbys', 'Burger King', 'Chick Fil-A', 'Dairy Queen', 'Mcdonalds', 'Sonic', 'Subway', 'Taco Bell']
sodium (int64) has range: 15.00 - 4520.00, 0 nan values
sugar (int64) has range: 0.00 - 87.00, 0 nan values
total_carb (int64) has range: 0.00 - 156.00, 0 nan values
total_fat (int64) has range: 0.00 - 126.00, 0 nan values
trans_fat (float64) has range: 0.00 - 8.00, 0 nan values
vit_a (float64) has range: 0.00 - 180.00, 171 nan values
vit_c (float64) has range: 0.00 - 400.00, 168 nan values
