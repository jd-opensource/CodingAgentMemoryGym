# OpenMLE-fast task

Task ID: `drw-remix-ii-remix-again-data@1`

Native metric: `DRWRemixQuantileForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2772 bytes)
- `data/sample_submission.csv` (24539687 bytes); columns: ["ID", "q05", "q10", "q20", "q30", "q40", "q50", "q60", "q70", "q80", "q90", "q95"]
- `data/test.csv` (753413 bytes); columns: ["ID"]
- `data/train.csv` (11281524 bytes); columns: ["ID", "value"]

## Public description

DRW Remix II — One-Stream Probabilistic Forecasting

Problem statement
You are given a long univariate sequence x_t observed at equally spaced time indices (ID). Your goal is to build a model that, for each time step in a held-out future segment, outputs calibrated predictive quantiles of x_t using only observations up to t−1.

Files provided
- train.csv: Historical data with columns:
  - ID: integer time index (ascending)
  - value: the observed numeric value at that time
- test.csv: Future segment to forecast with column:
  - ID: integer time index to forecast
- sample_submission.csv: Example submission showing the required format.

Task
For every row in test.csv, predict a set of conditional quantiles of value at the specified ID. Use only information from IDs strictly less than the forecasted ID when constructing features or models (i.e., no look-ahead).

Submission format
Submit a CSV with exactly these columns, in this order:
- ID
- q05, q10, q20, q30, q40, q50, q60, q70, q80, q90, q95
Each row corresponds to a row in test.csv with the same ID. Quantile values must be numeric, finite, and non-decreasing within each row (q05 ≤ q10 ≤ … ≤ q95). IDs in your submission must match test.csv exactly and in order.

Quantile levels
τ ∈ {0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95}

Evaluation
Submissions are scored with the mean pinball (quantile) loss averaged across all requested quantiles and all test rows. For a target y and a submitted quantile q_τ at level τ, the pinball loss is:
L_τ(y, q_τ) = (τ − I[y < q_τ]) · (y − q_τ)
Your final score is the average of L_τ over all test rows and the 11 quantile levels.

Notes and recommendations
- Ordering: The data are already ordered by ID. Do not shuffle and avoid any leakage from the held-out segment.
- Feature engineering (optional):
  - Lagged values, rolling statistics (means/medians/quantiles), exponentially weighted statistics, differencing.
  - Regime or drift indicators via change-point or variance tests.
  - Time index features (e.g., normalized ID) to capture slow mean drift.
- Normalization: If standardizing, compute parameters using training data only.
- Baselines to consider:
  - Global distribution baseline: submit quantiles of the training distribution for all test rows.
  - Rolling-window quantile estimates to adapt locally.
  - Parametric state-space/Kalman-style models to produce mean/variance converted to quantiles.

Final data files
- train.csv
- test.csv
- sample_submission.csv

Metric characteristics
The pinball loss is a proper scoring rule for quantile forecasts. It rewards accurate and well-calibrated uncertainty estimates, is robust to outliers, and provides precise leaderboard separation on long sequences.
