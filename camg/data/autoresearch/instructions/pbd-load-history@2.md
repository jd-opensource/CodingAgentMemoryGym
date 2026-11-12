# OpenMLE-fast task

Task ID: `pbd-load-history@2`

Native metric: `LoadForecastQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3066 bytes)
- `data/sample_submission.csv` (435088 bytes); columns: ["id", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (372922 bytes); columns: ["id", "date", "year", "month", "day", "weekday", "hour", "temperature"]
- `data/train.csv` (4801934 bytes); columns: ["id", "date", "year", "month", "day", "weekday", "hour", "temperature", "demand"]

## Public description

Bangladesh Hourly Load Forecasting (Probabilistic Day‑Ahead Quantiles)

Problem statement
Utilities must plan for uncertainty around next‑day electricity demand. Using historical hourly system load and temperature, your task is to produce calibrated probabilistic forecasts for the next year. Given history up to 2013‑12‑31, predict the 10th, 50th, and 90th percentiles of hourly load for every hour in 2014.

Files
- train.csv: Training data with columns
  - id: Unique row identifier formatted YYYY-MM-DD-HH (HH in 01–24)
  - date: ISO date string YYYY-MM-DD
  - year, month, day: Calendar integers
  - weekday: Integer in [1..7] as provided in the source data (1=Sunday, 7=Saturday)
  - hour: Integer in [1..24]
  - temperature: Realized temperature (°C)
  - demand: Target variable, system load (MW)
- test.csv: Same schema as train.csv but without the demand column. Contains all 2014 hours (8,760 rows).
- sample_submission.csv: Example submission with columns
  - id
  - q0.1, q0.5, q0.9: Predicted quantiles of demand (MW)

Task
- Train models on train.csv and generate predictions for every id in test.csv.
- Your submission must contain one row per id in test.csv and the three columns q0.1, q0.5, q0.9. Values must be finite numbers.
- Use only the provided dataset files; do not use external data or labels.

Evaluation
- Submissions are evaluated using the mean pinball (quantile) loss averaged over all test rows and the quantiles Q = {0.1, 0.5, 0.9}.
  - For a true value y and a predicted quantile qα at level α, the pinball loss is:
    Lα(y, qα) = (α − 1[y < qα]) · (y − qα).
  - The final score is the arithmetic mean of Lα across all test rows and all α ∈ {0.1, 0.5, 0.9}. Lower is better.
- Predictions must be numeric and finite. It is recommended (but not required) that quantiles are non‑decreasing: q0.1 ≤ q0.5 ≤ q0.9.

Scope and guidance
- Use only information available up to the time you forecast. The test set includes realized 2014 temperatures to focus the task on load modeling rather than weather prediction.
- Feature ideas (optional): calendar features (hour, weekday, month, weekend flags), lagged loads (e.g., 1–48, 168 hours), rolling statistics, temperature non‑linearities (splines, piecewise functions), interaction terms, and time‑varying variance cues.
- Any regression approach that supports quantiles is applicable: gradient boosting with quantile loss, random forests, SARIMAX with distributional modeling, quantile neural nets, temporal CNN/Transformers, ensembling, etc.

Important notes
- Hours are numbered 01–24. Dates are continuous with no DST adjustments.
- The full dataset is used; no subsampling. The split is fixed: train covers up to 2013‑12‑31; test covers 2014‑01‑01 to 2014‑12‑31.
- The order of rows in your submission does not matter as long as all ids are present and unique.

Submission format (must match exactly)
- Columns: id, q0.1, q0.5, q0.9
- One row per id present in test.csv
- Numeric, finite values only

Good luck and happy forecasting!
