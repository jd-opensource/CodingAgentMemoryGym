# OpenMLE-fast task

Task ID: `walmart-store-sales@2`

Native metric: `WalmartSalesQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2525 bytes)
- `data/sample_submission.csv` (33863 bytes); columns: ["Store", "Date", "quantile_0.1", "quantile_0.5", "quantile_0.9"]
- `data/test.csv` (26494 bytes); columns: ["Store", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
- `data/train.csv` (325132 bytes); columns: ["Store", "Date", "Weekly_Sales", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]

## Public description

Competition: Probabilistic multi-store weekly sales forecasting

Problem statement
- Forecast calibrated predictive quantiles of Walmart Weekly_Sales for every store over the final 13 weeks in the panel. Your model may use all earlier weeks and the provided covariates.

Data
- Columns: Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment.
- Date is weekly and formatted dd-mm-yyyy. The panel is balanced across stores and weeks.

Files provided
- train.csv: full historical data for the training horizon (includes Weekly_Sales).
- test.csv: the forecasting horizon with all covariates but without Weekly_Sales.
- sample_submission.csv: valid example showing the expected submission structure.

Target and features
- Target: Weekly_Sales (to be forecast for the test horizon).
- Example features (you may engineer others):
  - Calendar: week-of-year, month, quarter, year, holiday flags, days-since/until-holiday.
  - Dynamics within store: lags (1, 2, 4, 52 weeks), rolling mean/std/min/max, trend.
  - Macroeconomic: Fuel_Price, CPI, Unemployment.
  - Weather proxy: Temperature.

Train/test split
- Sort unique dates ascending across the full panel.
- Train horizon: first 130 weeks.
- Test horizon: last 13 weeks.
- All stores appear in both horizons; covariates for test weeks are included in test.csv.

Submission format
- CSV with columns (exact names and order):
  - Store (integer)
  - Date (string dd-mm-yyyy)
  - quantile_0.1, quantile_0.5, quantile_0.9 (floats)
- The (Store, Date) keys, their order, and Date strings must exactly match test.csv (sorted by Store ascending, then Date ascending).
- Tip: Ensure quantile monotonicity (q10 ≤ q50 ≤ q90) to avoid unnecessary pinball loss; it’s not enforced but recommended.

Evaluation metric
- Mean pinball loss averaged per store and across quantiles q ∈ {0.1, 0.5, 0.9}. Lower is better.
  - For true y and prediction y_q at quantile q, pinball(y, y_q, q) = max(q · (y − y_q), (q − 1) · (y − y_q)).
  - For each store, average pinball over all its test weeks and the three quantiles; then take the mean across stores with equal weight. This prevents large stores from dominating and rewards calibrated uncertainty.

Notes
- Parse Date with dayfirst semantics (dd-mm-yyyy).
- Handle numeric values carefully and avoid NaN/Inf in predictions.
- Any ML approach is allowed (e.g., quantile regression with linear/GBM/forest models, distributional forests, sequence models) as long as the submission format is respected.
