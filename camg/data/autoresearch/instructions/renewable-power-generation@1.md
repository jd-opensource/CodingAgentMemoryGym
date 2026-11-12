# OpenMLE-fast task

Task ID: `renewable-power-generation@1`

Native metric: `EnergyConsumptionSMAPEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3646 bytes)
- `data/sample_submission.csv` (4255 bytes); columns: ["Country", "Year", "Consumption_TWh"]
- `data/test.csv` (24675 bytes); columns: ["Year", "Country", "World", "OECD", "BRICS", "Europe", "North_America", "Latin_America", "Asia", "Pacific", "Africa", "Middle_East", "CIS", "Europe_if_member", "North_America_if_member", "Latin_America_if_member", "Asia_if_member", "Pacific_if_member", "Africa_if_member", "Middle_East_if_member", "CIS_if_member", "BRICS_if_member", "Hydro_TWh", "Biofuel_TWh", "Solar_PV_TWh", "Geothermal_TWh"]
- `data/train.csv` (270095 bytes); columns: ["Year", "Country", "Consumption_TWh", "World", "OECD", "BRICS", "Europe", "North_America", "Latin_America", "Asia", "Pacific", "Africa", "Middle_East", "CIS", "Europe_if_member", "North_America_if_member", "Latin_America_if_member", "Asia_if_member", "Pacific_if_member", "Africa_if_member", "Middle_East_if_member", "CIS_if_member", "BRICS_if_member", "Hydro_TWh", "Biofuel_TWh", "Solar_PV_TWh", "Geothermal_TWh"]

## Public description

Global Country Energy Consumption Forecasting (2018–2020)

Problem statement
Participants must build models to forecast annual total energy consumption (TWh) for every country for the years 2018, 2019, and 2020. Historical country-level consumption (1990–2017) is provided, along with contemporaneous macro aggregates (e.g., World, regions/blocks) and global renewable generation trends. Your task is to produce accurate point forecasts for all country–year pairs in the test set.

Data description
You are given panel time-series data with one row per country-year. The following files are provided:
- train.csv: Historical features and the target Consumption_TWh for all countries from 1990 through 2017 (inclusive).
- test.csv: Features for all countries for 2018–2020 (target removed). Predict the numeric column Consumption_TWh for each row.
- sample_submission.csv: Example submission with valid format and plausible values.

Feature columns include:
- Country (string), Year (int).
- Global and regional aggregates per year (e.g., World, OECD, BRICS, Europe, North_America, Latin_America, Asia, Pacific, Africa, Middle_East, CIS). For some regions, a “_if_member” feature is included that equals the region’s annual total if the country belongs to that region, else 0.
- Global renewable generation time series (Hydro_TWh, Biofuel_TWh, Solar_PV_TWh, Geothermal_TWh) aligned by Year. Note: these series are only available through 2017 and appear as missing in later years in test.csv; you may handle these as part of your modeling strategy.

Target
- Consumption_TWh: total energy consumption of the country in a given year (continuous, non-negative).

What you need to predict
- For every row in test.csv (all countries for 2018–2020), predict Consumption_TWh and submit a file with columns: Country, Year, Consumption_TWh.

Evaluation
Submissions are evaluated using Symmetric Mean Absolute Percentage Error (SMAPE), averaged uniformly over all country–year targets:
SMAPE = 100 * mean( 2 * |y_true - y_pred| / (|y_true| + |y_pred| + eps) )
- eps is a small constant to avoid division by zero; when both y_true and y_pred are zero, the contribution is defined as 0.
- Lower SMAPE is better.

Notes and recommendations
- This is a multivariate, panel forecasting task. Consider feature engineering such as lags, rolling statistics, growth rates, and country-specific trend terms. Global models across countries often work well.
- Use time-aware validation (e.g., rolling or expanding windows). A typical setup is training up to 2014–2016 and validating on 2015–2017.
- Regional aggregates can be leveraged directly (e.g., as exogenous covariates) or combined with country membership features. Handle missing covariates in 2018–2020 carefully (e.g., model without them, impute using reasonable projections, or encode “unknown” indicators). Avoid using post-2017 information that would leak test labels.

Submission format
- CSV with columns exactly: Country, Year, Consumption_TWh.
- Each (Country, Year) pair from test.csv must appear exactly once.
- Predictions must be numeric and non-negative.

Files you will see
- train.csv
- test.csv
- sample_submission.csv

Tips to get started
- Baseline: a per-country last-value or trend extrapolation model is a decent starting point.
- Stronger approaches: gradient boosting on panel features; regularized panel regressions; global forecasting models (e.g., LightGBM/XGBoost/CatBoost) with lags and interactions; classical univariate models per country, then meta-learning across countries.
- Ensure deterministic pipelines and robust handling of numeric stability.
