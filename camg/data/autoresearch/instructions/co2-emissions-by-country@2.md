# OpenMLE-fast task

Task ID: `co2-emissions-by-country@2`

Native metric: `CO2AsinhRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3272 bytes)
- `data/sample_submission.csv` (74032 bytes); columns: ["country_code", "country_name", "year", "value"]
- `data/test.csv` (38512 bytes); columns: ["country_code", "country_name", "year"]
- `data/train.csv` (306584 bytes); columns: ["country_code", "country_name", "year", "value"]

## Public description

Global CO2 Panel Imputation Challenge (1960–2019)

Problem statement
Reconstruct a hidden subset of historical CO2 emissions at the country–year level. You are given a global panel of annual CO2 emissions (kilotons) for real countries and territories from 1960–2019. A stratified subset of observed country–year entries has been masked and provided as test data. Your task is to impute the missing emission values as accurately as possible using information across time and countries.

What makes this challenging
- Scale and heterogeneity: Emissions span orders of magnitude across countries and decades, with structural breaks and changing growth regimes.
- Sparsity at the edges: Early decades for some countries are sparse; you must leverage both temporal dynamics and cross-country similarities.
- No aggregates: Regional/income aggregates are removed to avoid leakage from deterministic sums and to focus the task on country-level modeling.

Files provided (under public/)
- train.csv — Observed country–year emissions for real countries/territories (columns: country_code, country_name, year, value). These are the rows you can train with.
- test.csv — The masked country–year rows to predict (columns: country_code, country_name, year). These rows are removed from train.
- sample_submission.csv — Example submission with randomly generated, valid numeric predictions (columns: country_code, country_name, year, value).

Target to predict
- value — CO2 emissions in kilotons (kt) for the corresponding (country_code, country_name, year).

Evaluation
- Metric: Root Mean Squared Error (RMSE) on asinh-transformed values.
  score = sqrt(mean( (asinh(y_pred) − asinh(y_true))^2 ))
- Rationale: Emissions vary by several orders of magnitude. The inverse hyperbolic sine (asinh) behaves like log for large values and like linear near zero. It is defined at zero and for negatives, yielding a scale-stable, fair loss across small islands and large emitters.

Submission format
- A single CSV with the exact rows and columns of test.csv plus the value column:
  [country_code, country_name, year, value]
- Each (country_code, country_name, year) must appear exactly once. Extra/missing rows or duplicates will be rejected.
- value must be finite numeric for every row.

Notes and guidance
- This is retrospective imputation, not forecasting: You may use any year available in train (past or future) to impute a masked row.
- Feature ideas: lags/leads, rolling statistics, country embeddings, matrix factorization, graph/hierarchical pooling, sequence models with masking, gradient boosting on engineered panel features.
- Robust baselines include: per-country smoothing splines; matrix completion (SVD/ALS) on the country–year matrix; GBMs with temporal and regional features.

Data integrity and split
- The panel consists only of real countries/territories; regional and income-group aggregates are excluded. True missing cells in the source are not used as targets. Edge years (first/last observed per country) are retained in train to anchor the time span.
- The split is deterministic and stratified by country and decade (~20% of eligible internal country–year cells are masked). The same train/test split is provided to all participants.
