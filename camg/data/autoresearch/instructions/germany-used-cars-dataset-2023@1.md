# OpenMLE-fast task

Task ID: `germany-used-cars-dataset-2023@1`

Native metric: `UsedCarPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2869 bytes)
- `data/sample_submission.csv` (1252657 bytes); columns: ["row_id", "price_in_euro"]
- `data/test.csv` (6828579 bytes); columns: ["brand", "model", "color", "registration_date", "year", "power_kw", "power_ps", "transmission_type", "fuel_type", "fuel_consumption_l_100km", "fuel_consumption_g_km", "mileage_in_km", "offer_description", "row_id"]
- `data/train.csv` (28881934 bytes); columns: ["brand", "model", "color", "registration_date", "year", "power_kw", "power_ps", "transmission_type", "fuel_type", "fuel_consumption_l_100km", "fuel_consumption_g_km", "mileage_in_km", "offer_description", "price_in_euro", "row_id"]

## Public description

Germany Used Car Price Prediction (AutoScout24 1995–2023)

Problem statement
You are given real-world listings of used car offers in Germany spanning models from 1995–2023. Each listing contains technical specifications, categorical attributes, mileage, fuel consumption, transmission and fuel type, exterior color, and a free-text offer description. Your goal is to build a model that predicts the asking price in euros for each listing.

Files provided
- train.csv: Training data with features, the target price_in_euro, and a row_id identifier.
- test.csv: Test data with the same features and a row_id identifier; price_in_euro is withheld.
- sample_submission.csv: Example submission showing the required format.

Target and features
- Target (train.csv only): price_in_euro
- Identifier (both train.csv and test.csv): row_id (do not use as a predictive feature)
- Features (present in both train.csv and test.csv):
  brand, model, color, registration_date, year, power_kw, power_ps, transmission_type, fuel_type, fuel_consumption_l_100km, fuel_consumption_g_km, mileage_in_km, offer_description
- Note: Numeric fields may appear as strings with German-style formatting and units (e.g., "8,9 l/100 km", "210 g/km"). Handle parsing as you see fit. An index-like column present in the raw source has been removed.

Submission format
- Submit a CSV file with exactly these columns:
  - row_id: Identifier matching each row in test.csv, in the same order as test.csv
  - price_in_euro: Your non-negative prediction for that row
- The set and order of row_id must match test.csv exactly. Include a header row. Do not include extra columns.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on price_in_euro.
- Definition: For N test rows with predictions p_i and true prices y_i,
  RMSLE = sqrt( (1/N) * sum_i ( log(1 + p_i) − log(1 + y_i) )^2 ).
- Rationale: Prices are heavy-tailed with outliers. RMSLE measures relative error and stabilizes scale, yielding fair and robust comparisons.

Train/test split details
- A single deterministic split is provided. The split preserves distribution by stratifying on brand and registration year extracted from registration_date (MM/YYYY), with randomization inside strata.
- All test rows have strictly positive labels, and brands present in test also occur in train.

Hints and expectations
- Parsing and normalization are crucial: convert German-formatted numbers (e.g., decimal commas) and strip units where helpful.
- Text in offer_description can provide valuable signals via TF-IDF or embeddings.
- Handle missing values and artifacts robustly (e.g., placeholders like "- (g/km)").
- Strong performance typically requires careful feature engineering (e.g., interactions across brand, model, year, mileage) and appropriate modeling (e.g., gradient-boosted trees, regularized linear models, stacking).
