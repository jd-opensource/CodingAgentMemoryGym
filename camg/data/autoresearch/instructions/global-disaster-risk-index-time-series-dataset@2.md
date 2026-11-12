# OpenMLE-fast task

Task ID: `global-disaster-risk-index-time-series-dataset@2`

Native metric: `WorldRiskIndexQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3277 bytes)
- `data/sample_submission.csv` (2130 bytes); columns: ["id", "next_wri_category"]
- `data/test.csv` (14783 bytes); columns: ["id", "Region", "Year", "WRI", "Exposure", "Vulnerability", "Susceptibility", "Lack of Coping Capabilities", "Lack of Adaptive Capacities", "Exposure Category", "WRI Category", "Vulnerability Category", "Susceptibility Category"]
- `data/train.csv` (126952 bytes); columns: ["id", "Region", "Year", "WRI", "Exposure", "Vulnerability", "Susceptibility", "Lack of Coping Capabilities", "Lack of Adaptive Capacities", "Exposure Category", "WRI Category", "Vulnerability Category", "Susceptibility Category", "next_wri_category"]

## Public description

Competition: Ordinal Global Disaster Risk Forecast (Next-Year Category)

Problem statement
- Task: From each country/region’s historical annual profiles, predict the next year’s WorldRiskIndex (WRI) Category (an ordinal 5-level tier: Very Low, Low, Medium, High, Very High).
- Target year: Predict the 2021 WRI Category for each region using its 2020 (and earlier) information.
- Framing: Supervised, ordinal classification on a panel time series. Train on past “next-year” transitions, then forecast the next-year category for the final year.

Data description
You are given a yearly panel (2011–2021) of ~180 regions with numeric indicators and categorical tiers.
- Features per row (year t):
  - Region (string identifier)
  - Year (integer)
  - WRI, Exposure, Vulnerability, Susceptibility, Lack of Coping Capabilities, Lack of Adaptive Capacities (floats in [0, 100])
  - WRI Category, Exposure Category, Vulnerability Category, Susceptibility Category (strings; each one of {Very Low, Low, Medium, High, Very High})
- Label per row (used only in train): next_wri_category, which is the WRI Category of the same region at year t+1.

Final files provided
- train.csv: Historical samples (years up to 2019). Each row is a (Region, Year=t) feature vector with the label next_wri_category equal to the region’s WRI Category at year t+1.
- test.csv: One row per region for Year=2020 containing only the features (no labels) and an id column.
- sample_submission.csv: A valid example submission with random labels.

Important notes
- All features in test.csv come from year 2020 (and earlier) only. No 2021 features are included; you must forecast 2021 WRI Category from history.
- Region names may include different endonyms and diacritics. Treat them as categorical identifiers; ensure chronological ordering for any feature engineering based on lags/differences.
- The panel is not perfectly complete across all regions/years; handle missing histories robustly.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) with 5 ordered classes in the following order: Very Low < Low < Medium < High < Very High.
- Submission format: A CSV with two columns: id, next_wri_category. The id must exactly match the ids in test.csv; next_wri_category must be one of the five allowed categories.

Recommended modeling workflow
- Data processing: Normalize headers, coerce numerics to floats, standardize category strings, and sort by (Region, Year).
- Feature engineering: Lagged categories (1–3 years), recent run-length in category, trends/differences of numeric indicators (e.g., ΔWRI, rolling means), and interactions between numeric and categorical signals.
- Modeling: Ordinal regression (e.g., ordered logistic), gradient boosting with ordinal encoding and class-weighting, sequence models leveraging region histories, or stacking/ensembling.

Reproducibility and constraints
- A fixed temporal split is used: train up to 2019→2020 transitions; test is 2020→2021. All five classes appear in training labels; every class present in test is seen in training at least once.
- Do not use any external data.

Deliverables
- Submit predictions for all ids in test.csv in a file named submission.csv (two columns: id, next_wri_category). Scoring is performed with QWK.
