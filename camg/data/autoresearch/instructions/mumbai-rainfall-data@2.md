# OpenMLE-fast task

Task ID: `mumbai-rainfall-data@2`

Native metric: `MumbaiRainfallExceedanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3446 bytes)
- `data/sample_submission.csv` (6572 bytes); columns: ["row_id", "probability"]
- `data/test.csv` (30785 bytes); columns: ["row_id", "year", "month", "trend", "lag1", "lag2", "lag3", "lag4", "lag5", "roll3_mean", "roll5_mean", "monsoon_prev1", "monsoon_prev3_avg"]
- `data/train.csv` (156965 bytes); columns: ["row_id", "year", "month", "trend", "lag1", "lag2", "lag3", "lag4", "lag5", "roll3_mean", "roll5_mean", "monsoon_prev1", "monsoon_prev3_avg", "target"]

## Public description

Mumbai Extreme Monthly Rainfall: Probabilistic Exceedance Forecasting

Overview
Urban flood risk and water management rely on anticipating unusually wet months. Your task is to learn from 120+ years of Mumbai’s monthly rainfall and, for each Year–Month in the test set, predict the probability that rainfall will be “extreme” for that calendar month.

Target definition (fixed and deterministic)
- For each calendar month (1–12), an extreme threshold is defined as the 95th percentile of that month’s rainfall computed using the training set only.
- The binary target y is 1 if rainfall for a Year–Month exceeds that month’s threshold; otherwise 0. Train labels are computed with this protocol. Test labels use the same thresholds but are hidden.

Files
- train.csv: One row per Year–Month with engineered features and the target column.
- test.csv: Same features as train.csv, without the target.
- sample_submission.csv: Shows the required submission format with random but valid probabilities.

Columns
- row_id: Unique identifier in the form "YYYY-MM".
- year: Year number.
- month: Integer in [1, 12].
- trend: year minus the first year in the dataset (a simple linear trend feature).
- lag1, lag2, lag3, lag4, lag5: Rainfall of the same calendar month in the previous 1–5 years.
- roll3_mean, roll5_mean: Rolling means of the same-month rainfall over the last 3 and 5 available years, respectively.
- monsoon_prev1: Sum of June–September rainfall in the previous year.
- monsoon_prev3_avg: Average of June–September totals over the previous 3 years.
- target (train only): Binary label 0/1 for extreme exceedance.

Important notes
- The source has only rainfall; no exogenous climate drivers are included. Useful modeling includes feature engineering, seasonality handling, and probability calibration.
- Features are constructed strictly from historical information prior to each Year–Month to avoid leakage. Missing lags (e.g., at the very beginning of the record) are imputed to -1.
- The “Total” annual rainfall is not used as a feature.

Submission format
- A CSV with exactly two columns and a header: row_id,probability
- row_id must match the identifiers in test.csv.
- probability is a floating-point number in [0, 1] representing P(y=1).

Evaluation
- Metric: Log loss (binary cross-entropy) averaged over all test rows.
- Given N test rows with targets yi in {0,1} and submitted probabilities pi, the score is:
  -logloss = -(1/N) * Σ [ yi * log(pi) + (1 - yi) * log(1 - pi) ]
- Submissions are clipped to [1e-15, 1 - 1e-15] for numerical stability.
- Log loss is a proper scoring rule favoring calibrated probabilistic forecasts and handling imbalance between extreme and non-extreme months.

Suggested approaches
- Seasonal modeling: model each month’s process or include strong month indicators/embeddings.
- Feature engineering: lags, rolling stats, long-term trends, and monsoon accumulation features already provided can be extended.
- Modeling: Logistic regression, gradient boosting trees (e.g., XGBoost, LightGBM, CatBoost), random forests, calibrated classifiers, or probabilistic time-series models.
- Validation: Time-based splits (e.g., rolling-origin). Consider post-hoc calibration (isotonic or Platt) on a validation fold.

Deliverables
- Submit probabilities for all rows in test.csv following the format above.
- Higher scores indicate better models (lower log loss). Good luck!
