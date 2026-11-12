# OpenMLE-fast task

Task ID: `world-happiness-index-and-inflation-dataset@1`

Native metric: `InflationForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3322 bytes)
- `data/sample_submission.csv` (5526 bytes); columns: ["row_id", "next_year_headline_cpi"]
- `data/test.csv` (38556 bytes); columns: ["row_id", "Country", "Year", "Headline Consumer Price Inflation", "Energy Consumer Price Inflation", "Food Consumer Price Inflation", "Official Core Consumer Price Inflation", "Producer Price Inflation", "GDP deflator Index growth rate", "Continent/Region", "Score", "GDP per Capita", "Social support", "Healthy life expectancy at birth", "Freedom to make life choices", "Generosity", "Perceptions of corruption"]
- `data/train.csv` (159428 bytes); columns: ["Country", "Year", "Headline Consumer Price Inflation", "Energy Consumer Price Inflation", "Food Consumer Price Inflation", "Official Core Consumer Price Inflation", "Producer Price Inflation", "GDP deflator Index growth rate", "Continent/Region", "Score", "GDP per Capita", "Social support", "Healthy life expectancy at birth", "Freedom to make life choices", "Generosity", "Perceptions of corruption", "next_year_headline_cpi"]

## Public description

Title: Forecast Next-Year Headline CPI from Happiness and Economic Indicators (2015–2023)

Problem statement
Participants are tasked with forecasting a country’s next-year Headline Consumer Price Inflation using its current-year social well-being and macroeconomic indicators. The dataset spans 2015–2023 and covers 148 countries worldwide. For each country-year y, if the next year (y+1) exists and its headline CPI is known, we construct a supervised sample with features from year y and the target equal to headline CPI in year y+1.

Why this is challenging and meaningful
- Realistic forecasting task that blends social science and macroeconomics.
- Cross-country generalization with covariate and label shift during 2020–2023 (pandemic, energy shocks).
- Heterogeneity across countries and missingness in subcomponent series (e.g., energy/food CPI) require careful preprocessing and robust modeling.
- Uses nearly all available features to enable creative feature engineering.

Data description
Each row in the provided training and test files corresponds to a country-year “current year” sample. The target is the next-year headline CPI for the same country.

Key feature columns (current-year):
- Country, Year, Continent/Region
- Headline Consumer Price Inflation
- Energy Consumer Price Inflation
- Food Consumer Price Inflation
- Official Core Consumer Price Inflation
- Producer Price Inflation
- GDP deflator Index growth rate
- Score (World Happiness Index)
- GDP per Capita
- Social support
- Healthy life expectancy at birth
- Freedom to make life choices
- Generosity
- Perceptions of corruption

Target column:
- next_year_headline_cpi (numeric, the headline CPI at year y+1 for the same country)

Final competition files
- train.csv: Supervised training data with all features and the target column next_year_headline_cpi.
- test.csv: Test data with the same feature columns only, plus a row_id column used for submission alignment. The target column is not included here.
- sample_submission.csv: Example submission with columns [row_id, next_year_headline_cpi]. Values are valid numeric placeholders.

Train/test split
- Time-based split only. Samples are constructed when a valid next-year headline CPI exists.
- Training set: samples whose label (next-year) falls in 2016–2021.
- Test set: samples whose label (next-year) falls in 2022–2023.
- Countries and continents present in the test set also appear in the training set.

Submission format
- A CSV file with exactly two columns: row_id and next_year_headline_cpi.
- row_id must match the identifiers provided in test.csv.
- next_year_headline_cpi must be finite numeric values.

Evaluation metric
- Mean Absolute Error (MAE) on next_year_headline_cpi.
- Rationale: MAE is scale-consistent across countries and robust to extreme inflation episodes, yielding a fair, precise measure of average deviation without over-penalizing outliers.

Notes
- No external data is required. Participants may perform any data processing, imputation, and feature engineering on the provided features.
- Categorical features (e.g., Country, Continent/Region) are permitted; appropriate encodings are up to the participant.
- Numeric scaling is optional.
- Be mindful that some subcomponent series have missing values; robust handling is encouraged.
