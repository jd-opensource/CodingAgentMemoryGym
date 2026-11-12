# OpenMLE-fast task

Task ID: `usedcarprices@1`

Native metric: `UsedCarPriceForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (660 bytes)
- `data/sample_submission.csv` (14457 bytes); columns: ["Id", "Price"]
- `data/test.csv` (127014 bytes); columns: ["Id", "Name", "Location", "Year", "Kilometers_Driven", "Fuel_Type", "Transmission", "Owner_Type", "Mileage", "Engine", "Power", "Seats"]
- `data/train.csv` (529402 bytes); columns: ["Id", "Name", "Location", "Year", "Kilometers_Driven", "Fuel_Type", "Transmission", "Owner_Type", "Mileage", "Engine", "Power", "Seats", "Price"]

## Public description

Competition: Used Car Price Forecast (India)

Problem statement:
Estimate the fair resale price (in INR Lakhs) of used cars across Indian cities from listing attributes.

Data description:
- Task type: Tabular regression.
- Target: Price (in INR Lakhs).
- Files:
  - train.csv: labeled training data.
  - test.csv: unlabeled test data.
  - sample_submission.csv: example submission with valid format (Id, Price).

Submission format:
- CSV file with exactly two columns: Id, Price.
- Id must match the Id values in test.csv.
- Price must be non-negative finite numbers (in INR Lakhs).

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) on Price.
