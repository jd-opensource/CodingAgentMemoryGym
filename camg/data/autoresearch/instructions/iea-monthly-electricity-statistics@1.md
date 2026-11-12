# OpenMLE-fast task

Task ID: `iea-monthly-electricity-statistics@1`

Native metric: `ElectricityForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3965 bytes)
- `data/sample_submission.csv` (389761 bytes); columns: ["row_id", "VALUE"]
- `data/test.csv` (581681 bytes); columns: ["row_id", "COUNTRY", "PRODUCT", "YEAR", "MONTH"]
- `data/train.csv` (6904379 bytes); columns: ["COUNTRY", "PRODUCT", "YEAR", "MONTH", "VALUE"]

## Public description

Monthly Electricity Panel Forecasting: 2022 by Country and Product

Problem statement
Build a model to forecast monthly electricity metrics (in GWh) for calendar year 2022 across all observed country–product pairs. Each target is a VALUE for a specific (COUNTRY, PRODUCT, YEAR, MONTH) combination. The task covers thousands of related monthly time series with heterogeneous scales, strong seasonality, and structural changes.

Data files
- train.csv: Historical data from 2010–2021 across all countries and products. Columns:
  - COUNTRY (string)
  - PRODUCT (string)
  - YEAR (int)
  - MONTH (int, 1–12)
  - VALUE (float, target)
- test.csv: Forecasting targets for 2022. Columns:
  - row_id (string, unique key for each row)
  - COUNTRY (string)
  - PRODUCT (string)
  - YEAR (int = 2022)
  - MONTH (int, 1–12)

Submission format
- Submit a CSV with two columns and the same number of rows as test.csv:
  - row_id (string)
  - VALUE (float, your prediction in GWh)
- The row_id must exactly match test.csv. Missing or extra rows are not allowed.

What is provided and what is not
- train.csv includes only the core modeling columns (COUNTRY, PRODUCT, YEAR, MONTH, VALUE) to avoid presentational noise.
- test.csv excludes leakage-prone fields such as cumulative within-year aggregates or derived shares; you should build features from train.csv.
- The split is strictly time-based: train = YEAR ≤ 2021; test = YEAR = 2022, for all rows that exist in 2022 in the raw data.
- There may be intermittent/missing months in some series; score only the rows present in test.csv.

Evaluation metric: Weighted sMAPE
- The leaderboard metric is a weighted symmetric mean absolute percentage error (sMAPE) computed at the row level and aggregated with series-level weights.
- For a given row i with ground truth y_i and prediction ŷ_i:
  sMAPE_i = 2 * |y_i − ŷ_i| / (|y_i| + |ŷ_i| + ε), with ε = 1.0 to stabilize near zero.
- Series definition: A series is identified by the pair (COUNTRY, PRODUCT). Each row in test belongs to exactly one series.
- Weights:
  1) For each series j that appears in test, compute its historical scale w*_j as the mean of VALUE over 2019–2021 in train.
  2) If a series has no rows in 2019–2021, fall back to its mean VALUE over all available years in train.
  3) Replace non-finite or non-positive scales with a small positive constant and normalize weights across all test series so that sum_j w_j = 1.
  4) Each series weight w_j is equally distributed over its test rows so every row from series j has weight w_j / N_j, where N_j is the number of test rows in that series.
- The final score is the weighted average of sMAPE_i over all test rows. Lower is better.

Modeling guidance
- Strong recurring seasonality suggests using calendar features (month-of-year) and lagged/rolling statistics (e.g., 12-month lag, rolling means).
- Global models that learn across countries and products (e.g., gradient boosting, linear models with interactions, or sequence models) often outperform per-series models, especially for small series.
- Consider log1p transformations for skewed targets, device careful handling of zeros/near-zeros, and robust back-transforms.
- Hierarchical relations (e.g., renewables vs. components) may help; coherence is not enforced but can be exploited.

Files you will interact with
- train.csv (training data)
- test.csv (features and row_id for 2022 targets)
- sample_submission.csv (template with valid row_id and example values)

Rules and notes
- Do not add or remove rows in test.csv; your submission must align exactly via row_id.
- Do not rely on any fields other than those provided in train.csv and test.csv. External data is optional but not required.
- Numeric handling should be robust: avoid producing NaN/Inf; predictions can be any real numbers but should be in GWh units.

Good luck and enjoy tackling a realistic, large-scale panel forecasting challenge in the electricity domain!
