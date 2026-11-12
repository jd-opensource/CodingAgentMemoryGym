# OpenMLE-fast task

Task ID: `macro-economic-indicators-data@1`

Native metric: `MacroReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3409 bytes)
- `data/sample_submission.csv` (6636 bytes); columns: ["row_id", "next_month_real_total_return"]
- `data/test.csv` (34147 bytes); columns: ["row_id", "date", "s_p_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns"]
- `data/train.csv` (208137 bytes); columns: ["row_id", "date", "s_p_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns", "next_month_real_total_return"]

## Public description

Title: 1-Month Ahead Real Total Return Forecasting (Shiller Macro Data)

Problem statement:
Given monthly U.S. market and macroeconomic indicators at month t, predict the next-month real total return of the U.S. equity market, defined as r_{t+1} = RealTRPrice_{t+1}/RealTRPrice_t - 1. The task is challenging due to regime shifts, heavy tails, and long historical span, requiring careful preprocessing, feature engineering, and robust modeling.

What you need to do:
- Use the provided monthly time-series features (valuation, earnings/dividends, CPI, long rates, real prices, bond returns, etc.) available up to and including month t.
- Build a model that outputs a point prediction for r_{t+1} for each row in the test set.
- Engineer features such as lags, differences, rolling statistics, spreads, term-structure or inflation momentum, provided you only use information available up to month t for each forecast.

Files provided:
- train.csv: Training set with features and the target column next_month_real_total_return.
- test.csv: Test set with features only. You must predict next_month_real_total_return for each row.
- sample_submission.csv: Example submission file showing the required format.

Data description (columns):
- date: Monthly timestamp (YYYY-MM) for month t.
- row_id: Unique row identifier used to align predictions with the test set.
- Feature columns: Cleaned numeric versions of macro and market indicators, including but not limited to: S&P price level, dividend, earnings, CPI, 10-year Treasury yield, real price, real dividend, real total return price, real earnings, CAPE, total-return CAPE, excess CAPE yield, monthly total bond returns, real total bond returns. Empty columns and forward-looking 10-year realized return columns are removed.
- Target (train.csv only): next_month_real_total_return = (Real Total Return Price at t+1 / Real Total Return Price at t) - 1, expressed in decimal units (e.g., 0.012 = 1.2%).

Train/test split:
- Chronological split to preserve causality.
- Train: from the start of the series up to 1999-12 (inclusive), rows with valid labels only.
- Test: from 2000-01 to the latest month with a valid next-month label. Each test row has a corresponding ground-truth label used for scoring.

Submission format:
- CSV with two columns and header:
  - row_id: exactly matches the row_id values in test.csv
  - next_month_real_total_return: your predicted decimal return for the next month
- Do not reorder, duplicate, or drop IDs. No extra columns are allowed.

Evaluation metric:
- Mean Absolute Error (MAE) in percentage points, computed as mean(abs(100 × (y_pred − y_true))). Numerically equivalent to MAE on decimal returns scaled by 100. Lower is better.

Important notes and constraints:
- Use only information available up to and including month t for each forecast. Do not use any forward-looking realized return fields or information dependent on t+1 or beyond.
- This is a long historical time series with structural changes (inflation regimes, crises). Proper cleaning (NAs, numeric coercion, column normalization) and robust validation are essential.
- You may use any ML method (e.g., regularized regression, tree ensembles, gradient boosting, state-space models, neural time series). Strong feature engineering and evaluation practice are encouraged.

Final files for this competition:
- train.csv
- test.csv
- sample_submission.csv
