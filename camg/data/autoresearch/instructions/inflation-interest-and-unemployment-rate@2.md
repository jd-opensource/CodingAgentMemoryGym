# OpenMLE-fast task

Task ID: `inflation-interest-and-unemployment-rate@2`

Native metric: `CountryMacroMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3225 bytes)
- `data/sample_submission.csv` (18655 bytes); columns: ["row_id", "spread"]
- `data/test.csv` (416659 bytes); columns: ["row_id", "iso3c", "country", "year", "adminregion", "incomeLevel", "dep_rate_lag1", "dep_rate_lag2", "dep_rate_lag3", "dep_rate_mean3", "dep_rate_lag_miss_frac", "lend_rate_lag1", "lend_rate_lag2", "lend_rate_lag3", "lend_rate_mean3", "lend_rate_lag_miss_frac", "real_rate_lag1", "real_rate_lag2", "real_rate_lag3", "real_rate_mean3", "real_rate_lag_miss_frac", "cpi_inflation_lag1", "cpi_inflation_lag2", "cpi_inflation_lag3", "cpi_inflation_mean3", "cpi_inflation_lag_miss_frac", "gdpdef_inflation_lag1", "gdpdef_inflation_lag2", "gdpdef_inflation_lag3", "gdpdef_inflation_mean3", "gdpdef_inflation_lag_miss_frac", "unemp_nat_lag1", "unemp_nat_lag2", "unemp_nat_lag3", "unemp_nat_mean3", "unemp_nat_lag_miss_frac", "unemp_ilo_lag1", "unemp_ilo_lag2", "unemp_ilo_lag3", "unemp_ilo_mean3", "unemp_ilo_lag_miss_frac", "spread_lag1", "spread_lag2", "spread_lag3", "spread_mean3", "spread_lag_miss_frac", "post_2008", "post_2020"]
- `data/train.csv` (1906723 bytes); columns: ["row_id", "iso3c", "country", "year", "adminregion", "incomeLevel", "dep_rate_lag1", "dep_rate_lag2", "dep_rate_lag3", "dep_rate_mean3", "dep_rate_lag_miss_frac", "lend_rate_lag1", "lend_rate_lag2", "lend_rate_lag3", "lend_rate_mean3", "lend_rate_lag_miss_frac", "real_rate_lag1", "real_rate_lag2", "real_rate_lag3", "real_rate_mean3", "real_rate_lag_miss_frac", "cpi_inflation_lag1", "cpi_inflation_lag2", "cpi_inflation_lag3", "cpi_inflation_mean3", "cpi_inflation_lag_miss_frac", "gdpdef_inflation_lag1", "gdpdef_inflation_lag2", "gdpdef_inflation_lag3", "gdpdef_inflation_mean3", "gdpdef_inflation_lag_miss_frac", "unemp_nat_lag1", "unemp_nat_lag2", "unemp_nat_lag3", "unemp_nat_mean3", "unemp_nat_lag_miss_frac", "unemp_ilo_lag1", "unemp_ilo_lag2", "unemp_ilo_lag3", "unemp_ilo_mean3", "unemp_ilo_lag_miss_frac", "spread_lag1", "spread_lag2", "spread_lag3", "spread_mean3", "spread_lag_miss_frac", "post_2008", "post_2020", "spread"]

## Public description

Title: Cross-Country Lending Rate Spread Forecast (2016–2021)

Problem statement
Participants must forecast each country’s one-year-ahead banking interest rate spread:
  spread_t = Lending interest rate_t − Deposit interest rate_t
Using only information available up to the previous year, predict spread for all country–years from 2016 through 2021. The task is a panel time-series regression problem across countries.

Files
- train.csv: Feature matrix with lagged (t−1, t−2, t−3) and simple rolling features constructed from the historical macro-financial series, plus identifiers. Includes the target column spread.
- test.csv: Same columns as train.csv except the target spread is withheld. Contains all country–years 2016–2021 where the target exists.
- sample_submission.csv: A valid sample formatted submission with row_id and spread columns.

Data description
Each row represents a country–year observation. Identifiers include row_id (unique), iso3c, country, and year, plus static descriptors adminregion and incomeLevel. Feature columns are derived strictly from information available up to year t−1 for that country:
- Lagged levels: dep_rate_lag{k}, lend_rate_lag{k}, spread_lag{k}, real_rate_lag{k}, cpi_inflation_lag{k}, gdpdef_inflation_lag{k}, unemp_nat_lag{k}, unemp_ilo_lag{k} for k ∈ {1,2,3}.
- Three-year trailing means (computed over lags): dep_rate_mean3, lend_rate_mean3, spread_mean3, real_rate_mean3, cpi_inflation_mean3, gdpdef_inflation_mean3, unemp_nat_mean3, unemp_ilo_mean3.

Targets
- spread: Lending − Deposit for year t, provided in train.csv only.

Important notes
- No contemporaneous (year t) deposit or lending rate values are present in features, preventing label leakage.
- Countries are restricted to valid ISO3 codes (alphabetic 3-letter) to exclude regional aggregates.
- Missing values in features reflect real-world data gaps; participants should implement appropriate imputation or models that handle missingness.

Evaluation
- Submissions must contain two columns: row_id and spread, covering all rows in test.csv.
- The competition metric is Country-Macro Mean Absolute Error (MAE):
  1) For each country, compute the mean absolute error over its test years.
  2) Average these per-country MAEs equally across countries.
This macro-averaging ensures countries with more test years do not dominate the score.

Submission format
- CSV with header: row_id,spread
- row_id exactly matches the identifiers in test.csv.
- spread must be a finite numeric value for every row.

Recommended modeling approaches
- Strong baselines: persistence on spread_lag1; linear or ridge regression on lagged features.
- Advanced: gradient boosting (LightGBM/XGBoost/CatBoost), random forests, panel regularized regression, and sequence models.
- Feature ideas: additional lags/rolling windows, regime dummies (e.g., post-2008/2020), interaction with incomeLevel/adminregion, and missingness indicators.

Rules and constraints
- Use only features derived from information up to t−1.
- Do not attempt to reverse-engineer withheld labels; external data is allowed if properly time-aligned and non-leaking.

Good luck and have fun forecasting cross-country banking spreads!
