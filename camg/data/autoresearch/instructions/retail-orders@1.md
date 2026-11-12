# OpenMLE-fast task

Task ID: `retail-orders@1`

Native metric: `RetailOrdersRevenueForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3190 bytes)
- `data/sample_submission.csv` (202661 bytes); columns: ["week_start_date", "Region", "Category", "Sub Category", "weekly_revenue"]
- `data/test.csv` (137741 bytes); columns: ["week_start_date", "Region", "Category", "Sub Category"]
- `data/train.csv` (163119 bytes); columns: ["week_start_date", "Region", "Category", "Sub Category", "weekly_revenue"]

## Public description

# Hierarchical Weekly Revenue Forecasting for US Retail Orders

Problem statement
Participants must forecast weekly revenue for every Region–Category–Sub Category combination in 2023, using historical orders from 2022. The target is the total weekly revenue per group, where revenue is computed deterministically from order-level fields.

Files provided
- train.csv: Weekly aggregates for 2022 with the target.
- test.csv: The forecasting keys (Region, Category, Sub Category, week_start_date) for 2023, without the target.
- sample_submission.csv: A correctly formatted example submission for test.csv with random but valid predictions.

Data description
- Granularity: Weekly time series per (Region, Category, Sub Category).
- Week convention: Weeks start on Monday. The key column week_start_date is the Monday date for that week.
- Target definition: weekly_revenue = sum over the week of List Price × (1 − Discount Percent/100) × Quantity for all orders belonging to the same Region–Category–Sub Category.
- Training horizon: All Mondays in 2022.
- Test horizon: All Mondays in 2023.
- Group coverage: Only Region–Category–Sub Category groups that appear in both 2022 and 2023 are included to ensure all test labels occur in training at least once.

Columns
- week_start_date: Date string (YYYY-MM-DD) representing the Monday of the week.
- Region: Region name.
- Category: Product category.
- Sub Category: Product subcategory.
- weekly_revenue: Non-negative float; only present in train.csv and the final submission file.

Submission format
- CSV with columns: week_start_date, Region, Category, Sub Category, weekly_revenue.
- Must contain exactly the same rows as test.csv (same keys, no duplicates, one prediction per row).
- weekly_revenue must be non-negative. Predictions may be any non-negative real values.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE) on weekly_revenue:
  rmsle = sqrt(mean((log1p(y_pred) − log1p(y_true))^2))
- Why RMSLE: Weekly revenue has many small values and occasional spikes; RMSLE balances relative and absolute error, handles zeros with log1p, and is robust to scale differences across groups.

Modeling notes
- This is a pure forecasting task: no future covariates are provided for 2023. Participants may use hierarchical reconciliation, classical time-series models (ETS/ARIMA), machine learning on lagged features (XGBoost/LightGBM), or hybrid approaches.
- Feature engineering ideas (from history only): lags and rolling statistics of revenue, price/discount mix derived from 2022, seasonal indicators (month/week-of-year), group-level embeddings, and cross-sectional pooling.
- Handle intermittency and zeros carefully; clipping to non-negatives is recommended.

Rules and clarifications
- Train and test keys are aligned by design; the week_start_date convention is fixed (Monday). Do not alter the calendar alignment.
- Do not introduce external future covariates that are not strictly known in advance; only history up to the forecast week should inform predictions.
- The submission is evaluated against the exact keys in test.csv; ordering does not matter as long as keys match and there are no duplicates.
