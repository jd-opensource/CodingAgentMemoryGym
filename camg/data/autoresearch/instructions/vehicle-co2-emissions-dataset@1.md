# OpenMLE-fast task

Task ID: `vehicle-co2-emissions-dataset@1`

Native metric: `VehicleCO2EmissionsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (896 bytes)
- `data/sample_submission.csv` (13075 bytes); columns: ["id", "CO2 Emissions(g/km)"]
- `data/test.csv` (92500 bytes); columns: ["id", "Make", "Model", "Vehicle Class", "Engine Size(L)", "Cylinders", "Transmission", "Fuel Type", "Fuel Consumption City (L/100 km)", "Fuel Consumption Hwy (L/100 km)", "Fuel Consumption Comb (L/100 km)"]
- `data/train.csv` (394185 bytes); columns: ["id", "Make", "Model", "Vehicle Class", "Engine Size(L)", "Cylinders", "Transmission", "Fuel Type", "Fuel Consumption City (L/100 km)", "Fuel Consumption Hwy (L/100 km)", "Fuel Consumption Comb (L/100 km)", "CO2 Emissions(g/km)"]

## Public description

Title: Vehicle CO2 Emissions — Full-Scale Tabular Regression Challenge

Problem
Predict a vehicle’s CO2 emissions (g/km) from its specifications and measured fuel consumption.

Files
- train.csv — Training features plus target.
- test.csv — Test features only.
- sample_submission.csv — Example submission with valid numeric predictions.

Columns
- id — Unique identifier aligning rows across files.
- Make, Model, Vehicle Class, Engine Size(L), Cylinders, Transmission, Fuel Type.
- Fuel Consumption City (L/100 km), Fuel Consumption Hwy (L/100 km), Fuel Consumption Comb (L/100 km).
- CO2 Emissions(g/km) — Target available only in train.csv.

Submission
CSV with columns in order: id, CO2 Emissions(g/km). Id values must match test.csv exactly; predictions must be numeric and finite.

Evaluation
Root Mean Squared Error (RMSE) on CO2 Emissions(g/km), after aligning rows by id.
