# OpenMLE-fast task

Task ID: `increasing-crop-yields-v5@1`

Native metric: `WheatYieldForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3532 bytes)
- `data/sample_submission.csv` (9964 bytes); columns: ["Entity", "Year", "Wheat yield"]
- `data/test.csv` (4320 bytes); columns: ["Entity", "Year"]
- `data/train.csv` (134800 bytes); columns: ["Entity", "Year", "Wheat yield"]

## Public description

Title: Global Wheat Yield Forecasting Challenge (2021–2023)

Background
Accurately forecasting national wheat yields helps governments, markets, and humanitarian organizations plan procurement, storage, imports, and food security measures. Yields evolve over decades with technology and practices, but remain volatile year-to-year due to climate, pests, and shocks. Robust, generalizable forecasting models are critical to anticipate short-term outcomes across diverse countries.

Problem Statement
Given each country’s historical annual wheat yield series up to 2020, forecast the next three years’ yields: 2021, 2022, and 2023, for a fixed set of eligible countries. Models must generalize across heterogeneous countries, nonstationary trends, and irregular histories. This is a pure time-series regression problem with no covariates beyond past yields. Wheat yield is a continuous numeric target (tonnes per hectare).

Data Description
- Training file (train.csv): Panel of annual wheat yields with columns [Entity, Year, Wheat yield] for the selected countries and years ≤ 2020.
- Test file (test.csv): The forecast targets to be predicted with columns [Entity, Year] for the same countries and years 2021–2023.
- Sample submission (sample_submission.csv): Example submission with the required format and randomized valid predictions.

Split and Scope
- Countries are limited to non-aggregate national entities with sufficient history and complete test horizons.
- Training covers years 1961–2020; test covers 2021–2023.
- All entities in test appear in training; each has at least 30 observations in 1961–2023.

Submission Format
- Submit a CSV with exactly the same rows as test.csv and columns [Entity, Year, Wheat yield].
- The Entity and Year must match test.csv exactly and be in the same order; Wheat yield contains your numeric forecasts.
- Lower scores are better.

Evaluation Metric
- Macro-averaged MASE (Mean Absolute Scaled Error).
  - For each country i, compute its in-sample naïve one-step forecast MAE on training years (naïve: ŷ_t = y_{t−1}). This scale S_i = mean_t |y_t − y_{t−1}| uses only training data.
  - For each test row (country-year), compute the absolute error |y_t − ŷ_t| and scale it by S_i.
  - The leaderboard score is the mean of these scaled errors across all test rows (countries and years). This metric is scale-free and fair across countries with different yield levels.
  - Numerical stability: if S_i = 0, a small epsilon is used to avoid division-by-zero.

What Makes This Challenging
- Three-step forecasting compounds uncertainty.
- Nonstationary and heterogeneous dynamics across countries.
- Irregular histories and missing years require careful feature engineering.
- Limited covariates: models must extract signal from past yields alone.

Modeling Guidance
- Recommended processing: sort by Entity and Year; use only years ≤ 2020 for fitting; do not peek at test-period yields.
- Feature ideas: lags, differences, moving averages, trend features, volatility estimates; global models that share parameters across entities; classical time-series (ETS/ARIMA/state-space) or ML approaches (gradient boosting on engineered features, RNN/TCN/transformers on panel sequences).

Files Provided
- train.csv
- test.csv
- sample_submission.csv

Your task
Train your model(s) on train.csv and produce predictions for all rows in test.csv. Submit a CSV in the specified format. Scores are computed using macro-averaged MASE across all test rows. Lower is better.
