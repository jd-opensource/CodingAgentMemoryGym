# OpenMLE-fast task

Task ID: `arms-imports-per-country@1`

Native metric: `ArmsImportsRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2974 bytes)
- `data/sample_submission.csv` (5771 bytes); columns: ["id", "imports"]
- `data/test.csv` (11161 bytes); columns: ["id", "entity", "year"]
- `data/train.csv` (168486 bytes); columns: ["id", "entity", "year", "imports"]

## Public description

# Arms-Imports Forecasting Challenge (2016–2020)

Problem statement
Participants are given annual arms-import values (SIPRI-derived, in millions) for a global panel of countries/regions/groups from 1950–2015. The task is to forecast imports for 2016–2020. The target is highly skewed, sparse, and spike-prone, requiring robust time-series modeling and cross-entity generalization.

Files provided
- train.csv: id, entity, year, imports
- test.csv: id, entity, year
- sample_submission.csv: id, imports

Task details
- Input: Historical imports per entity-year up to 2015. Zeros represent deliveries valued <0.5m; NaN in the original data means “too minimal” or unreported.
- Predict: For each row in test.csv (entity-year pairs in 2016–2020 with official values), output a non-negative numeric forecast in a CSV named submission.csv with columns: id, imports.
- Constraints: Use features derived from the provided files (e.g., lags, rolling stats, growth rates, entity-level aggregates, pooling across entities, global models). External data is not required.

Evaluation
- Metric: Root Mean Squared Log Error (RMSLE) on the entity-year pairs listed in test.csv (log1p applied). Lower is better. Zeros are valid; negative predictions are invalid.
- Submission format: CSV with columns exactly [id, imports], ids must match test.csv. Imports must be finite and non-negative.

Data notes and modeling tips
- The panel exhibits heavy right skew and intermittent large spikes. RMSLE emphasizes order-of-magnitude correctness and handles zeros via log1p.
- The dataset has missingness; only non-null 2016–2020 values are evaluated and appear in test.csv. You may train with all non-null years up to 2015.
- Consider global ML forecasters (e.g., gradient boosting or sequence models over engineered lag features), hierarchical shrinkage across entities, and spike-aware strategies (e.g., mixture models, zero-inflated modeling, quantile losses, or separate spike classifiers).
- Useful features: recent lags (1–5 years), rolling means/medians, rolling std, year-over-year growth, decade indicators, entity historical quantiles, lifespan since first non-null observation, proportion of zeros, and cross-sectional aggregates.

Final dataset definitions
- Training set: All rows with year ≤ 2015 and non-null labels.
- Test set: Entity-year pairs within 2016–2020 that have official non-null values.

Reproducible preparation
- The included prepare.py script deterministically generates train.csv, test.csv, and sample_submission.csv from the raw source.
- Do not include paths in any CSV files.

Baseline ideas
- Naive last-observation-carried-forward per entity with fallbacks to rolling medians.
- Global gradient boosting with entity identifiers and lagged features.
- Simple ETS/ARIMA per-entity where coverage permits and blend with cross-entity regressors.

Rules
- Keep predictions non-negative and finite.
- Ensure submission ids exactly match test.csv.
