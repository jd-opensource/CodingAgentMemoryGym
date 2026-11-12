# OpenMLE-fast task

Task ID: `ab-nyc-2019csv@1`

Native metric: `AirbnbPricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (585 bytes)
- `data/sample_submission.csv` (268741 bytes); columns: ["id", "price"]
- `data/test.csv` (1400069 bytes); columns: ["id", "name", "host_id", "host_name", "neighbourhood_group", "neighbourhood", "latitude", "longitude", "room_type", "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365"]
- `data/train.csv` (5640842 bytes); columns: ["id", "name", "host_id", "host_name", "neighbourhood_group", "neighbourhood", "latitude", "longitude", "room_type", "price", "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365"]

## Public description

NYC Airbnb Nightly Price Prediction

Public files and structure (paths are relative to the public/ directory):
- train.csv: Training data with features and the target column 'price'.
- test.csv: Test data with the same features as train.csv but without the 'price' column.
- sample_submission.csv: Example submission file with two columns ['id', 'price']; 'id' matches test.csv and 'price' contains placeholder values.

Notes:
- The objective is to predict the 'price' for each listing in test.csv.
- Evaluation uses RMSLE computed between your submission and the hidden ground truth.
