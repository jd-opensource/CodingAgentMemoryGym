# OpenMLE-fast task

Task ID: `macro-economic-indicators-data@2`

Native metric: `MacroExcessReturnForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3651 bytes)
- `data/sample_submission.csv` (6389 bytes); columns: ["date", "target"]
- `data/test.csv` (27321 bytes); columns: ["date", "S&P Comp.", "Dividend", "Earnings", "Consumer Price Index CPI", "Date Fraction", "Long Interest Rate GS10", "Real Price", "Real Dividend", "Real Total Return Price", "Real Earnings", "Real TR Scaled Earnings", "Cyclically Adjusted Price Earnings Ratio P/E10 or CAPE", "Cyclically Adjusted Total Return Price Earnings Ratio TR P/E10 or TR CAPE", "Excess CAPE Yield", "Monthly Total Bond Returns", "Real Total Bond Returns"]
- `data/train.csv` (138773 bytes); columns: ["date", "S&P Comp.", "Dividend", "Earnings", "Consumer Price Index CPI", "Date Fraction", "Long Interest Rate GS10", "Real Price", "Real Dividend", "Real Total Return Price", "Real Earnings", "Real TR Scaled Earnings", "Cyclically Adjusted Price Earnings Ratio P/E10 or CAPE", "Cyclically Adjusted Total Return Price Earnings Ratio TR P/E10 or TR CAPE", "Excess CAPE Yield", "Monthly Total Bond Returns", "Real Total Bond Returns", "target"]

## Public description

Title: 10-Year Forward Real Equity–Bond Excess Return Forecasting

Problem statement
You are given a long-run monthly macro/market panel derived from Robert Shiller’s historical dataset (1871–present). For each month t, predict the 10-year forward real excess annualized return of equities over bonds at t:

target = (10Y annualized real stock return) − (10Y annualized real bond return)

The target is provided ex post in the data and is smooth but regime-dependent. Participants must build a model that, using only contemporaneous and lagged information (available at or before month t), forecasts this target for a held-out, chronologically later test period.

Data description
- Source file was standardized into two competition files:
  - train.csv: features plus the numeric regression target column named target
  - test.csv: the same feature columns as train.csv but without target; includes a date column used as row identifier
  - sample_submission.csv: two columns [date, target], matching the dates in test.csv

Feature space (columns may include, sanitized and consistently typed):
- date: month in YYYY-MM format (serves as identifier; do not drop)
- Market level/valuation: price indexes, real price, real total return price, earnings, dividends, CAPE (P/E10), TR CAPE, Excess CAPE Yield
- Macro/yields: CPI, long interest rate (e.g., GS10), monthly total bond returns, real total bond returns
- Other standardized real versions of price/earnings/dividends

The following forward-looking return columns are excluded from features and must not be engineered back in: any 10-year annualized stock/bond real return and their excess. Only the target in train.csv is the outcome to be predicted.

Files to use
- Training: train.csv (features + target)
- Testing: test.csv (features only)
- Submission format: sample_submission.csv provides the required column names and types. Your submission must have exactly two columns: date and target, with dates matching those in test.csv.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on the target values, computed in percentage points.
- Definition: RMSE = sqrt(mean((y_pred − y_true)^2)) over all rows in the test period.
- The evaluator validates the submission format, aligns rows on the date key, checks for finite numeric predictions, and then computes RMSE. Lower is better.

Important rules and notes
- Time awareness: construct features using only information available at or before t. Do not use any forward-looking labels or leak the target via engineered features.
- Scale and coverage: the split keeps the full viable history up to the start of the test period and a contiguous test block with fully realized 10-year labels. No subsampling is used.
- Nonstationarity: expect structural breaks and long-memory effects. Robust feature engineering (levels, changes, moving averages), regularization, and time-series cross-validation are recommended.

Baseline ideas (non-exhaustive)
- Linear/elastic-net models using valuation and yield levels/changes
- Gradient-boosted trees on engineered trend/momentum/valuation features
- State-space/Bayesian regression with time-varying coefficients
- GAMs or splines to model nonlinear valuation–return relationships

Submission
- Submit a CSV with columns [date, target] for all dates in test.csv. The target is a real number (percentage points annualized). Any extra columns or missing/extra rows will fail validation.

Reproducibility
- The provided preparation script deterministically standardizes the raw file, performs strict checks, and writes train.csv, test.csv, and sample_submission.csv aligned with this description.
