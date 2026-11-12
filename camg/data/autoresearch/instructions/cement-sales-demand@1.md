# OpenMLE-fast task

Task ID: `cement-sales-demand@1`

Native metric: `CementSalesSMAPEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3615 bytes)
- `data/sample_submission.csv` (129 bytes); columns: ["id", "sales"]
- `data/test.csv` (760 bytes); columns: ["id", "month", "production", "demand", "population", "gdp", "disbursement", "interest_rate"]
- `data/train.csv` (9135 bytes); columns: ["id", "month", "production", "demand", "population", "gdp", "disbursement", "interest_rate", "sales"]

## Public description

Cement Sales Nowcasting with Exogenous Signals

Problem statement
You are given monthly operational and macro-credit indicators for a cement company from Jan-2010 through Nov-2022. Your task is to predict monthly Sales (tons) for the final 12 months using the provided contemporaneous exogenous features (e.g., Production, Demand, GDP, Disbursement, Interest Rate, Population) and any features you engineer from them. This mirrors a realistic nowcasting problem where Sales must be inferred from month-end drivers with strong seasonality, trend, and structural breaks.

Files provided
- train.csv: Labeled historical data (all features plus the target).
- test.csv: Unlabeled data for the final 12 months (same features except the target column is removed).
- sample_submission.csv: A valid example submission file containing predictions for the test set (ids aligned with test.csv).

Target and features
- Target to predict: sales (monthly tons).
- Key provided fields per row include: id (row identifier), month (timestamp string), production, demand, population, gdp, disbursement, interest_rate. The training file also includes the target column sales.
- All numeric fields are real-valued. Sales and other operational quantities are non-negative. Month is chronologically ordered and unique per row.

Evaluation metric
- Submissions are evaluated using Symmetric Mean Absolute Percentage Error (sMAPE), averaged across the 12 test months:
  sMAPE = (100 / N) * sum_{i=1..N} 2 * |y_i - yhat_i| / (|y_i| + |yhat_i|)
  where y_i denotes the true Sales and yhat_i denotes your prediction. Lower is better. We compute the metric robustly by replacing any zero denominators with a small epsilon to avoid division-by-zero.

Submission format
- CSV with two columns and a header: id,sales
- id must match exactly the ids in test.csv (order does not matter; all ids must be present exactly once).
- sales must be valid real numbers (non-NaN, finite). Negative values are allowed by the scorer, but note that Sales are non-negative in the data; well-calibrated models should not rely on negative outputs.

Train/test split
- Chronological split is used to simulate real forecasting:
  - train.csv contains Jan-2010 through Nov-2021 (inclusive).
  - test.csv contains Dec-2021 through Nov-2022 (inclusive). All exogenous features are provided; the target sales is withheld.

Modeling guidance
- Strong yearly seasonality and long-term trend are present, with disruptions around 2015 and during the COVID-19 period. Effective approaches include:
  - Leakage-safe lag features (e.g., 1/3/6/12-month lags and rollings) for Sales (lags only), Production, Demand, GDP, Disbursement, Interest Rate.
  - Calendar features (month-of-year, Fourier seasonality) and trend terms.
  - Regularized linear models, tree ensembles (e.g., XGBoost/LightGBM), and time-series models with exogenous regressors (e.g., SARIMAX, Prophet).
- No external data is required; use only the provided features and your engineered features derived from them.

Important notes
- The dataset has been cleaned to standardize headers and types. The misspelled column in the raw source (disbusment) is standardized to disbursement. Month strings are parsed to timestamps internally; the provided month column is for your convenience in feature engineering.
- Avoid label leakage: do not generate features for a given month using Sales or future values beyond that month.

Deliverables
- Submit a CSV following the required format with predictions for all rows in test.csv. Your score will be computed using sMAPE on the hidden ground truth for those months.
