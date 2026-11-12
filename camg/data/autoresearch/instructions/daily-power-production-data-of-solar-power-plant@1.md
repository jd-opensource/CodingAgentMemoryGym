# OpenMLE-fast task

Task ID: `daily-power-production-data-of-solar-power-plant@1`

Native metric: `SolarPVSMAPEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2874 bytes)
- `data/sample_submission.csv` (2042206 bytes); columns: ["uid", "kWh"]
- `data/test.csv` (6569367 bytes); columns: ["uid", "site_id", "timestamp", "site_name", "site_address", "installation_date"]
- `data/train.csv` (27802165 bytes); columns: ["uid", "site_id", "timestamp", "kWh", "site_name", "site_address", "installation_date"]

## Public description

Competition: Multi-site Hourly Solar PV Forecasting (Calgary Municipal Sites)

Problem statement
- Given historical hourly energy production (kWh) for multiple municipal solar PV sites, forecast the hourly energy production for each site over a future holdout period.
- This is a multi-site time-series forecasting task. Build models that generalize across sites and seasons using only the provided files.

Data
- Multi-year production records per site with timestamps and site metadata. Only top-of-hour rows are included; a small number of extreme outliers in kWh were removed to improve label quality.
- Files provided:
  1) train.csv — historical data including the target.
  2) test.csv — future-period rows without the target (your prediction targets).
  3) sample_submission.csv — example submission with random but valid predictions.

Columns
- uid: Unique identifier for the row (site_id + timestamp). This is the key you must predict for.
- site_id: Numeric identifier of the site.
- timestamp: Local timestamp string (format YYYY-MM-DD HH:MM:SS). All rows are aligned to top-of-hour.
- kWh: Target column (only in train.csv). Hourly energy production in kWh.
- site_name: Name of the site (static metadata).
- site_address: Address of the site (static metadata).
- installation_date: Date the site was installed (static metadata).

Task
- Predict kWh for every row in test.csv and submit a file with two columns: uid,kWh.

Split
- Chronological split shared across all sites:
  - Training: up to and including 2023-09-30 23:59:59.
  - Test: 2023-10-01 00:00:00 through 2024-02-15 23:59:59.
- Only sites present in training appear in test. There is no overlap in rows between train and test.

Evaluation
- Submissions are evaluated with site-averaged sMAPE (symmetric Mean Absolute Percentage Error) with epsilon for numerical stability.
- For each row, sMAPE = |y - y_hat| / max(eps, (|y| + |y_hat|)/2), with eps = 1e-3.
- For each site, compute the mean sMAPE over its test rows; then take the simple average across all sites (equal weight per site).
- Lower is better.

Rules and notes
- Use only the provided files; external data or manual labels are not allowed.
- You may engineer features such as hour-of-day, day-of-week, day-of-year, month, holidays (derived from the timestamp), site age (timestamp − installation_date), and interactions.
- Timestamps are in the local calendar for the sites. No timezone conversion is required.
- Nighttime hours can be near zero; the epsilon in sMAPE ensures numerical stability near dawn/dusk.

Submission format
- A CSV with two columns, exactly and in order: uid,kWh
- The set of uid values must match test.csv exactly (one prediction per uid, no duplicates, no missing rows).
- kWh must be numeric and finite. Lower sMAPE is better.

Files in this competition
- train.csv
- test.csv
- sample_submission.csv
