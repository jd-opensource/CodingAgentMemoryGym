# OpenMLE-fast task

Task ID: `gaza-strip-olive-oil-forecasting@2`

Native metric: `GazaOliveOilQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2934 bytes)
- `data/sample_submission.csv` (1933 bytes); columns: ["Date", "q0.10", "q0.50", "q0.90"]
- `data/test.csv` (324 bytes); columns: ["Date"]
- `data/train.csv` (2314 bytes); columns: ["Date", "USD_Price"]

## Public description

Gaza Olive Oil Price Probabilistic Forecasting (Quantiles)

Problem statement
- Forecast the distribution of monthly olive oil prices (USD) in Gaza for a held-out future period. Submit the 10th, 50th, and 90th percentile forecasts for each target month. The objective is to produce calibrated and sharp uncertainty estimates, not just point forecasts.

Files provided
- train.csv
  - Columns: Date, USD_Price
  - Historical monthly observations (15th of each month)
- test.csv
  - Columns: Date
  - Target months requiring forecasts
- sample_submission.csv
  - Columns: Date, q0.10, q0.50, q0.90
  - Example format with placeholder values

Target horizon and split
- Training period: 2007-01-15 to 2018-12-15 inclusive.
- Forecast target period: 2019-01-15 to 2021-07-15 inclusive, excluding two months with no labels in the source (2020-05-15 and 2020-09-15). All remaining months in that horizon are included.

Data notes
- Frequency: Monthly, timestamped on the 15th.
- Cleaning: Duplicate rows sharing the same Date were removed by Date (keeping the first instance). Two months in 2020 are genuinely absent and are not targets.
- Target variable: USD_Price. Submissions must be in USD level.

Submission format
- CSV with columns exactly: Date, q0.10, q0.50, q0.90
- One row per Date in test.csv; dates must match test.csv exactly. No extra/missing rows.
- q columns must contain finite numeric values. It is strongly recommended that q0.10 ≤ q0.50 ≤ q0.90 for each row.

Evaluation metric
- Mean pinball loss across all dates and τ ∈ {0.1, 0.5, 0.9}. Lower is better.
- For an observation with true value y and predicted quantile q at level τ:
  Lτ(y, q) = max(τ(y − q), (τ − 1)(y − q))
- Final score = average of Lτ over all target dates and the three quantiles.
- Rationale: Pinball loss is a proper scoring rule for quantile forecasts; it rewards calibrated uncertainty and sharpness and is robust to outliers.

Modeling guidance (non-exhaustive)
- Data processing: Parse Date; consider seasonality (annual pattern), potential regime shifts around 2019–2020, and transformations (e.g., log) if useful. Engineer time-based features such as month-of-year, lagged USD_Price (e.g., 1, 3, 6, 12 months), and rolling statistics (means/medians/volatility).
- Modeling options: Quantile regression (e.g., gradient boosting with quantile loss), random forest quantiles, SARIMA/ETS with simulation or bootstrapped residuals, state-space models, Prophet with uncertainty, or distributional neural models. Ensembling can improve calibration.
- Predictions must be reported in the original USD scale for q0.10, q0.50, q0.90 per Date.

What makes this challenge interesting
- Small-data regime with mild seasonality and possible structural shifts requires careful uncertainty modeling.
- Proper handling of irregularities (duplicates removed; two absent months not targeted) avoids leakage and keeps the task realistic.
