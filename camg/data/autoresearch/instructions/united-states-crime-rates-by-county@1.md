# OpenMLE-fast task

Task ID: `united-states-crime-rates-by-county@1`

Native metric: `CountyViolentCrimeRateMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2851 bytes)
- `data/sample_submission.csv` (4945 bytes); columns: ["id", "violent_crime_rate_per_100k"]
- `data/test.csv` (37918 bytes); columns: ["id", "county_name", "population", "COVIND", "FIPS_ST", "FIPS_CTY", "BURGLRY", "LARCENY", "MVTHEFT", "ARSON", "MODINDX"]
- `data/train.csv` (186015 bytes); columns: ["county_name", "population", "COVIND", "FIPS_ST", "FIPS_CTY", "BURGLRY", "LARCENY", "MVTHEFT", "ARSON", "MODINDX", "violent_crime_rate_per_100k"]

## Public description

County Violent Crime Rate Prediction (UCR 2016)

Problem statement
Build a model to predict the county-level violent crime rate per 100,000 residents in the United States for 2016. The target is defined as:
violent_crime_rate_per_100k = 100000 × (MURDER + RAPE + ROBBERY + AGASSLT) / population.

To avoid label leakage, test features exclude all violent crime category counts and any precomputed overall crime rate fields. Participants should infer violent crime rates from non-violent features, demographics, and coverage indicators.

Files provided
- train.csv: training data with features and the target violent_crime_rate_per_100k.
- test.csv: test data with features only and an id column.
- sample_submission.csv: example submission with the expected columns and random plausible values.

Features
Features focus on non-violent variables and geographic/context fields. Typical columns include:
- population: Resident population count (denominator for rate normalization).
- COVIND: Coverage indicator (percent of reporting coverage; often 100).
- FIPS_ST, FIPS_CTY: State and county FIPS codes (categorical/geospatial identifiers).
- BURGLRY, LARCENY, MVTHEFT, ARSON: Property crime counts.
- MODINDX: Property crime index count (if present).
- county_name: County descriptor (string; can be parsed or encoded).

Note: Violent counts (MURDER, RAPE, ROBBERY, AGASSLT) and precomputed overall crime rate fields are not present in test.csv and should not be used as features. The exact column set may include additional administrative fields removed from test/train features to prevent leakage.

Evaluation
- Metric: Mean Absolute Error (MAE) on violent_crime_rate_per_100k.
- Submission format: A CSV with exactly two columns, in order: id, violent_crime_rate_per_100k. The id values must match and be in the same order as the ids in test.csv.

Why MAE?
- Interpretable: Errors are in native rate units (per 100k residents).
- Robust: Handles heavy-tailed distributions and small-population counties better than RMSE, and avoids RMSLE issues when true rates can be zero.

Modeling guidance
- Data processing: Ensure numeric parsing is correct and values are finite. Consider transformations (e.g., log1p for skewed counts) and standardization.
- Feature engineering: Normalize property crime counts to rates per 100k using population; encode FIPS_ST/FIPS_CTY to capture regional variation; optionally use MODINDX; parse county_name to extract state abbreviations.
- Training: Try regularized regression, tree ensembles, gradient boosting, and other regressors. Address heteroskedasticity (small vs large counties) and potential covariate shift across states.

Split design
The train/test split is deterministic and stratified by state (FIPS_ST) to ensure broad geographic coverage and a challenging generalization test while remaining solvable.
