# OpenMLE-fast task

Task ID: `global-airports-iata-icao-timezone-geo@2`

Native metric: `CountryLocatorMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (304 bytes)
- `data/sample_submission.csv` (10907 bytes); columns: ["Id", "country"]
- `data/test.csv` (29329 bytes); columns: ["Id", "lat", "lon"]
- `data/train.csv` (136975 bytes); columns: ["Id", "lat", "lon", "country"]

## Public description

Files in this directory:
- train.csv: [Id, lat, lon, country]
- test.csv: [Id, lat, lon]
- sample_submission.csv: [Id, country]

Task: Predict the ISO 3166-1 alpha-3 country code (country) for each Id in test.csv from its coordinates.

Evaluation: Macro-averaged F1 over classes present in the test set.
