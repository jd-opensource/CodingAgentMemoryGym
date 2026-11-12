# OpenMLE-fast task

Task ID: `calories-in-food-items-per-100-grams@1`

Native metric: `CaloriesPer100gMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (311 bytes)
- `data/sample_submission.csv` (8644 bytes); columns: ["Id", "Cals_per100grams"]
- `data/test.csv` (15664 bytes); columns: ["Id", "FoodCategory", "FoodItem"]
- `data/train.csv` (77641 bytes); columns: ["Id", "FoodCategory", "FoodItem", "Cals_per100grams"]

## Public description

This competition provides calorie information per 100 grams for various food items.
Your task is to predict the Cals_per100grams for each item in the test set.

Files:
- train.csv: Id, FoodCategory, FoodItem, Cals_per100grams
- test.csv: Id, FoodCategory, FoodItem
- sample_submission.csv: Id, Cals_per100grams
