# OpenMLE-fast task

Task ID: `goibibo-flight-data@1`

Native metric: `FlightFareRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (485 bytes)
- `data/sample_submission.csv` (839865 bytes); columns: ["row_id", "price"]
- `data/test.csv` (5372400 bytes); columns: ["row_id", "flight date", "airline", "flight_num", "class", "from", "dep_time", "to", "arr_time", "duration", "stops"]
- `data/train.csv` (20062599 bytes); columns: ["flight date", "airline", "flight_num", "class", "from", "dep_time", "to", "arr_time", "duration", "stops", "price"]

## Public description

Flight Fare Prediction (India Domestic, 2023)

Files
- train.csv: Labeled training data with features and the target column price.
- test.csv: Unlabeled test data with the same features as train and an extra row_id column.
- sample_submission.csv: Example submission file with columns row_id and price.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on price; lower is better.
- Submissions must contain exactly the columns row_id and price for each row in test.csv.
