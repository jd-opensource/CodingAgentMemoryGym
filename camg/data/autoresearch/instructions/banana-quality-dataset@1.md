# OpenMLE-fast task

Task ID: `banana-quality-dataset@1`

Native metric: `BananaSweetnessMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2461 bytes)
- `data/sample_submission.csv` (4540 bytes); columns: ["sample_id", "sugar_content_brix"]
- `data/test.csv` (15838 bytes); columns: ["sample_id", "variety", "region", "ripeness_index", "firmness_kgf", "length_cm", "weight_g", "harvest_date", "tree_age_years", "altitude_m", "rainfall_mm", "soil_nitrogen_ppm"]
- `data/train.csv` (67551 bytes); columns: ["sample_id", "variety", "region", "ripeness_index", "sugar_content_brix", "firmness_kgf", "length_cm", "weight_g", "harvest_date", "tree_age_years", "altitude_m", "rainfall_mm", "soil_nitrogen_ppm"]

## Public description

```
description.txt (53 lines)
sample_submission.csv (201 lines)
test.csv (201 lines)
train.csv (801 lines)```

-> sample_submission.csv has 200 rows and 2 columns.
Here is some information about the columns:
sample_id (int64) has range: 8.00 - 998.00, 0 nan values
sugar_content_brix (float64) has range: 15.04 - 21.89, 0 nan values

-> test.csv has 200 rows and 12 columns.
Here is some information about the columns:
altitude_m (float64) has range: 0.40 - 1496.10, 0 nan values
firmness_kgf (float64) has range: 0.51 - 4.98, 0 nan values
harvest_date (object) has 13 unique values. Some example values: ['2023-10-30', '2023-10-27', '2023-10-29', '2023-10-25']
length_cm (float64) has range: 10.00 - 29.85, 0 nan values
rainfall_mm (float64) has range: 1000.50 - 2992.00, 0 nan values
region (object) has 8 unique values: ['Philippines', 'India', 'Ecuador', 'Costa Rica', 'Honduras', 'Guatemala', 'Brazil', 'Colombia']
ripeness_index (float64) has range: 1.05 - 6.98, 0 nan values
sample_id (int64) has range: 8.00 - 998.00, 0 nan values
soil_nitrogen_ppm (float64) has range: 10.20 - 199.70, 0 nan values
tree_age_years (float64) has range: 2.10 - 19.90, 0 nan values
variety (object) has 8 unique values: ['Manzano', 'Burro', 'Plantain', 'Cavendish', 'Blue Java', 'Fehi', 'Lady Finger', 'Red Dacca']
weight_g (float64) has range: 82.04 - 247.65, 0 nan values

-> train.csv has 800 rows and 13 columns.
Here is some information about the columns:
altitude_m (float64) has range: 0.60 - 1498.40, 0 nan values
firmness_kgf (float64) has range: 0.50 - 5.00, 0 nan values
harvest_date (object) has 49 unique values. Some example values: ['2023-09-25', '2023-09-30', '2023-09-27', '2023-09-04']
length_cm (float64) has range: 10.00 - 29.95, 0 nan values
rainfall_mm (float64) has range: 1000.80 - 2991.60, 0 nan values
region (object) has 8 unique values: ['Costa Rica', 'Colombia', 'Philippines', 'Guatemala', 'Brazil', 'India', 'Honduras', 'Ecuador']
ripeness_index (float64) has range: 1.02 - 7.00, 0 nan values
sample_id (int64) has range: 1.00 - 1000.00, 0 nan values
soil_nitrogen_ppm (float64) has range: 10.00 - 199.90, 0 nan values
sugar_content_brix (float64) has range: 15.00 - 21.98, 0 nan values
tree_age_years (float64) has range: 2.00 - 20.00, 0 nan values
variety (object) has 8 unique values: ['Manzano', 'Plantain', 'Fehi', 'Cavendish', 'Burro', 'Red Dacca', 'Lady Finger', 'Blue Java']
weight_g (float64) has range: 81.05 - 249.89, 0 nan values
