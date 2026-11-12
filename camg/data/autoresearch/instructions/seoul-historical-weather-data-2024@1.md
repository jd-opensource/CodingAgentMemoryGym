# OpenMLE-fast task

Task ID: `seoul-historical-weather-data-2024@1`

Native metric: `SeoulWeatherForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (270 bytes)
- `data/sample_submission.csv` (296401 bytes); columns: ["date", "tempmax", "tempmin", "temp", "precip", "snow", "windspeed", "winddir", "sealevelpressure", "cloudcover", "visibility", "solarradiation", "uvindex", "humidity", "dew"]
- `data/test.csv` (114498 bytes); columns: ["date", "feelslikemax", "feelslikemin", "feelslike", "snowdepth", "windgust", "solarenergy", "severerisk", "moonphase", "doy_sin", "doy_cos", "day_length_hours"]
- `data/train.csv` (684746 bytes); columns: ["date", "feelslikemax", "feelslikemin", "feelslike", "snowdepth", "windgust", "solarenergy", "severerisk", "moonphase", "doy_sin", "doy_cos", "day_length_hours", "tempmax_next", "tempmin_next", "temp_next", "precip_next", "snow_next", "windspeed_next", "winddir_next", "sealevelpressure_next", "cloudcover_next", "visibility_next", "solarradiation_next", "uvindex_next", "humidity_next", "dew_next"]

## Public description

Files in this dataset:

- train.csv: Training data with features at time t and next-day target columns suffixed with _next.
- test.csv: Test data with features at time t (no target columns).
- sample_submission.csv: Example submission file with columns [date] + targets.
