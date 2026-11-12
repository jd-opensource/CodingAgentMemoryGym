# OpenMLE-fast task

Task ID: `coffee-bean-sales-raw-dataset@1`

Native metric: `CoffeeDemandForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3257 bytes)
- `data/sample_submission.csv` (11690 bytes); columns: ["product_id", "country", "month", "qty"]
- `data/test.csv` (15651 bytes); columns: ["product_id", "country", "month", "orders", "coffee_type", "roast_type", "size"]
- `data/train.csv` (223910 bytes); columns: ["product_id", "country", "month", "qty", "orders", "coffee_type", "roast_type", "size"]

## Public description

Coffee Demand Forecasting by Product–Country–Month

Overview
Retail planning needs accurate demand forecasts for each SKU in each market. Your task is to forecast monthly coffee bean quantities sold for every product–country combination for the next 3 months.

Task
Given historical transactional order data joined with customer countries and product attributes, predict total quantity sold per (product_id, country, month) for the next three months: 2022-06, 2022-07, and 2022-08.

Files
- train.csv: Panel of monthly observations with target and features.
- test.csv: Same structure but with the target removed for the forecast horizon.
- sample_submission.csv: An example of the required submission format with random, valid predictions.

Columns
All files are tabular CSVs.
- product_id: Product identifier (48 SKUs varying by bean type, roast, and pack size).
- country: Customer country derived from the customers table (United States, United Kingdom, Ireland appear in this dataset).
- month: Calendar month in YYYY-MM format.
- qty: Target variable — total units sold in that month for this (product_id, country).
- orders: Number of distinct orders contributing to that month’s qty (auxiliary feature).
- coffee_type: Static product attribute (e.g., Ara, Exc, Rob, Lib abbreviations in the raw data).
- roast_type: Static product attribute (L, M, D — light/medium/dark).
- size: Pack size in kilograms.

Train/Test Split
- Train contains all observed months up to and including 2022-05.
- Test contains a complete monthly panel for all observed (product_id, country) pairs over the next 3 months: 2022-06, 2022-07, 2022-08.
- Some series can be intermittent or even cold-start-like at this horizon; use cross-sectional signals (product attributes, country effects) and temporal patterns to generalize.

Submission
Submit a CSV with the following columns in this exact order:
product_id,country,month,qty
- month must be in YYYY-MM format.
- qty must be a non-negative number. Integer predictions are fine; floats will be accepted and evaluated numerically.
- The set of keys (product_id, country, month) must match test.csv exactly and in any order; they will be aligned for scoring.

Evaluation
Primary metric: sMAPE (symmetric mean absolute percentage error) averaged across all rows.
For true values y and predictions y_hat on each row:
  sMAPE = 2*|y - y_hat| / (|y| + |y_hat|), with sMAPE = 0 when y = y_hat = 0.
- This choice balances performance across high- and low-volume series and is robust to zeros.
- The final score is the mean sMAPE over all rows in the test set (lower is better).

Modeling Hints
- Consider calendar features (month of year, lags, moving averages), hierarchical modeling (SKU within country), and cross-learning across SKUs using the static product attributes.
- Intermittent demand techniques (croston variants) or tree-based regressors on the panel can be effective baselines.
- Use all data provided in train.csv; no external data is required.

Rules and Notes
- Do not attempt to reconstruct prices or revenue; the target is quantity (units) only.
- Keep deterministic pipelines for reproducibility.
- No data paths are included in the CSV files; treat them as relative to your working environment.
