# OpenMLE-fast task

Task ID: `trends-product-coffee-shop-sales-revenue-dataset@2`

Native metric: `CoffeeRevenueForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3490 bytes)
- `data/sample_submission.csv` (60012 bytes); columns: ["transaction_date", "hour", "store_location", "target_revenue"]
- `data/test.csv` (36127 bytes); columns: ["transaction_date", "hour", "store_location"]
- `data/train.csv` (219925 bytes); columns: ["transaction_date", "hour", "store_location", "target_revenue"]
- `data/transactions_train.csv` (10510471 bytes); columns: ["transaction_id", "transaction_date", "transaction_time", "transaction_qty", "store_id", "store_location", "product_id", "unit_price", "product_category", "product_type", "product_detail"]

## Public description

Maven Roasters: Hourly Revenue Forecasting Challenge

Problem statement
Using historical transaction-level data from three NYC coffee shops between 2023-01-01 and 2023-05-31, predict hourly revenue for each store for 2023-06-01 to 2023-06-30. The forecasting horizon covers hours 06:00–20:00 inclusive (15 hours per day) for each store.

You must aggregate raw transactions into hourly revenue and build a forecasting model that captures intraday and weekly seasonality, store heterogeneity, and price/mix effects.

Files provided
- train.csv: Hourly aggregated training targets.
  - Columns: transaction_date, hour, store_location, target_revenue
- test.csv: Hourly keys (no labels) for the June forecast horizon.
  - Columns: transaction_date, hour, store_location
- sample_submission.csv: Example submission with randomized but valid target values.
  - Columns: transaction_date, hour, store_location, target_revenue
- transactions_train.csv: Raw transaction-level data for 2023-01-01 to 2023-05-31 only (same schema as the original source) to enable feature engineering without leakage.

Target definition
- target_revenue = sum(transaction_qty × unit_price) aggregated by (transaction_date, hour, store_location), for hours 06:00–20:00 inclusive.
- Hours without transactions in the source data are present with target_revenue = 0 in the training set. The test set provides all store × day × hour keys in the horizon.

Submission format
- Submit a single CSV with the following columns and exact names: transaction_date (YYYY-MM-DD), hour (integer 6–20), store_location (string), target_revenue (non-negative float).
- Every row in test.csv must appear exactly once in your submission; no extra/missing rows or duplicates are allowed.

Evaluation metric
Revenue-weighted seasonal MASE (mean absolute scaled error):
1) For each store and hour h (6–20), form the training-time series y_{d,h} from train.csv (d = training dates) and compute the scaling factor as the mean absolute seasonal difference |y_{d,h} − y_{d−7,h}| over the training window where d−7 exists. If this factor is zero/undefined, a safe fallback based on the mean absolute level is used.
2) For the test window (June), compute the mean absolute error (MAE) for each store–hour series between your predictions and the ground truth.
3) Divide each series’ MAE by its training seasonal factor to obtain MASE.
4) Average MASE across hours within each store, then average across stores using weights proportional to each store’s total training revenue.

Why this metric?
- Scale-free and comparable across stores/hours.
- Weekly seasonal scaling matches the business cadence.
- Revenue weighting emphasizes business impact while preserving fairness across stores.

Modeling guidance (optional)
Participants are encouraged to engineer features such as:
- Calendar: day-of-week, weekend flags, month, week-of-year.
- Intraday structure: hour-of-day, lagged and rolling statistics at the same hour (7/14/28-day means, std, last value), preceding-hour carryover.
- Price/mix signals from transactions_train.csv: store × hour average unit_price by category, category share dynamics, price-change flags.
A range of methods are viable (e.g., gradient boosting, GLMs, Prophet/TBATS, RNN/TCN/TFT) as long as no information from June labels is used.

Deliverables
- Submit a CSV following the specified format. The leaderboard will use the described metric evaluated against the hidden ground truth for June.
