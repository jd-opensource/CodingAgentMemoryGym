# OpenMLE-fast task

Task ID: `gold-rates-1985-jan-2022@2`

Native metric: `GoldVolatilityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/annual.csv` (2523 bytes); columns: ["year", "USD", "EUR", "GBP", "INR", "AED", "CNY"]
- `data/description.txt` (3652 bytes)
- `data/prices.csv` (572059 bytes); columns: ["date", "USD", "EUR", "GBP", "INR", "AED", "CNY"]
- `data/sample_submission.csv` (55658 bytes); columns: ["row_id", "rv10"]
- `data/test.csv` (47001 bytes); columns: ["row_id", "date", "currency"]
- `data/train.csv` (2978700 bytes); columns: ["row_id", "date", "currency", "rv10"]

## Public description

Competition: Multi-currency 10‑day Realized Volatility Forecasting

Problem statement
Participants must predict the next 10-day realized volatility of daily log returns for gold prices denominated in six currencies (USD, EUR, GBP, INR, AED, CNY). For each (base date, currency) pair in the test set, the target is the square-root of the sum of squared daily log returns over the next 10 trading days after the base date. The task spans decades of history and multiple exchange-rate regimes, demanding careful feature engineering and robust forecasting models.

Data description
You are provided with:
- train.csv: Training samples with columns [row_id, date, currency, rv10]. Each row represents a base date and a currency, and rv10 is the 10-day forward realized volatility label for that currency at that base date.
- test.csv: Test samples with columns [row_id, date, currency] for which you must predict rv10.
- prices.csv: Daily gold prices per troy ounce for the six currencies with columns [date, USD, EUR, GBP, INR, AED, CNY]. This file is truncated to include history only up to the last base date in test to prevent target leakage. Use this to engineer features.
- annual.csv: Annual average gold prices per currency by calendar year. This is optional auxiliary context you may use to engineer macro/regime features (ensure causality in your features).
- sample_submission.csv: Correct submission format with placeholder predictions.

Target definition
For a given base date t and currency c with daily prices P_{t,c}, define the daily log return as r_{t,c} = log(P_{t,c} / P_{t-1,c}). The 10-day forward realized volatility RV10_{t,c} is
RV10_{t,c} = sqrt( sum_{i=1..10} r_{t+i,c}^2 ).
We do not annualize RV10; any scaling you apply in modeling should be internally consistent between train and test.

Train/test split
- Training base dates end on 2022-09-06 (inclusive).
- Test base dates run from 2022-09-07 to 2023-09-06 (inclusive).
- All currencies appear in both train and test; a row is included only if all 10 forward daily returns exist for that currency.

Submission format
- A single CSV file with columns: [row_id, rv10]
- row_id must match exactly the row_id values in test.csv.
- rv10 must be non-negative real numbers. Use reasonable numeric precision.

Evaluation
Primary metric: RMSE of log-volatility, aggregated date-first, then across the full test set. For each test base date, compute the mean squared error across available currencies on the log scale, then average those date-wise MSEs and take the square root:
RMSE = sqrt( mean_over_dates( mean_over_currencies( ( log(y_pred + eps) - log(y_true + eps) )^2 ) ) ), with eps = 1e-8.

Tie-breaker: sMAPE on RV10 values, aggregated in the same date-first manner:
sMAPE = mean_over_dates( mean_over_currencies( 2 * |y_pred - y_true| / ( |y_pred| + |y_true| + eps ) ) ).

Notes and guidance
- Use prices.csv to build features such as rolling realized volatility (e.g., 5/10/20/60-day), lagged squared returns, level–volatility interactions, calendar features, and cross-currency signals.
- annual.csv can provide slow-moving context (e.g., deviations from within-year averages) but must be used causally (do not leak information from future dates).
- Missing prices occur in early periods for some currencies; the provided train/test splits exclude base dates where a 10-day label cannot be formed.
- All dates are trading days as present in prices.csv; align your features accordingly.

Deliverable
Submit a CSV named however you like, containing [row_id, rv10]. The leaderboard uses the primary RMSE metric; the tie-breaker sMAPE applies only to exact ties in RMSE.
