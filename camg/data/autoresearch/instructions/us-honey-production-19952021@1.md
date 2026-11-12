# OpenMLE-fast task

Task ID: `us-honey-production-19952021@1`

Native metric: `HoneyPriceForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3946 bytes)
- `data/sample_submission.csv` (3837 bytes); columns: ["state", "year", "average_price"]
- `data/test.csv` (5468 bytes); columns: ["state", "year", "prev_colonies_number", "prev_yield_per_colony", "prev_production", "prev_stocks"]
- `data/train.csv` (47838 bytes); columns: ["state", "year", "prev_colonies_number", "prev_yield_per_colony", "prev_production", "prev_stocks", "average_price"]

## Public description

Competition: Forecasting State-Level Honey Prices (US, 1996–2021)

Problem statement
Build a model to forecast the next-year average honey price (USD per pound) for each US state. Given historical state-level honey industry indicators, predict average_price for a fixed held-out period. Your predictions should be made using only information available up to the prior year for each target year.

What you need to predict
- Target: average_price (USD/lb) for each state-year in the test set.
- Horizon: one-year-ahead forecasts. For a given state and year t in the test set, you should use information from year t-1 and earlier.

Data description
You are provided pre-split files constructed from the USDA/NASS honey production panel:
- train.csv: Supervised learning table covering years 1996–2018. Each row corresponds to a (state, year) target with previous-year features. Columns:
  - state (string): US state identifier (categorical). Use as-is; no merging.
  - year (int): target year t for which the price is observed in train.
  - prev_colonies_number, prev_yield_per_colony, prev_production, prev_stocks (numeric): values from year t-1 in the same state.
  - average_price (float): the target price in USD for year t.
- test.csv: Rows for years 2019–2021 with the same schema as train.csv but without the average_price column. For each (state, year) in test, the prev_* columns are taken from year t-1 in the same state.
- sample_submission.csv: Example submission file aligned row-wise with test.csv, containing placeholder predictions for average_price.

Important unit note
The raw historical data spans multiple decades. To standardize units, average_price has been normalized to USD per pound via a simple, robust rule: if a recorded price value > 20, it is assumed to have been reported in cents and divided by 100. Otherwise, it is used as-is. All average_price values in train.csv and expected submissions are in USD.

Feature leakage policy
To avoid leakage, the provided features do not include any same-year statistics (e.g., production, stocks, yield for the target year) or previous-year price and value_of_production. You may create additional features from the provided prev_* variables and the state/year identifiers, but you cannot rely on unknown future data or derived price proxies.

Evaluation
Submissions are evaluated using Root Mean Squared Error (RMSE) on the natural log scale:
- Let y be the ground-truth average_price and y_hat be your prediction for the same row.
- Define y_clipped = max(y, 0.0) and y_hat_clipped = max(y_hat, 0.0).
- The score is RMSE(log(y_clipped + 1e-6), log(y_hat_clipped + 1e-6)). Lower is better.
This multiplicative-error view is robust to scale changes and treats relative error fairly across low- and high-price states.

Submission format
- CSV with the following columns and no header reordering:
  - state (string)
  - year (int)
  - average_price (float, USD)
- The (state, year) pairs must exactly match those in test.csv and appear exactly once. Extra/missing rows or duplicated pairs will be rejected.
- Predicted values must be finite real numbers (no NaN/Inf). Negative values are allowed by CSV but will be clipped to non-negative during evaluation; avoid negative predictions.

Recommended modeling approach (not required)
- Use the prev_* features and the state/year identifiers to engineer lags, differences, ratios, moving statistics (within the information set up to t-1), and interaction terms.
- Train a regression model (e.g., gradient boosted trees, random forests, regularized linear models) to map features to average_price.
- Validate with rolling or time-based splits (e.g., train up to 2012, validate on 2013–2015; then roll forward) to respect temporal ordering.

Files provided
- train.csv (supervised training data, 1996–2018)
- test.csv (features only, 2019–2021)
- sample_submission.csv (aligned with test.csv)

Good luck and happy modeling!
