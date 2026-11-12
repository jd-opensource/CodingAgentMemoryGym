# OpenMLE-fast task

Task ID: `countries-gdp-19602020@1`

Native metric: `GDPForecastRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3462 bytes)
- `data/sample_submission.csv` (11856 bytes); columns: ["row_id", "y"]
- `data/test.csv` (53014 bytes); columns: ["row_id", "country_code", "target_year", "gdp_t-4", "gdp_t-3", "gdp_t-2", "gdp_t-1", "gdp_t"]
- `data/train.csv` (599718 bytes); columns: ["row_id", "country_code", "target_year", "gdp_t-4", "gdp_t-3", "gdp_t-2", "gdp_t-1", "gdp_t", "y"]

## Public description

Global GDP Next-Year Forecasting (1960–2020)

Problem statement
Participants must build machine learning models that forecast next-year nominal GDP (current USD) for each country-year in 2016–2020 using only its historical GDP trajectory. This is a panel time-series forecasting challenge with non-stationarity, heterogeneous scales, structural breaks, and missingness. No external data are permitted; all features must be engineered from the provided historical GDP signals.

Files provided to participants
- train.csv: Supervised training samples with features and labels.
- test.csv: Test samples with features only.
- sample_submission.csv: Example submission file demonstrating required format.

Train/test structure
- Each row represents one country’s rolling window at year t with features from years t−4, t−3, t−2, t−1, t, and the target is GDP at year t+1.
- Train split: all windows whose target year is at most 2015.
- Test split: all windows whose target year is in 2016, 2017, 2018, 2019, or 2020.
- Only sovereign/territory ISO3 country codes are used; regional and income-group aggregates are excluded to prevent label leakage and double counting.
- All GDP values are non-negative and in current USD.

Column schema
- row_id: Unique integer identifier for the window. Train and test row_id ranges are disjoint.
- country_code: ISO 3166-1 alpha-3 country/territory code.
- target_year: Integer year of the prediction target (t+1).
- gdp_t-4, gdp_t-3, gdp_t-2, gdp_t-1, gdp_t: Numeric features (GDP in USD) for the five preceding years.
- y (train only): Ground-truth next-year GDP in USD.

Submission format
- A single CSV with exactly two columns, no header variations, and no extra columns: row_id,y
- row_id must match the IDs in test.csv.
- y must be a non-negative numeric prediction of next-year GDP in USD.

Evaluation metric
- Primary metric: RMSLE (root mean squared log error) computed over all test rows. Specifically: take log1p of predictions and ground truth, compute squared differences, average across all rows, then take the square root.
- Aggregation: Unweighted mean over test rows; each country-year pair contributes equally.
- Rationale: GDP spans orders of magnitude across countries. RMSLE evaluates multiplicative error, rewarding correct growth trajectories irrespective of absolute scale. Using log1p ensures numerical stability and supports zero values.

Modeling guidance (not mandatory)
- Strong baselines include growth-rate carry-forward, AR models on log-transformed GDP, gradient boosting on lagged log GDP and engineered growth features, and panel regressions with country effects.
- Recommended feature engineering: log1p transforms, year-over-year growth rates, multi-year compounded growth, rolling statistics, and regime-aware features. Ensure strictly causal features; do not use data from t+1 or later.
- Handle missing values by discarding windows that contain NA in any feature or target.

Rules and constraints
- No external datasets or manual labels are allowed.
- Do not attempt to infer test targets from aggregates; aggregates are excluded by design. Use only the provided train.csv and test.csv for modeling.

Goal
Deliver robust models that generalize across countries and decades, coping with scale heterogeneity, structural breaks (e.g., oil shocks, 2008 crisis, 2020 pandemic), and sparse early histories. The leaderboard rewards accurate, stable forecasts under the RMSLE metric.
