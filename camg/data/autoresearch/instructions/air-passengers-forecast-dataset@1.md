# OpenMLE-fast task

Task ID: `air-passengers-forecast-dataset@1`

Native metric: `AirPassengersForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2634 bytes)
- `data/sample_submission.csv` (162 bytes); columns: ["Month", "#Passengers"]
- `data/test.csv` (102 bytes); columns: ["Month"]
- `data/train.csv` (1602 bytes); columns: ["Month", "#Passengers"]

## Public description

AirPassengers-1960 Point Forecast Challenge

Problem statement
You are given a univariate monthly time series of international airline passengers. Using the monthly history from 1949-01 to 1959-12, forecast the monthly passenger totals for 1960-01 to 1960-12 (12 steps ahead). Submit one forecasted value per month.

Files provided
- train.csv: Historical data with two columns: Month, #Passengers. Contains months 1949-01 to 1959-12.
- test.csv: Future months to forecast with one column: Month. Contains months 1960-01 to 1960-12.
- sample_submission.csv: Example submission file with the expected columns and format.

Target
- #Passengers: Total passengers for the given Month. The target is an integer in the source data; your predictions may be real numbers.

Submission format
- CSV file with exactly two columns named Month and #Passengers.
- Must include exactly the same 12 Month values as in test.csv (order does not matter). Month format is YYYY-MM.

Evaluation
- Metric: sMAPE (symmetric Mean Absolute Percentage Error), averaged across the 12 test months.
  For month i with ground truth y_i and prediction ŷ_i:
    sMAPE_i = 2 * |y_i − ŷ_i| / (|y_i| + |ŷ_i|)
  The final score is the mean of sMAPE_i over the 12 months, expressed as a percentage on the leaderboard (lower is better). The implementation guards against division by zero and non-finite values.

Expected approaches
- This classic series exhibits a strong increasing trend and multiplicative seasonality (12-month period). Effective approaches include (but are not limited to):
  - Exponential smoothing (Holt-Winters/ETS)
  - SARIMA/Seasonal ARIMA
  - STL decomposition + ARIMA/ETS
  - State space models
  - Gradient boosting or tree-based models with calendar features (e.g., month-of-year), optionally modeling a transformed target (e.g., log)
  - Prophet/TBATS or similar tools
- Typical processing steps include: parsing Month, ensuring monthly frequency and ordering, optional transforms (log/Box-Cox), differencing, and feature engineering based on Month.

Rules and notes
- Use only the provided data. External data and manual look-ahead are not allowed.
- Keep numerical predictions finite; negative predictions will be clipped internally during metric computation but may harm your score.
- Do not include any extra columns in your submission. Column names must match exactly: Month, #Passengers.

Tips
- A seasonal naive baseline (use the same month from the previous year) is a strong starting point.
- Modeling on a log scale often helps capture multiplicative seasonality; remember to invert the transform when producing predictions.
