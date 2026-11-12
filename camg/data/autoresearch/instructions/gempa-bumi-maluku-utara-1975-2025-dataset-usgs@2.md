# OpenMLE-fast task

Task ID: `gempa-bumi-maluku-utara-1975-2025-dataset-usgs@2`

Native metric: `EarthquakeWeekRiskMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3580 bytes)
- `data/sample_submission.csv` (55148 bytes); columns: ["date", "prob_event_next7d"]
- `data/test.csv` (1270622 bytes); columns: ["date", "count_all", "energy_sum", "count_Mge30d1", "count_Mge40d1", "count_Mge45d1", "count_Mge50d1", "gap_mean_d1", "dmin_mean_d1", "nst_mean_d1", "rms_mean_d1", "depthError_mean_d1", "count_Mge30_d3", "count_Mge30_d7", "count_Mge30_d14", "count_Mge30_d30", "count_Mge30_d90", "count_Mge30_d365", "count_Mge40_d3", "count_Mge40_d7", "count_Mge40_d14", "count_Mge40_d30", "count_Mge40_d90", "count_Mge40_d365", "count_Mge45_d3", "count_Mge45_d7", "count_Mge45_d14", "count_Mge45_d30", "count_Mge45_d90", "count_Mge45_d365", "count_Mge50_d3", "count_Mge50_d7", "count_Mge50_d14", "count_Mge50_d30", "count_Mge50_d90", "count_Mge50_d365", "energy_sum_d3", "energy_sum_d7", "energy_sum_d14", "energy_sum_d30", "energy_sum_d90", "energy_sum_d365", "gap_mean_d7", "gap_mean_d30", "dmin_mean_d7", "dmin_mean_d30", "nst_mean_d7", "nst_mean_d30", "rms_mean_d7", "rms_mean_d30", "depthError_mean_d7", "depthError_mean_d30", "doy_sin", "doy_cos", "month_sin", "month_cos"]
- `data/train.csv` (6153018 bytes); columns: ["date", "count_all", "energy_sum", "count_Mge30d1", "count_Mge40d1", "count_Mge45d1", "count_Mge50d1", "gap_mean_d1", "dmin_mean_d1", "nst_mean_d1", "rms_mean_d1", "depthError_mean_d1", "count_Mge30_d3", "count_Mge30_d7", "count_Mge30_d14", "count_Mge30_d30", "count_Mge30_d90", "count_Mge30_d365", "count_Mge40_d3", "count_Mge40_d7", "count_Mge40_d14", "count_Mge40_d30", "count_Mge40_d90", "count_Mge40_d365", "count_Mge45_d3", "count_Mge45_d7", "count_Mge45_d14", "count_Mge45_d30", "count_Mge45_d90", "count_Mge45_d365", "count_Mge50_d3", "count_Mge50_d7", "count_Mge50_d14", "count_Mge50_d30", "count_Mge50_d90", "count_Mge50_d365", "energy_sum_d3", "energy_sum_d7", "energy_sum_d14", "energy_sum_d30", "energy_sum_d90", "energy_sum_d365", "gap_mean_d7", "gap_mean_d30", "dmin_mean_d7", "dmin_mean_d30", "nst_mean_d7", "nst_mean_d30", "rms_mean_d7", "rms_mean_d30", "depthError_mean_d7", "depthError_mean_d30", "doy_sin", "doy_cos", "month_sin", "month_cos", "label"]

## Public description

Competition: North Maluku 7-Day M≥5 Occurrence Risk (Daily rolling forecast)

Problem statement
Predict, for each calendar day in the test period, the probability that at least one mb-scale earthquake with magnitude ≥ 5.0 will occur in the North Maluku region during the following 7 days (open interval (t, t+7]).

You are given a historical earthquake catalog covering North Maluku and nearby seas for 1975–2025. Participants must build a leakage-free, time-ordered modeling pipeline that converts past events up to each day t into features and predicts a calibrated probability of a qualifying event in the next week.

Files
- train.csv: Daily rows with engineered features and the target label. Use these to train your model.
- test.csv: Daily rows with the same engineered features and the date column but without the label. Make predictions for these dates.
- sample_submission.csv: Example of a valid submission format.

Target definition
A “qualifying event” is an earthquake that satisfies all of the following:
- Status: reviewed
- Magnitude type: mb
- Magnitude threshold: mag ≥ 5.0
- Location: epicenter within the regional bounding box [lat −3…3, lon 125…130]

For a given day t, the target y_t is 1 if at least one qualifying event occurs strictly after t and within 7 days (i.e., in (t, t+7]), otherwise 0.

Features
Each row in train.csv and test.csv represents a calendar date t and includes:
- Multi-scale activity: counts of earthquakes above magnitude thresholds (≥3.0, ≥4.0, ≥4.5, ≥5.0) aggregated over same-day and rolling windows (3, 7, 14, 30, 90, 365 days).
- Energy proxies: cumulative sums of 10^(1.5·mag) over rolling windows.
- Network/data quality: rolling means of gap, dmin, nst, rms, and depthError.
- Recency indicators: days since the most recent M≥5 and M≥5.5 events; distance (km) from the region center to the latest event location as of day t.
- Seasonality: day-of-year and month encodings (sin/cos).

Train/test split
- Chronological split with no overlap.
- Training period: from the beginning of coverage up to 2021-12-31.
- Test period: 2022-01-01 onward (until the data allows given a 7-day lookahead).

Submission format
- CSV with two columns: [date, prob_event_next7d]
- date must exactly match the dates in test.csv (one-to-one, same order or sorted order acceptable).
- prob_event_next7d is a probability in [0, 1].

Evaluation
- Primary metric: Binary cross-entropy (log loss) computed per test date between your submitted probability and the ground-truth label.
- Lower is better. Probabilities are clipped to [1e-15, 1-1e-15] to ensure numerical stability.

Rules and guidance
- Time-order integrity: Features for day t may only use events at or before t. The provided train/test files are engineered to be leakage-free; you may model directly on them.
- External data: Allowed, but must be publicly available and documented. Any external features must be aligned in time and cannot use future information.
- Class imbalance: Positives are sparse. Consider calibrated probabilistic models, Poisson/Hawkes/ETAS baselines, gradient boosting with rolling features, or sequence models (RNN/Temporal CNN) trained on the provided features.
- Reproducibility: Set seeds and document your pipeline. Deterministic behavior is recommended.

Notes
- Do not add paths inside CSVs. File names are sufficient.
- All columns in test.csv replicate those in train.csv except the label.
- The problem is designed to reward both discrimination and calibration. Reliability plots are encouraged for local validation.
