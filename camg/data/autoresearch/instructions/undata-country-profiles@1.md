# OpenMLE-fast task

Task ID: `undata-country-profiles@1`

Native metric: `InfantMortalityRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3513 bytes)
- `data/sample_submission.csv` (913 bytes); columns: ["id", "InfantMortality"]
- `data/test.csv` (14048 bytes); columns: ["id", "Region", "Surface area (km2)", "Population in thousands (2017)", "Population density (per km2, 2017)", "Sex ratio (m per 100 f, 2017)", "GDP: Gross domestic product (million current US$)", "GDP growth rate (annual %, const. 2005 prices)", "GDP per capita (current US$)", "Economy: Agriculture (% of GVA)", "Economy: Industry (% of GVA)", "Economy: Services and other activity (% of GVA)", "Employment: Agriculture (% of employed)", "Employment: Industry (% of employed)", "Employment: Services (% of employed)", "Unemployment (% of labour force)", "Agricultural production index (2004-2006=100)", "Food production index (2004-2006=100)", "International trade: Exports (million US$)", "International trade: Imports (million US$)", "International trade: Balance (million US$)", "Balance of payments, current account (million US$)", "Population growth rate (average annual %)", "Urban population (% of total population)", "Urban population growth rate (average annual %)", "Fertility rate, total (live births per woman)", "Refugees and others of concern to UNHCR (in thousands)", "Health: Total expenditure (% of GDP)", "Health: Physicians (per 1000 pop.)", "Education: Government expenditure (% of GDP)", "Seats held by women in national parliaments %", "Mobile-cellular subscriptions (per 100 inhabitants)", "Mobile-cellular subscriptions (per 100 inhabitants).1", "Threatened species (number)", "CO2 emission estimates (million tons/tons per capita)", "Energy production, primary (Petajoules)", "Pop. using improved sanitation facilities (urban/rural, %)", "is_kiva_country", "LFPR_female", "LFPR_male", "female_LE", "male_LE", "age_0_14_pct", "age_60_plus_pct", "intl_migrant_thousands", "%_of_pop", "Primary_f", "Primary_m", "Secondary_f", "Secondary_m", "Tertiary_f", "Tertiary_m", "Forested area (% of land area)_a", "Forested area (% of land area)_b", "Energy supply per capita (Gigajoules)_a", "Energy supply per capita (Gigajoules)_b", "water_urban", "water_rural"]
- `data/train.csv` (49775 bytes); columns: ["id", "Region", "Surface area (km2)", "Population in thousands (2017)", "Population density (per km2, 2017)", "Sex ratio (m per 100 f, 2017)", "GDP: Gross domestic product (million current US$)", "GDP growth rate (annual %, const. 2005 prices)", "GDP per capita (current US$)", "Economy: Agriculture (% of GVA)", "Economy: Industry (% of GVA)", "Economy: Services and other activity (% of GVA)", "Employment: Agriculture (% of employed)", "Employment: Industry (% of employed)", "Employment: Services (% of employed)", "Unemployment (% of labour force)", "Agricultural production index (2004-2006=100)", "Food production index (2004-2006=100)", "International trade: Exports (million US$)", "International trade: Imports (million US$)", "International trade: Balance (million US$)", "Balance of payments, current account (million US$)", "Population growth rate (average annual %)", "Urban population (% of total population)", "Urban population growth rate (average annual %)", "Fertility rate, total (live births per woman)", "Refugees and others of concern to UNHCR (in thousands)", "Health: Total expenditure (% of GDP)", "Health: Physicians (per 1000 pop.)", "Education: Government expenditure (% of GDP)", "Seats held by women in national parliaments %", "Mobile-cellular subscriptions (per 100 inhabitants)", "Mobile-cellular subscriptions (per 100 inhabitants).1", "Threatened species (number)", "CO2 emission estimates (million tons/tons per capita)", "Energy production, primary (Petajoules)", "Pop. using improved sanitation facilities (urban/rural, %)", "is_kiva_country", "LFPR_female", "LFPR_male", "female_LE", "male_LE", "age_0_14_pct", "age_60_plus_pct", "intl_migrant_thousands", "%_of_pop", "Primary_f", "Primary_m", "Secondary_f", "Secondary_m", "Tertiary_f", "Tertiary_m", "Forested area (% of land area)_a", "Forested area (% of land area)_b", "Energy supply per capita (Gigajoules)_a", "Energy supply per capita (Gigajoules)_b", "water_urban", "water_rural", "InfantMortality"]

## Public description

Global Infant Mortality Prediction Challenge

Background
Infant mortality is a core public health outcome reflecting access to care, nutrition, sanitation, and broader socio‑economic conditions. The provided UNData country profiles (2017 or most recent prior) aggregate diverse indicators across the economy, society, environment, and infrastructure for countries worldwide.

Problem Statement
Predict each country’s infant mortality rate (per 1,000 live births) using other country‑level indicators. Build models that generalize across regions and handle missingness, heterogeneity and multicollinearity in the indicators.

Data Description
You are provided with country‑level tabular data featuring:
- Demographic and population statistics (population, density, sex ratio, urbanization, fertility, age distribution, migrant stock, refugees).
- Economic indicators (GDP and GDP per capita, sectoral GVA shares, employment shares, unemployment, labour force participation, trade flows, current account).
- Social indicators (life expectancy split by sex, health expenditure, physicians per 1,000, education expenditure, primary/secondary/tertiary enrolment splits by sex, seats held by women in parliament).
- Infrastructure and environment (mobile subscriptions, threatened species, forested area, CO2 emissions, energy production/supply, access to improved water and sanitation split urban/rural).

Final competition files
- train.csv — Training data containing features and the target column InfantMortality.
- test.csv — Test data containing only features for the countries to be evaluated.
- sample_submission.csv — Example submission with columns id, InfantMortality.

Important notes
- Country names are not included as a feature to prevent trivial memorization. A numeric id column links rows across files.
- Indicator values may contain missing entries; robust preprocessing is required. Some indicators originally reported as split values (e.g., female/male, urban/rural) appear as separate numeric features.

Target and Task Type
- Target: InfantMortality — infant mortality rate per 1,000 live births (continuous).
- Task: Regression.

Evaluation Metric
- Mean Absolute Error (MAE) between your submitted predictions and the ground truth on the test set.
- Formal definition: MAE = average over test countries of |prediction − ground_truth|.
- Rationale: MAE is robust to outliers common in cross‑country indicators, interpretable in natural units, and treats each country equally.

Train/Test Split
- Single 80/20 split created deterministically and region‑aware to preserve geographic representation, while ensuring countries with very rare regions remain in training when necessary.

Submission Format
- CSV file with two columns: id and InfantMortality.
- Each id must correspond to exactly one test row; predictions must be numeric and finite.

Tips
- Handle special placeholders (e.g., missing markers) appropriately.
- Parse split indicators (e.g., female/male, urban/rural, million tons/tons per capita) into separate numeric features.
- Consider log transforms for skewed quantities (e.g., GDP per capita, trade, energy) and robust imputation for missing values.
- One‑hot encode Region.
- Evaluate models with cross‑validation on training data to avoid overfitting.

Goal
Achieve low MAE by building well‑processed, robust models that capture the relationships between socio‑economic, health, and infrastructure indicators and infant mortality across countries.
