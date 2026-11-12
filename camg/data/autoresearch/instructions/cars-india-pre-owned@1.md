# OpenMLE-fast task

Task ID: `cars-india-pre-owned@1`

Native metric: `UsedCarPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3797 bytes)
- `data/sample_submission.csv` (11290 bytes); columns: ["id", "price"]
- `data/test.csv` (78754 bytes); columns: ["id", "brand", "model", "transmission", "make_year", "reg_year", "fuel_type", "engine_capacity(CC)", "km_driven", "ownership", "has_insurance", "spare_key", "reg_number", "title"]
- `data/train.csv` (314590 bytes); columns: ["id", "brand", "model", "transmission", "make_year", "reg_year", "fuel_type", "engine_capacity(CC)", "km_driven", "ownership", "has_insurance", "spare_key", "reg_number", "title", "price"]

## Public description

Used Car Price Prediction (India)

Problem statement
Predict the asking price of a pre-owned car in India using structured listing attributes and short text descriptions. The data spans diverse brands, models, fuel types, transmissions, ownership histories, usage, and registration regions, leading to rich non-linear interactions and a highly skewed price distribution.

Files provided
- train.csv: Training set with features and the target column price.
- test.csv: Test set with the same features as train.csv, without the price column.
- sample_submission.csv: Example submission file with the correct format and randomly generated valid predictions.

Target
- price: Asking price of the car listing (numeric, non-negative, Indian Rupees).

Input features (columns)
You will receive the following columns in train.csv and test.csv:
- id: Unique identifier for each listing (string). This has no predictive meaning and is included for submission merging.
- brand, model: Car brand and model (categorical, high cardinality for model).
- transmission: Manual/Automatic or similar labels (categorical; normalize as needed).
- make_year: Year the car was manufactured (integer).
- reg_year: Date string for first registration (e.g., "01-07-2018"). Parse the year if helpful.
- fuel_type: Petrol/Diesel/CNG/Electric etc. (categorical).
- engine_capacity(CC): Displacement in cubic centimeters (numeric, may be missing for some rows).
- km_driven: Odometer reading in kilometers (numeric).
- ownership: Ownership tier such as "1st owner", "2nd owner" (categorical; potential ordinal meaning).
- has_insurance: TRUE/FALSE flag (string indicator).
- spare_key: Yes/No (string indicator).
- reg_number: Vehicle registration code (string; early characters can proxy state/region).
- title: Short listing title (text; may contain trim/features like CVT, AMT, Turbo, etc.).

Notes
- The column overall_cost is intentionally excluded from train/test files to avoid target leakage.
- All rows in the original dataset are used; runtime constraints are not a concern.

Evaluation metric
Root Mean Squared Logarithmic Error (RMSLE) on price.
- For each listing i with true price y_i and predicted price p_i, we compute:
  RMSLE = sqrt( mean( (log(1 + clip(p_i, lower=0)) - log(1 + y_i))^2 ) )
- RMSLE treats proportional errors consistently across low- and high-priced cars and is robust to the heavy right tail of prices. Predictions are clipped at zero for scoring to avoid issues with negative values.

Submission format
- CSV with two columns and a header: id,price
- One row per id present in test.csv.
- The price column must be numeric. Non-finite values (NaN/inf) are not allowed.

Recommended approach (non-exhaustive)
- Data processing: Normalize categorical labels; parse reg_year to extract year; keep unknowns rather than dropping rows; robustly impute missing engine_capacity(CC).
- Feature engineering (optional):
  - age_at_registration = parse_year(reg_year) - make_year
  - usage_intensity = km_driven / max(1, age_at_registration)
  - region_code from reg_number prefix (e.g., DL, HR, UP)
  - text signals from title via keywords or TF-IDF
- Modeling: Gradient boosting trees, regularized linear models with target encoding for high-cardinality features, or tabular neural networks. Train on log(price) if your model benefits from it.
- Validation: Consider K-fold CV with brand-aware or stratified folds (price bins × brand) to better assess generalization.

Train/test split details
- A single deterministic split is used: approximately 75% train and 25% test.
- Stratification is applied jointly by brand and price quantile bins to stabilize distributions.

Goal
Build models that generalize across brands/models/regions and price ranges while minimizing RMSLE on the hidden test labels.
