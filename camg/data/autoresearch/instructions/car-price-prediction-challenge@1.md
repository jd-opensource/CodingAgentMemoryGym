# OpenMLE-fast task

Task ID: `car-price-prediction-challenge@1`

Native metric: `CarPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3294 bytes)
- `data/sample_submission.csv` (105439 bytes); columns: ["ID", "Price"]
- `data/test.csv` (419210 bytes); columns: ["ID", "Levy", "Manufacturer", "Model", "Prod. year", "Category", "Leather interior", "Fuel type", "Engine volume", "Mileage", "Cylinders", "Gear box type", "Drive wheels", "Doors", "Wheel", "Color", "Airbags"]
- `data/train.csv` (1761831 bytes); columns: ["ID", "Price", "Levy", "Manufacturer", "Model", "Prod. year", "Category", "Leather interior", "Fuel type", "Engine volume", "Mileage", "Cylinders", "Gear box type", "Drive wheels", "Doors", "Wheel", "Color", "Airbags"]

## Public description

Robust Used Car Price Prediction (RMSLE)

Problem statement
Build a model that predicts the market listing price of a used car from heterogeneous tabular attributes. Listings include mixed data types and occasional noisy or drifted values. Your task is to process the data, engineer meaningful features, train robust models, and generate accurate price predictions.

Data description
- Target: Price (continuous numeric).
- Identifier: ID (unique listing identifier).
- Predictors: Levy, Manufacturer, Model, Prod. year, Category, Leather interior, Fuel type, Engine volume, Mileage, Cylinders, Gear box type, Drive wheels, Doors, Wheel, Color, Airbags.
- Files provided:
  - train.csv: full training set with all predictors and the target column Price.
  - test.csv: test set with the same predictors (Price is withheld).
  - sample_submission.csv: a valid example submission with random but plausible predictions.

Important notes about the predictors
The predictors are intentionally realistic and somewhat messy:
- Numerics may appear as strings with units or punctuation (e.g., Mileage like "186005 km"; Engine volume like "2.0" or "2.0 Turbo").
- Categorical fields contain high cardinality (e.g., Model) and occasional drifted or unexpected tokens (e.g., Leather interior, Gear box type, Drive wheels, Doors, Wheel).
- Some values are missing or corrupted (e.g., Levy "-", Cylinders with non-numeric artifacts), and outliers exist in both features and target.
Participants are expected to design robust parsing, cleaning, and encoding strategies.

Recommended modeling approach (non-exhaustive)
- Data processing: standardize numeric fields, handle units, map anomalies to Unknown, and parse flags such as Turbo from Engine volume if desired.
- Feature engineering: age from Prod. year, engine displacement, interactions (e.g., Manufacturer × Category), robust scalers/winsorization where appropriate.
- Modeling: strong tabular methods (CatBoost/LightGBM/XGBoost, elastic nets, random forests), with careful CV (e.g., stratified on Price bins or grouped by Model to reduce overfitting).

Evaluation
- Metric: RMSLE (root mean squared log error) on Price using the standard +1 transform.
  - For true prices y and predictions p, score = sqrt(mean((log1p(y) − log1p(max(p, 0)))^2)).
  - RMSLE emphasizes relative error, which is appropriate for long-tailed price distributions, and is robust to a small number of extreme outliers.
- Submission format: a CSV with exactly two columns, in this order:
  - ID: the IDs from test.csv (each exactly once).
  - Price: your predicted price for each ID (non-negative; integer or float).

Data files for this competition
- train.csv
- test.csv
- sample_submission.csv

Baseline expectations
- A simple baseline using target log-transform and a gradient boosting model can achieve a reasonable RMSLE. Significant gains generally come from robust parsing/cleaning of mixed-type fields, high-cardinality encoding of Model, and careful validation to avoid leakage from near-duplicate listings.

Rules and tips
- Do not hardcode price based on ID or any other leakage-prone artifact.
- Ensure your preprocessing is applied identically to train and test.
- Validate your submission file format before submission to avoid penalties due to file errors.
