# OpenMLE-fast task

Task ID: `house-price-prediction-seattle@1`

Native metric: `SeattleHousePriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2867 bytes)
- `data/sample_submission.csv` (7079 bytes); columns: ["Id", "price"]
- `data/test.csv` (19753 bytes); columns: ["Id", "beds", "baths", "size", "size_units", "lot_size", "lot_size_units", "zip_code"]
- `data/train.csv` (95902 bytes); columns: ["Id", "beds", "baths", "size", "size_units", "lot_size", "lot_size_units", "zip_code", "price"]

## Public description

Seattle House Price Prediction (RMSLE)

Problem statement
You are given real sales of residential properties in Seattle, Washington (Aug–Dec 2022). Your task is to build a model that predicts the final sale price (USD) from structural attributes and a location proxy (ZIP code). The leaderboard is scored on log-price accuracy, encouraging well-calibrated predictions across a wide price range.

Files provided
- train.csv: Labeled training data. Columns: Id, beds, baths, size, size_units, lot_size, lot_size_units, zip_code, price.
- test.csv: Unlabeled test data. Columns: Id, beds, baths, size, size_units, lot_size, lot_size_units, zip_code.
- sample_submission.csv: Example submission with valid format. Columns: Id, price.

Target
- price: final sale price in US dollars (positive real number).

Feature description
- beds: Number of bedrooms in the property.
- baths: Number of bathrooms in the property. Note: 0.5 indicates a half bath.
- size: Interior floor area of the property.
- size_units: Units for size. In this dataset it is consistently "sqft".
- lot_size: Total area of the land parcel on which the property sits.
- lot_size_units: Units for lot_size. Values include "sqft", "acre", or missing.
- zip_code: USPS ZIP code for the property.

Recommendations and important notes
- Units: If you use lot_size, convert acres to square feet using 1 acre = 43,560 sqft. Consider retaining a flag for original unit type and missingness.
- Missing values: Some rows have missing lot_size and/or lot_size_units. Handle missingness explicitly rather than dropping rows.
- Target skew: Prices are highly skewed with large outliers. Modeling and/or evaluating in log space is beneficial.
- Categorical encoding: Treat zip_code as categorical; use appropriate encoders (e.g., one-hot, target, or impact encoding with leakage-safe CV).
- Validation: ZIP codes differ in price levels. Consider grouped or stratified CV by zip_code to obtain reliable validation.

Evaluation metric
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the true prices:
- For each property i, compute e_i = log(1 + y_pred_i) − log(1 + y_true_i)
- RMSLE = sqrt(mean(e_i^2))

Rules for submissions
- File format: CSV with columns exactly: Id, price. The Ids must match those in test.csv.
- Values: price predictions must be finite numbers and >= 0. Avoid NaN/Inf.
- Row count: The number of rows must equal the number of rows in test.csv.

What makes this challenge interesting
- Real, recent transactions from Seattle.
- Heterogeneous markets across many ZIP codes, including distribution shifts.
- Practical data quirks: unit conversion, missingness, skew, and outliers.
- Solvable with a range of tabular ML techniques (e.g., tree ensembles, GLMs, CatBoost, tabular neural nets) with thoughtful preprocessing and validation.
