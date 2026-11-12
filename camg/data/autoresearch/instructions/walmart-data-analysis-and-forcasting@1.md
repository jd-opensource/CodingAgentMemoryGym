# OpenMLE-fast task

Task ID: `walmart-data-analysis-and-forcasting@1`

Native metric: `WalmartSalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (737 bytes)
- `data/sample_submission.csv` (8217 bytes); columns: ["row_id", "Weekly_Sales"]
- `data/test.csv` (27077 bytes); columns: ["row_id", "Store", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
- `data/train.csv` (356098 bytes); columns: ["row_id", "Store", "Date", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment", "Weekly_Sales"]

## Public description

Multi-store weekly sales forecasting

Files
- train.csv: Training data with target Weekly_Sales.
- test.csv: Test data without target.
- sample_submission.csv: Example submission file with required columns (row_id, Weekly_Sales).

Columns
- row_id: Unique identifier per (Store, Date)
- Store: Store identifier
- Date: Week-ending date in dd-mm-YYYY format
- Holiday_Flag: 1 if the week contains a major holiday, else 0
- Temperature: Average temperature that week (Fahrenheit)
- Fuel_Price: Fuel price index
- CPI: Consumer Price Index
- Unemployment: Unemployment rate

Prediction target
- Predict Weekly_Sales for every row in test.csv. Submit a CSV with columns: row_id, Weekly_Sales

Evaluation
- Macro-averaged RMSLE across stores.
