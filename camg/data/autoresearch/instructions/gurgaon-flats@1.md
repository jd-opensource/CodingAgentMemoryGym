# OpenMLE-fast task

Task ID: `gurgaon-flats@1`

Native metric: `GurgaonFlatPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (686 bytes)
- `data/sample_submission.csv` (14053 bytes); columns: ["id", "price_inr"]
- `data/test.csv` (572299 bytes); columns: ["id", "society", "area_sqft", "bedRoom", "bathroom", "balcony", "has_study", "has_servant", "has_store", "address", "floor_current", "floor_total", "facing", "agePossession", "nearbyLocations", "furnishDetails", "features", "rating_env", "rating_safety", "rating_lifestyle", "rating_connectivity", "rating_mean"]
- `data/train.csv` (2219580 bytes); columns: ["id", "society", "area_sqft", "bedRoom", "bathroom", "balcony", "has_study", "has_servant", "has_store", "address", "floor_current", "floor_total", "facing", "agePossession", "nearbyLocations", "furnishDetails", "features", "rating_env", "rating_safety", "rating_lifestyle", "rating_connectivity", "rating_mean", "price_inr"]

## Public description

```
description.txt (68 lines)
sample_submission.csv (609 lines)
test.csv (609 lines)
train.csv (2389 lines)```

-> sample_submission.csv has 608 rows and 2 columns.
The columns are: id, price_inr

-> test.csv has 608 rows and 22 columns.
The columns are: id, society, area_sqft, bedRoom, bathroom, balcony, has_study, has_servant, has_store, address, floor_current, floor_total, facing, agePossession, nearbyLocations... and 7 more columns

-> train.csv has 2388 rows and 23 columns.
The columns are: id, society, area_sqft, bedRoom, bathroom, balcony, has_study, has_servant, has_store, address, floor_current, floor_total, facing, agePossession, nearbyLocations... and 8 more columns
