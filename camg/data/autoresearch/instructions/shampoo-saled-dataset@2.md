# OpenMLE-fast task

Task ID: `shampoo-saled-dataset@2`

Native metric: `ShampooSalesQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2763 bytes)
- `data/sample_submission.csv` (749 bytes); columns: ["Month", "q0.10", "q0.50", "q0.90"]
- `data/test.csv` (66 bytes); columns: ["Month"]
- `data/train.csv` (276 bytes); columns: ["Month", "Sales"]

## Public description

Competition: Probabilistic Multi‑Horizon Forecasting of Monthly Shampoo Sales

Problem statement
You are given a univariate monthly retail demand series with trend and weak seasonality. Using the first two years (24 months) of observations as training data, forecast the predictive distribution for the next 12 months. Your submission must provide calibrated quantile forecasts at the 10th, 50th, and 90th percentiles for each test month on the original sales scale.

Files provided after running prepare.py
- train.csv: 24 rows with columns [Month, Sales].
- test.csv: 12 rows with column [Month] only (no labels).
- sample_submission.csv: Example submission with columns [Month, q0.10, q0.50, q0.90].

Data description
- Month: String index of the form Y-M (e.g., "1-01" … "3-12"), representing sequential months. Use it to reconstruct chronological order; do not assume calendar years.
- Sales: Monthly shampoo sales (float). There are no missing values in the provided data.

Task
- Train on the 24 rows in train.csv and produce 3 quantile forecasts for every Month in test.csv.
- Submit a CSV with one row per test Month and columns exactly: [Month, q0.10, q0.50, q0.90]. All values must be on the original sales scale and finite numbers. Quantiles must be non‑decreasing per row: q0.10 ≤ q0.50 ≤ q0.90.

Evaluation
- Metric: Mean pinball loss (quantile loss), averaged uniformly over the 12 horizons and the three quantiles {0.10, 0.50, 0.90}.
  For a true value y and predicted quantile ŷ_q at level q, the loss is: (q − 1{y < ŷ_q}) · (y − ŷ_q). Lower is better.
- Submissions are validated for correct columns, exact Month coverage and uniqueness, numeric finite values, and per‑row quantile monotonicity.

Guidance and constraints
- Use any ML approach (statistical or machine‑learning) to model the series and produce predictive distributions: e.g., ETS/ARIMA with simulation, state‑space models, Prophet, quantile regression across horizons, bootstrapped residuals, or distributional neural nets. You may apply transformations internally (e.g., log1p, Box‑Cox, differencing) but your submitted quantiles must be on the original Sales scale.
- External data is not provided or required. Feature engineering from the Month index (e.g., trend, seasonal dummies, Fourier terms) is permitted.
- Runtime limits are generous for this small dataset; prioritize model quality and calibrated uncertainty.

Submission format
- CSV with header and exactly these columns in order: Month,q0.10,q0.50,q0.90
- Each Month value must appear exactly once and match those in test.csv.

Summary
- Train on train.csv
- Predict quantiles for every Month in test.csv
- Submit Month,q0.10,q0.50,q0.90
- Scored by mean pinball loss (lower is better)
