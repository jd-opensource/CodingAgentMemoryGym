# OpenMLE-fast task

Task ID: `california-wildfire-incidents-20132020@1`

Native metric: `CaliforniaWildfireRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3356 bytes)
- `data/sample_submission.csv` (6021 bytes); columns: ["Id", "AcresBurned"]
- `data/test.csv` (44298 bytes); columns: ["Id", "Started", "Latitude", "Longitude", "Counties", "CountyIds", "AdminUnit", "CalFireIncident", "ArchiveYear", "Name", "Location", "FuelType"]
- `data/train.csv` (230998 bytes); columns: ["Id", "Started", "Latitude", "Longitude", "Counties", "CountyIds", "AdminUnit", "CalFireIncident", "ArchiveYear", "Name", "Location", "FuelType", "AcresBurned"]

## Public description

California Wildfire Final Acreage Prediction (2013–2020)

Overview
California experiences frequent and destructive wildfires. Rapidly estimating the eventual size of an incident helps guide resource allocation and risk communication. In this competition, you will predict the final acres burned for each wildfire incident using information available at or near ignition.

Task
Given tabular incident metadata available at start time (date/time, location, jurisdiction, and short descriptions), build a model to predict the final AcresBurned for each incident.

Files
- train.csv: Training set with features and the target column AcresBurned.
- test.csv: Test set with the same feature columns as train.csv (without AcresBurned).
- sample_submission.csv: A sample submission file in the correct format.

Target
- AcresBurned (non-negative real number): the final area burned for the incident.

Features
The provided features are limited to fields that are plausibly known at or near ignition to avoid outcome leakage. Examples include:
- Started: timestamp when the incident started (string ISO-like format). Useful for deriving year, month, day-of-week, hour bins, seasonality, etc.
- Latitude, Longitude: location coordinates (use for spatial encodings or coarse grids).
- Counties, CountyIds: one or more counties associated with the incident (strings; you may multi-hot encode or parse as needed).
- AdminUnit: responsible agency/unit (categorical).
- CalFireIncident: whether the incident is a CAL FIRE incident (boolean/categorical).
- ArchiveYear: reporting year value (numeric/categorical).
- Name, Location: short text fields that often reference local geography, highways, landmarks.
- FuelType: when available (categorical).
Note: Some fields may be missing for some incidents. You are free to engineer features from these columns. Fields reflecting mid/late-incident outcomes and resource allocations have been removed to prevent leakage.

Split
- The split is chronological to respect temporal drift: training incidents occur in 2013–2018; test incidents occur in 2019–2020. Use only the provided files; do not assume access to the original raw data.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on AcresBurned.
- Definition: score = sqrt(mean((log1p(y_pred) − log1p(y_true))^2)).
- Requirements: Your submission must be a CSV with columns:
  - Id: identifier for each test row.
  - AcresBurned: your predicted non-negative value for that Id.
- The set of Id values in your submission must exactly match the Id values in test.csv.

Recommendations
- Handle heavy-tailed targets using log1p transforms, robust models, and appropriate loss functions.
- Engineer temporal features (year, month, day-of-week, season, hour), geospatial features (coarse bins/geohash), and simple text features from Name and Location (e.g., TF-IDF with regularization).
- Expect non-stationarity between train and test (policy, climate); prefer time-aware validation.
- Manage missingness carefully.

Rules and Notes
- External data use is allowed as long as it is publicly available to all participants and does not leak target information for the test period.
- Do not attempt to reverse-engineer withheld labels or use outcome-based fields; only the provided features should be used.

Good luck, and we look forward to your solutions!
