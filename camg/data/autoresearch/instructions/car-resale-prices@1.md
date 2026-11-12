# OpenMLE-fast task

Task ID: `car-resale-prices@1`

Native metric: `CarResalePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3682 bytes)
- `data/sample_submission.csv` (98943 bytes); columns: ["id", "resale_price"]
- `data/test.csv` (531300 bytes); columns: ["id", "full_name", "registered_year", "engine_capacity", "insurance", "transmission_type", "kms_driven", "owner_type", "fuel_type", "max_power", "seats", "mileage", "body_type", "city"]
- `data/train.csv` (2255136 bytes); columns: ["id", "full_name", "registered_year", "engine_capacity", "insurance", "transmission_type", "kms_driven", "owner_type", "fuel_type", "max_power", "seats", "mileage", "body_type", "city", "resale_price"]

## Public description

India Used-Car Resale Price Prediction (2023)

Problem statement
Predict the resale price (in Indian Rupees, INR) of a used car listing given its attributes at the time of sale. The data reflects real marketplace noise: mixed units, missing values, duplicates, and heterogeneous categories across brands, model years, cities, body types, fuel/transmission types, and more.

Files provided
- train.csv: Training data with features and the target column resale_price (numeric INR).
- test.csv: Test data with the same feature columns as train.csv except without the target.
- sample_submission.csv: Example submission file with the expected format.

Target and features
- Target
  - resale_price: Numeric price in INR in train.csv. This column does not exist in test.csv.
- Features (columns may include messy strings, missing values, and mixed units; they are intentionally left raw to encourage robust preprocessing):
  - id: Unique identifier for each listing
  - full_name: Name of the car along with model and variant
  - registered_year: Year the car was registered
  - engine_capacity: Engine displacement (e.g., "1197 cc")
  - insurance: Insurance type/status
  - transmission_type: Transmission type
  - kms_driven: Total kilometers driven (e.g., "1,20,000 Kms")
  - owner_type: Ownership count/category (e.g., First Owner, Second Owner)
  - fuel_type: Fuel type
  - max_power: Peak power (e.g., "83.1bhp")
  - seats: Number of seats
  - mileage: Mileage (e.g., "21.4 kmpl")
  - body_type: Body configuration
  - city: City of sale

Important characteristics and recommended preprocessing
- Units and formatting: Features such as engine_capacity, kms_driven, max_power, and mileage are strings with units and Indian digit grouping. They should be parsed into numeric features when appropriate.
- Categorical richness: full_name implicitly contains brand/model information and often complements fuel_type, body_type, and city. Consider extracting brand/model/variant tokens and using encoders (e.g., target encoding, frequency encoding, or one-hot for frequent categories).
- Temporal/usage effects: registered_year can be transformed into vehicle_age. Combine with kms_driven to derive usage intensity (e.g., km_per_year).
- Outliers and missing values: Expect heavy tails in price and missing or inconsistent entries. Robust preprocessing and loss functions help.
- Duplicates: Splits are group-aware to avoid duplicate leakage across train/test.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on the price in INR.
  - For true prices y and predictions p, RMSLE = sqrt(mean((log1p(p) - log1p(y))^2)).
  - Predictions must be non-negative; negative values will be clipped to zero during evaluation.
  - RMSLE emphasizes proportional accuracy and is robust to the heavy-tailed nature of car prices.

Submission format
- A CSV file with exactly two columns and N rows, where N equals the number of rows in test.csv:
  - id: Integer identifiers matching those in test.csv
  - resale_price: Predicted numeric prices in INR for each id

Data scale
- Use all provided rows. The dataset retains broad brand/model/city coverage to encourage generalization. No subset or down-sampling is used.

Tips for strong performance
- Parse units carefully (Lakh/Crore, kmpl, bhp, cc, Kms with Indian digit grouping).
- Engineer domain features (age, km_per_year, power_per_liter, interactions like fuel×transmission or city×body_type).
- Consider modeling log(resale_price + 1) and converting back.
- Use robust tree-based models or regularized linear models with appropriate encodings.

Final file names for this competition
- train.csv
- test.csv
- sample_submission.csv
