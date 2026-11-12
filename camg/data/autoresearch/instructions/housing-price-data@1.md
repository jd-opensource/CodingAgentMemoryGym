# OpenMLE-fast task

Task ID: `housing-price-data@1`

Native metric: `HousingPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2294 bytes)
- `data/sample_submission.csv` (2734 bytes); columns: ["Id", "price"]
- `data/test.csv` (5848 bytes); columns: ["Id", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus"]
- `data/train.csv` (25246 bytes); columns: ["Id", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus", "price"]

## Public description

Title: Robust Housing Price Prediction (RMSLE)

Problem statement
Build an automated valuation model to predict residential property sale prices from tabular attributes. Each row represents a home with features describing size, rooms, amenities, and neighborhood preference flags. Your task is to estimate the price for the properties in the test set.

Files provided
- train.csv: Feature columns and the target column price for training.
- test.csv: The same feature columns as train.csv plus an Id column; price is withheld.
- sample_submission.csv: Example submission file with Id and price columns.

Target and features
- Target: price (continuous, strictly positive)
- Features: area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus
- Id: unique integer identifier for each row in test.csv (also present in train.csv for convenience).

Data characteristics and modeling hints
- Price distribution is skewed; robust modeling (log-transformations, quantile losses, or ensembles) may help.
- Categorical features include several binary yes/no attributes and furnishingstatus (unfurnished, semi-furnished, furnished). Encode them appropriately.
- Consider interaction features (e.g., amenity counts, area per bedroom/bathroom, effects of mainroad with airconditioning/furnishingstatus).
- Handle potential missing values and outliers defensively.
- Leverage cross-validation and careful preprocessing to avoid overfitting.

Evaluation metric
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE):
RMSLE = sqrt(mean((log(1 + y_pred) - log(1 + y_true))^2))
- y_pred must be finite real numbers; negative predictions are clipped to 0 before scoring.
- Lower RMSLE indicates better performance and rewards accurate proportional errors across price ranges.

Submission format
- A single CSV file with exactly two columns: Id, price.
- Include a prediction for every Id in test.csv; no extras, no duplicates.
- price must be numeric, finite, and non-negative.

Notes on the split
- The train/test split is deterministic and stratified by price bins and furnishingstatus to preserve distribution and ensure a challenging, fair evaluation.
- All data is included; there is no runtime constraint.
