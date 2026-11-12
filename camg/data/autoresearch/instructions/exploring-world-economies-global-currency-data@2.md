# OpenMLE-fast task

Task ID: `exploring-world-economies-global-currency-data@2`

Native metric: `GlobalGDPPerCapitaRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3691 bytes)
- `data/sample_submission.csv` (10833 bytes); columns: ["row_id", "target"]
- `data/test.csv` (60208 bytes); columns: ["Country Name", "Country Code", "Region", "IncomeGroup", "Year", "Birth rate, crude (per 1,000 people)", "Death rate, crude (per 1,000 people)", "Electric power consumption (kWh per capita)", "GDP (USD)", "GDP per capita (USD)", "Individuals using the Internet (% of population)", "Infant mortality rate (per 1,000 live births)", "Life expectancy at birth (years)", "Population density (people per sq. km of land area)", "Unemployment (% of total labor force) (modeled ILO estimate)", "hdi", "gnipc_ppp2017", "row_id"]
- `data/train.csv` (1338533 bytes); columns: ["Country Name", "Country Code", "Region", "IncomeGroup", "Year", "Birth rate, crude (per 1,000 people)", "Death rate, crude (per 1,000 people)", "Electric power consumption (kWh per capita)", "GDP (USD)", "GDP per capita (USD)", "Individuals using the Internet (% of population)", "Infant mortality rate (per 1,000 live births)", "Life expectancy at birth (years)", "Population density (people per sq. km of land area)", "Unemployment (% of total labor force) (modeled ILO estimate)", "hdi", "gnipc_ppp2017", "row_id", "target"]

## Public description

Global Development Panel Forecasting: Next‑Year GDP per Capita

Problem statement
You are given yearly country-level development indicators. For each country and year t, predict the country’s GDP per capita (USD) for year t+1. Models must rely only on information available up to and including year t. This is a panel time‑series regression task with a strict chronological split for evaluation.

Data description
- train.csv: Panel of country‑years used for model training. Each row corresponds to a country‑year t and contains:
  - row_id: unique identifier for a country‑year (e.g., ISO3 code + year)
  - Country Name, Country Code, Region, IncomeGroup
  - Year: the reference year t
  - World Bank development indicators for year t (e.g., birth/death rates, life expectancy, unemployment, population density, electricity consumption, internet usage, GDP (USD), GDP per capita (USD), etc.)
  - UNDP/HDI features aligned at year t (e.g., human development index, life expectancy, education years, inequality measures, GNI per capita in 2017 PPP, etc.)
  - target: the value to predict during training — GDP per capita (USD) at year t+1

- test.csv: Same structure as train.csv but without the target column. It contains country‑years strictly after the training cutoff; each row corresponds to a country‑year t for which you must predict GDP per capita (USD) at year t+1.

- sample_submission.csv: A valid example of the expected submission format with randomly generated non‑negative values.

Target and forecasting setup
- For each row (country‑year t), the label is GDP per capita (USD) at t+1. You may freely engineer features from columns at year t (e.g., lags, moving averages using only past values) and combine information across indicators. Do not use information from years later than t for that row.

Evaluation
- Primary metric: RMSLE (root mean squared logarithmic error) between the predicted and true GDP per capita (USD) for year t+1.
  - Definition: RMSLE = sqrt(mean((log1p(y_pred) − log1p(y_true))^2))
  - All values are clipped at a minimum of zero inside the metric to avoid issues with small negatives.
  - Lower is better.
- Tie‑breaker (reported but not used for ranking): MAE on log‑levels, i.e., mean absolute error of log1p values.

Submission format
- A single CSV with exactly two columns in this order:
  - row_id: matches the identifiers in test.csv
  - target: your predicted GDP per capita (USD) for year t+1 (non‑negative real numbers)
- The set of row_id must match test.csv exactly (order is not important). Duplicates, missing, non‑finite, or negative targets will be rejected.

Train/test split policy
- A chronological split is used to emulate genuine forecasting. Training rows are from earlier years (up to a fixed cutoff), and test rows are from the immediately following 2–3 years where labels are available. This prevents look‑ahead and encourages robust generalization across countries and time.

Notes and recommendations
- Feature engineering is essential. Consider lags, growth rates (e.g., log‑changes), moving averages, and interaction terms derived from year‑t indicators. Handle missing data carefully; robust imputation fitted on training data only is allowed.
- The dataset spans many countries and decades with heterogeneous dynamics and varying coverage, making the task challenging but solvable by classical ML (e.g., ridge/elastic net, gradient‑boosted trees) and sequence models (e.g., RNNs/transformers on yearly panels).
- Use cross‑validation on the training period (e.g., time‑based folds) for model selection. Keep validation strictly within the training years to avoid leakage.
