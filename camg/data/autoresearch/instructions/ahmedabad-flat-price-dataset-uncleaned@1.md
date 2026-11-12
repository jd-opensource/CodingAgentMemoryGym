# OpenMLE-fast task

Task ID: `ahmedabad-flat-price-dataset-uncleaned@1`

Native metric: `AhmedabadPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1097 bytes)
- `data/sample_submission.csv` (34665 bytes); columns: ["listing_id", "price"]
- `data/test.csv` (506772 bytes); columns: ["listing_id", "title", "type_area", "value_area", "status", "floor", "transaction", "furnishing", "facing", "description"]
- `data/train.csv` (2097797 bytes); columns: ["listing_id", "title", "type_area", "value_area", "status", "floor", "transaction", "furnishing", "facing", "description", "price"]

## Public description

Ahmedabad Flat Price Prediction Challenge

Problem statement
Participants are tasked with predicting the total listed price (INR) of residential flats in Ahmedabad, India using heterogeneous, real-world listing attributes. The data contains both structured fields (area, status, floor, transaction type, furnishing, facing) and unstructured text (title and description). The dataset is intentionally uncleaned to reflect real marketplace conditions.

Data description
- train.csv: Tabular data with listing_id, label column price (numeric INR), and features including title, type_area, value_area, status, floor, transaction, furnishing, facing, description.
- test.csv: Same feature columns as train.csv (excluding price). Contains listing_id for joining.
- sample_submission.csv: A file with listing_id and price columns. Participants should predict price in INR for each listing_id in test.csv.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on predicted vs true total price.

Deliverables
- A submission file named submission.csv (format identical to sample_submission.csv).
