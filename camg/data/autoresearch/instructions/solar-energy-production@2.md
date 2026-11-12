# OpenMLE-fast task

Task ID: `solar-energy-production@2`

Native metric: `SolarEnergyImputationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3641 bytes)
- `data/sample_submission.csv` (1739248 bytes); columns: ["site_id", "timestamp", "kWh"]
- `data/test.csv` (2664056 bytes); columns: ["site_id", "site_name", "timestamp", "installation_date"]
- `data/train.csv` (16512100 bytes); columns: ["site_id", "site_name", "timestamp", "installation_date", "kWh"]

## Public description

Title: Solar PV Hourly Imputation under Irregular Sampling (Cross-site)

Problem statement
City-operated solar PV sites report hourly energy production, but logs are irregular and contain gaps. Your goal is to build a global imputation model that predicts withheld hourly kWh values at specified site–timestamp pairs. The challenge stresses: (1) learning strong diurnal and seasonal structure, (2) handling both isolated and contiguous missing blocks (simulated outages), and (3) leveraging cross-site similarities without letting large-capacity sites dominate.

Files provided
- train.csv: Observed rows for training with the target kWh provided.
- test.csv: Rows where kWh is withheld; these are the rows to predict.
- sample_submission.csv: Example valid submission containing plausible numeric predictions.

Data description
Each row is an hourly energy reading for a site and time. Columns:
- site_id: Integer identifier for the PV site.
- site_name: Human-readable site name.
- timestamp: Local timestamp for the clock hour (timezone-naive; consistent formatting across files). Duplicate readings within the same clock hour are aggregated prior to the split.
- installation_date: Date the site was commissioned.
- kWh: Hourly energy production in kilowatt-hours. Present only in train.csv.

Scope and notes
- Multiple years and multiple sites with heterogeneous capacities are included.
- Sampling is irregular; hours without readings remain missing and may appear in test.csv.
- Address and external/public URL fields are not included to avoid leakage and noise; focus on time features and cross-site modeling.

What to predict
- Predict kWh for every row in test.csv.
- Your submission must contain exactly the same (site_id, timestamp) pairs as test.csv and the columns: site_id, timestamp, kWh.

Evaluation
A site-normalized Mean Absolute Error (nMAE) averaged equally across sites:
1) For each site s, compute Cs = 95th percentile of kWh using that site’s rows in train.csv.
2) For each test row i in site s, compute ei = |y_i − yhat_i| / max(Cs, 1e-6).
3) Average ei over rows within each site.
4) The final score is the mean of the site-level averages (lower is better).
Rationale: Normalizing by a robust per-site capacity measure prevents large sites from dominating, is robust to night-time near-zeros, and keeps the metric interpretable.

Train/test split summary (pre-prepared)
- Approximately 15% of observed hours per site are masked for testing.
- The masking is stratified by hour-of-day and month to represent daylight and shoulder hours, avoiding over-representing night-time zeros.
- The test set combines isolated hours and contiguous blocks (2–24 hours) to emulate realistic outages.
- There is no overlap: each (site_id, timestamp) appears in exactly one of train.csv or test.csv.

Submission format
- CSV with columns: site_id, timestamp, kWh.
- The set of (site_id, timestamp) keys must exactly match test.csv; one row per key; kWh must be numeric and finite.

Modeling guidance (optional)
- Useful features: hour-of-day, day-of-year, month, weekday/weekend, site age since installation, rolling/lagged statistics, and per-site scaling.
- Strong classical baselines: per-site/hour medians or gradient-boosted trees on engineered calendar features.
- Advanced: state-space models, matrix completion, or global deep time-series models (RNN/Transformer) with masking. Consider DST transitions, seasonality, weather variability, and capacity heterogeneity.

Deliverable
- submission.csv containing predictions for all rows in test.csv. The leaderboard uses the nMAE metric described above; lower is better.
