# OpenMLE-fast task

Task ID: `weather-data@1_duplicate_1`

Native metric: `WeatherForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (96 bytes)
- `data/sample_submission.csv` (1472258 bytes); columns: ["row_id", "Temperature_C_1h", "Humidity_pct_1h", "Precipitation_mm_1h", "Wind_Speed_kmh_1h", "Temperature_C_3h", "Humidity_pct_3h", "Precipitation_mm_3h", "Wind_Speed_kmh_3h", "Temperature_C_6h", "Humidity_pct_6h", "Precipitation_mm_6h", "Wind_Speed_kmh_6h"]
- `data/test.csv` (714930 bytes); columns: ["row_id", "Location", "Date_Time", "Temperature_C", "Humidity_pct", "Precipitation_mm", "Wind_Speed_kmh"]
- `data/train.csv` (8564891 bytes); columns: ["Location", "Date_Time", "Temperature_C", "Humidity_pct", "Precipitation_mm", "Wind_Speed_kmh", "Temperature_C_1h", "Humidity_pct_1h", "Precipitation_mm_1h", "Wind_Speed_kmh_1h", "Temperature_C_3h", "Humidity_pct_3h", "Precipitation_mm_3h", "Wind_Speed_kmh_3h", "Temperature_C_6h", "Humidity_pct_6h", "Precipitation_mm_6h", "Wind_Speed_kmh_6h"]

## Public description

Files in this competition (relative to public/):
- train.csv
- test.csv
- sample_submission.csv
