# OpenMLE-fast task

Task ID: `nuclear-energy-datasets@1`

Native metric: `NuclearCapacityFactorForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2912 bytes)
- `data/sample_submission.csv` (1141 bytes); columns: ["Year", "Month", "Nuclear Generating Units, Capacity Factor"]
- `data/test.csv` (1522 bytes); columns: ["Year", "Month", "Nuclear Generating Units, Total Operable Units", "Nuclear Generating Units, Net Summer Capacity", "Nuclear Electricity Net Generation", "Nuclear Share of Electricity Net Generation"]
- `data/train.csv` (22302 bytes); columns: ["Year", "Month", "Nuclear Generating Units, Total Operable Units", "Nuclear Generating Units, Net Summer Capacity", "Nuclear Electricity Net Generation", "Nuclear Share of Electricity Net Generation", "Nuclear Generating Units, Capacity Factor"]

## Public description

US Nuclear Capacity Factor Forecasting (Monthly)

Problem statement
Forecast the monthly capacity factor (%) of U.S. nuclear generating units over a held-out test window. Use historical monthly sector indicators and your own engineered time-series features to predict the capacity factor for each month in the test set.

Why this matters
The U.S. nuclear fleet delivers steady baseload power but exhibits seasonal and maintenance-driven variability. Accurate monthly forecasts support grid planning, outage scheduling, and fuel procurement.

Files provided
- train.csv: Monthly observations with features and the target for the training period.
- test.csv: Monthly observations with the same features as train.csv but without the target for the forecasting period.
- sample_submission.csv: Example of the required submission format.

Columns
- Year (integer)
- Month (full English month name, e.g., January)
- Nuclear Generating Units, Total Operable Units
- Nuclear Generating Units, Net Summer Capacity
- Nuclear Electricity Net Generation
- Nuclear Share of Electricity Net Generation
- Nuclear Generating Units, Capacity Factor (target; present only in train.csv)

Target and feature engineering
- Target: Nuclear Generating Units, Capacity Factor (percent)
- You may create any features you like from the provided columns in train.csv and test.csv, including but not limited to:
  - Lags and rolling statistics (e.g., t-1..t-12, 3/6/12-month means)
  - Month-of-year and other calendar effects
  - Differences and growth rates (MoM, YoY)
- If you choose to use any additional files available in this dataset package, treat them strictly as exogenous inputs and avoid any leakage from the test period.

Submission format
- A CSV file with the following columns and header:
  - Year
  - Month (full English month name)
  - Nuclear Generating Units, Capacity Factor
- Each row must correspond to a unique Year–Month combination appearing in test.csv. Order does not matter, but each Year–Month must appear exactly once. All values must be finite numbers.

Evaluation
- Primary metric: Root Mean Squared Error (RMSE) computed between your submitted capacity factor and the ground truth for the test window.
  - RMSE = sqrt(mean((y_pred − y_true)^2))
- For reference only, we will also display Mean Absolute Error (MAE).
- Submissions containing NaN/inf values are invalid.

Train/test split
- The split is strictly chronological to emulate real forecasting. Do not use any information from the test period when building features, performing scaling, or training models.

Tips
- Expect strong seasonality and refueling cycles; lagged and seasonal features are often effective.
- Some early months may have missing values in certain fields; handle missing data appropriately.
- Try multiple modeling approaches (e.g., SARIMAX/ETS, gradient-boosted trees on engineered features, or deep time-series models).
