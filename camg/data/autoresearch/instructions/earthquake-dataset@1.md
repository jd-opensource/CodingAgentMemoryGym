# OpenMLE-fast task

Task ID: `earthquake-dataset@1`

Native metric: `EarthquakeMagnitudeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (615 bytes)
- `data/sample_submission.csv` (443734 bytes); columns: ["event_uid", "mag"]
- `data/test.csv` (1587053 bytes); columns: ["event_uid", "time", "latitude", "longitude", "depth", "magType", "nst", "gap", "dmin", "rms"]
- `data/train.csv` (8321177 bytes); columns: ["event_uid", "time", "latitude", "longitude", "depth", "magType", "nst", "gap", "dmin", "rms", "mag"]

## Public description

Competition: Global Earthquake Magnitude Prediction from Seismic Metadata

Problem statement
Participants must predict the reviewed earthquake magnitude using event-level metadata.

Data description
- Train data (train.csv): event_uid, features, and target mag.
- Test data (test.csv): same features as train.csv but without mag.
- Sample submission (sample_submission.csv): two columns [event_uid, mag].

Submission format
- CSV with exactly two columns: [event_uid, mag] covering all rows in test.csv.

Evaluation
- Mean Absolute Error (MAE). Lower is better.

Files
- train.csv
- test.csv
- sample_submission.csv
