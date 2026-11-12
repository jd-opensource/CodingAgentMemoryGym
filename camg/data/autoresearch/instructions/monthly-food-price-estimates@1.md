# OpenMLE-fast task

Task ID: `monthly-food-price-estimates@1`

Native metric: `FoodInflationForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3271 bytes)
- `data/sample_submission.csv` (7838 bytes); columns: ["country", "iso3", "date", "Inflation"]
- `data/test.csv` (16186 bytes); columns: ["country", "iso3", "date", "Open", "High", "Low", "Close", "currency", "number_of_markets_modeled", "number_of_markets_covered", "number_of_food_items"]
- `data/train.csv` (290113 bytes); columns: ["country", "iso3", "date", "Open", "High", "Low", "Close", "currency", "number_of_markets_modeled", "number_of_markets_covered", "number_of_food_items", "Inflation"]

## Public description

Global Food Price Inflation Forecasting (Monthly, Multi-Country)

Problem statement
Build a model that forecasts next-month food inflation rates across multiple countries using monthly OHLC (Open/High/Low/Close) food price indices and static country context. You must predict the Inflation value for each (country, iso3, date) pair in the test period.

Data description
Final files provided:
- train.csv: Historical rows with features and the target Inflation.
- test.csv: Rows for which you must predict Inflation (the target column is omitted).
- sample_submission.csv: Example of a valid submission format, containing placeholder predictions for the test rows.

Columns
- country: Country name.
- iso3: Three-letter country code.
- date: Monthly timestamp in ISO format (YYYY-MM-DD); typically the first day of the month.
- Open, High, Low, Close: Monthly OHLC values of the food price index for the country.
- currency: Country currency (categorical feature).
- number_of_markets_modeled: Static country attribute from the details file.
- number_of_markets_covered: Static country attribute from the details file.
- number_of_food_items: Static country attribute from the details file.
- Inflation: Target variable (present in train.csv only; absent from test.csv and required in submissions).

Train/test split
- Train window: All rows with available Inflation up to and including 2022-12 for each country.
- Test window: Rows from 2023-01 to the last available month in 2023 for each country, only where Inflation exists in the source data.
- There is no overlap between train and test. Keys are unique per (country, iso3, date).

Submission format
- A CSV file with exactly the following columns and rows in any order:
  - country, iso3, date, Inflation
- Each row must correspond to one row in test.csv (matching on country, iso3, date). The Inflation column should contain your numeric prediction.

Evaluation metric
- Primary metric: Macro-averaged sMAPE across countries.
  1) For each country, compute mean sMAPE over its test rows: sMAPE = 200 * mean(|y - y_hat| / (|y| + |y_hat|)), with the convention that if y = y_hat = 0 then the per-row sMAPE is 0.
  2) Average the per-country sMAPE values equally (macro-average) to obtain the final score. Lower is better.
- Rationale: sMAPE is scale-free and symmetric, handling both positive and negative inflation. Macro-averaging ensures that countries with more volatile series do not dominate the score, encouraging models that generalize across geographies.

Modeling guidance
- This is a time-series forecasting task. Do not leak future information.
- Useful approaches include lag features of OHLC series, rolling statistics (means/volatility), calendar features (month-of-year), and the static country context variables provided. Sequence models and gradient-boosted trees can both be effective when engineered properly.

File list to expect
- train.csv
- test.csv
- sample_submission.csv

Notes
- The provided files already exclude rows without observed Inflation.
- You may create any additional features from the provided columns during modeling. External data is allowed if consistent with Kaggle rules.
- All numeric values should be treated carefully to avoid NaN/Inf in your pipeline and predictions.
