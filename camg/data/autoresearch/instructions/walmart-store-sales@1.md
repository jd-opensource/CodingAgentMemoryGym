# OpenMLE-fast task

Task ID: `walmart-store-sales@1`

Native metric: `WalmartSalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2546 bytes)
- `data/sample_submission.csv` (18838 bytes); columns: ["Store", "Date", "Weekly_Sales"]
- `data/test.csv` (26494 bytes); columns: ["Store", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
- `data/train.csv` (325132 bytes); columns: ["Store", "Date", "Weekly_Sales", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]

## Public description

Walmart Multi-Store Weekly Sales Forecasting (13-week horizon)

Problem statement
- You are given a complete weekly panel of 45 Walmart stores across 143 consecutive weeks. Each row corresponds to a (Store, Date) pair with covariates such as holiday flag, temperature, fuel price, CPI, and unemployment. Your task is to predict Weekly_Sales for the final 13 weeks for every store.
- This is a point-forecasting regression task on panel time series. All covariates for the forecast horizon are provided; you only need to predict Weekly_Sales.

Data description
- train.csv: Historical records for the first 130 consecutive weeks for all stores.
  - Columns: Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment
  - Date is in dd-mm-yyyy format. Rows are sorted by Store then Date.
- test.csv: Input rows for the final 13 consecutive weeks for all stores. Weekly_Sales is withheld.
  - Columns: Store, Date, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment
- sample_submission.csv: Example submission, containing the same (Store, Date) keys as test.csv and a numeric Weekly_Sales column with randomly generated values for illustration.

Submission format
- Submit a single CSV with exactly these columns in this order:
  - Store, Date, Weekly_Sales
- Requirements:
  - The (Store, Date) key set must match test.csv exactly (order does not matter, no duplicates).
  - Date strings must be formatted as dd-mm-yyyy to match test.csv.
  - Weekly_Sales must be numeric and finite.
  - For reference, there are 45 stores and 13 weeks in the test horizon (45 × 13 = 585 rows).

Evaluation
- Metric: Symmetric Mean Absolute Percentage Error (sMAPE), averaged over all test rows (lower is better).
  - For each row i with actual Ai and forecast Fi:
    sMAPE_i = 200 * |Fi - Ai| / (|Fi| + |Ai| + epsilon)
  - The final score is the mean of sMAPE_i over all test rows. We use a small epsilon = 1e-9 for numerical stability.
  - sMAPE is scale-free across stores and robust to level differences.

Modeling notes (optional but recommended)
- Useful feature ideas: calendar features (week-of-year, month, quarter, year), within-store lags (1, 2, 4, 52 weeks), rolling statistics, holiday effects, and interactions with macro covariates.
- Suitable approaches include global statistical models, gradient-boosted trees on engineered lag features, and sequence models (RNNs/TCNs/Transformers) that leverage the panel structure.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck and happy forecasting!
