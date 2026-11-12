# OpenMLE-fast task

Task ID: `world-air-quality-data-2024-updated@1`

Native metric: `AirQualityNowcastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (579 bytes)
- `data/sample_submission.csv` (4700 bytes); columns: ["id", "pm25"]
- `data/test.csv` (18228 bytes); columns: ["id", "bc", "co", "no", "no2", "nox", "o3", "pm1", "pm10", "so2", "lat", "lon", "month", "dayofweek", "hour", "country_code", "country_label", "source_name", "Location"]
- `data/train.csv` (359695 bytes); columns: ["id", "bc", "co", "no", "no2", "nox", "o3", "pm1", "pm10", "so2", "lat", "lon", "month", "dayofweek", "hour", "country_code", "country_label", "source_name", "Location", "pm25"]

## Public description

Competition: PM2.5 Nowcasting from Multi-Pollutant and Spatiotemporal Context

Files provided
- train.csv: Feature table with the target column pm25.
- test.csv: Feature table without the target (pm25 is withheld).
- sample_submission.csv: A sample submission file showing the expected format.

Submission format
- A CSV file with exactly two columns in this order: id, pm25
- id: The identifier provided in test.csv.
- pm25: Predicted PM2.5 concentration in µg/m³.

Evaluation
- Root Mean Squared Error (RMSE) between predictions and ground truth pm25 on the hidden test set.
