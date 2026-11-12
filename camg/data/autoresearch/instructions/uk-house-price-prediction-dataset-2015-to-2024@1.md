# OpenMLE-fast task

Task ID: `uk-house-price-prediction-dataset-2015-to-2024@1`

Native metric: `UKHousePriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2607 bytes)
- `data/sample_submission.csv` (428406 bytes); columns: ["row_id", "price"]
- `data/test.csv` (1635459 bytes); columns: ["date", "postcode", "property_type", "new_build", "freehold", "street", "locality", "town", "district", "county", "row_id"]
- `data/train.csv` (6650136 bytes); columns: ["price", "date", "postcode", "property_type", "new_build", "freehold", "street", "locality", "town", "district", "county"]

## Public description

UK Price Paid Prediction (2015–2024)

Problem statement
Predict the final sale price of a UK residential property at the time of transaction using tabular attributes capturing time, location, property type, tenure, and build status. You will train on historical transactions and produce predictions for an unseen test set.

Files provided
- train.csv: Labeled training data with features and the target column price.
- test.csv: Unlabeled test data with the same features as train.csv plus a row_id column for submission alignment.
- sample_submission.csv: A valid example submission with random predictions for the test set row_id values.

Target
- price: Sale price in GBP (strictly positive).

Features
- date: ISO date of transaction (YYYY-MM-DD).
- postcode: Full UK postcode (e.g., SW1A 1AA).
- property_type: Property type code among {D, S, T, F, O}.
- new_build: Whether the property was newly built at sale time {Y, N}.
- freehold: Tenure type {F (Freehold), L (Leasehold)}.
- street, locality, town, district, county: Location hierarchy text fields.

Recommended feature engineering (optional)
- Temporal: year, month, quarter, day-of-week, seasonality encodings.
- Geography: outward code (e.g., SW1A), district/sector extraction; regularized target/count encodings; hashing for high-cardinality fields.
- Target transform: log1p(price) for modeling heavy-tailed prices.

Evaluation
- Root Mean Squared Log Error (RMSLE) on price.
  - log1p is applied to both ground truth and predictions.
  - Lower is better.

Submission format
- CSV with exactly two columns in this order:
  - row_id: integer identifiers provided in test.csv.
  - price: non-negative predicted price in GBP for each row_id.
- Your row_id set must exactly match test.csv; no missing or extra rows.

Rules and notes
- Use only the provided training data for supervised learning. External data is allowed only if it’s publicly available and equally accessible to all participants.
- Do not leak labels by engineering features directly from the test set labels (which are not provided).
- Prices are heavy-tailed and vary strongly by region and year; robust encoding and regularization are essential.

Baseline ideas
- Gradient boosting trees with careful categorical encoding (e.g., CatBoost, target encoding with CV, count encoders).
- Time-aware validation (e.g., stratified by year and property_type) to mimic the competition split.

Data integrity
- All fields are non-missing and represent information available at transaction time.
- The host split preserves (year, property_type) distributions between train and test.
