# OpenMLE-fast task

Task ID: `household-monthly-electricity-bill@1`

Native metric: `HouseholdElectricityBillMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2332 bytes)
- `data/sample_submission.csv` (4933 bytes); columns: ["id", "amount_paid"]
- `data/test.csv` (7340 bytes); columns: ["id", "num_rooms", "num_people", "housearea", "is_ac", "is_tv", "is_flat", "ave_monthly_income", "num_children", "is_urban"]
- `data/train.csv` (38524 bytes); columns: ["id", "num_rooms", "num_people", "housearea", "is_ac", "is_tv", "is_flat", "ave_monthly_income", "num_children", "is_urban", "amount_paid"]

## Public description

Title: Household Monthly Electricity Bill Prediction

Overview:
Predict the monthly electricity bill (amount_paid) for Indian households from tabular features describing household composition, dwelling characteristics, appliance ownership, urbanicity, and income. Build a robust ML model that generalizes across diverse households.

Files provided:
- train.csv: id + all features + target amount_paid
- test.csv: id + all features (no target)
- sample_submission.csv: id + amount_paid (example format with plausible values)

Schema:
- id: unique integer identifier
- Features:
  - num_rooms: Number of rooms (integer, >= 0)
  - num_people: Number of people in the household (integer, >= 0)
  - housearea: Area of the house (float, > 0)
  - is_ac: AC present? (binary 0/1)
  - is_tv: TV present? (binary 0/1)
  - is_flat: Dwelling is a flat? (binary 0/1)
  - ave_monthly_income: Average monthly household income (float, >= 0)
  - num_children: Number of children (integer, >= 0)
  - is_urban: Urban area? (binary 0/1)
- Target:
  - amount_paid: Monthly electricity bill (continuous)

Split details:
- Deterministic 80/20 split into train/test.
- Stratified across (is_ac, is_urban) to preserve coverage.
- IDs in test.csv match those in sample_submission.csv and are disjoint from train.csv.

Evaluation:
- Metric: Root Mean Squared Error (RMSE) on amount_paid.
  - RMSE penalizes large errors and is precise, reproducible, and standard for regression.
- Submission format:
  - CSV with exactly two columns: id, amount_paid.
  - Predict exactly one value per id in test.csv.
  - All predictions must be finite numeric values (no NaN/Inf).

Guidance and hints:
- Consider robust preprocessing and feature engineering:
  - Ratios: area_per_room, people_per_room, income_per_person (handle zero denominators safely).
  - Interactions: is_ac × is_urban, is_flat × housearea, num_children × is_tv.
  - Transformations: log scaling for skewed variables (e.g., income) and robust scaling.
- Zeros in counts can be valid (e.g., temporarily unoccupied household); handle such edge cases carefully.
- Expect nonlinearity and outliers; models like regularized linear models, tree ensembles, and well-regularized neural nets can perform well.

Goal:
Minimize RMSE on the test set by producing accurate predictions for amount_paid in test.csv.
