# OpenMLE-fast task

Task ID: `srioryzia-multivariate-rice-price-forecasting@2`

Native metric: `RicePriceQuantileForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3396 bytes)
- `data/sample_submission.csv` (1554 bytes); columns: ["date", "q10", "q50", "q90"]
- `data/test.csv` (10357 bytes); columns: ["date", "anuradhapura_producer_price_lag1", "anuradhapura_producer_price_lag12", "anuradhapura_producer_price_lag3", "anuradhapura_producer_price_lag6", "exchange_rate_lag1", "exchange_rate_lag12", "exchange_rate_lag3", "exchange_rate_lag6", "fuel_price_lag1", "fuel_price_lag12", "fuel_price_lag3", "fuel_price_lag6", "kurunegala_producer_price_lag1", "kurunegala_producer_price_lag12", "kurunegala_producer_price_lag3", "kurunegala_producer_price_lag6", "m0_lag1", "m0_lag12", "m0_lag3", "m0_lag6", "m1_lag1", "m1_lag12", "m1_lag3", "m1_lag6", "m2_lag1", "m2_lag12", "m2_lag3", "m2_lag6", "m2b_lag1", "m2b_lag12", "m2b_lag3", "m2b_lag6", "month", "polonnaruwa_producer_price_lag1", "polonnaruwa_producer_price_lag12", "polonnaruwa_producer_price_lag3", "polonnaruwa_producer_price_lag6", "price_lag1", "price_lag12", "price_lag3", "price_lag6", "production_lag1", "production_lag12", "production_lag3", "production_lag6", "production_total_lag1", "production_total_lag12", "production_total_lag3", "production_total_lag6", "year"]
- `data/train.csv` (106841 bytes); columns: ["date", "price", "anuradhapura_producer_price_lag1", "anuradhapura_producer_price_lag12", "anuradhapura_producer_price_lag3", "anuradhapura_producer_price_lag6", "exchange_rate_lag1", "exchange_rate_lag12", "exchange_rate_lag3", "exchange_rate_lag6", "fuel_price_lag1", "fuel_price_lag12", "fuel_price_lag3", "fuel_price_lag6", "kurunegala_producer_price_lag1", "kurunegala_producer_price_lag12", "kurunegala_producer_price_lag3", "kurunegala_producer_price_lag6", "m0_lag1", "m0_lag12", "m0_lag3", "m0_lag6", "m1_lag1", "m1_lag12", "m1_lag3", "m1_lag6", "m2_lag1", "m2_lag12", "m2_lag3", "m2_lag6", "m2b_lag1", "m2b_lag12", "m2b_lag3", "m2b_lag6", "month", "polonnaruwa_producer_price_lag1", "polonnaruwa_producer_price_lag12", "polonnaruwa_producer_price_lag3", "polonnaruwa_producer_price_lag6", "price_lag1", "price_lag12", "price_lag3", "price_lag6", "production_lag1", "production_lag12", "production_lag3", "production_lag6", "production_total_lag1", "production_total_lag12", "production_total_lag3", "production_total_lag6", "year"]

## Public description

Competition: Probabilistic Retail Price Forecasting (Sri Lanka Colombo Nadu)

Problem statement
Participants must forecast the one-month-ahead predictive distribution of Colombo market retail prices for Sri Lankan Nadu rice. For each evaluation month, submit three quantiles (q10, q50, q90) of the next-month price, leveraging multivariate monthly covariates and lagged history.

Data
We provide a single consolidated monthly panel derived from official sources (1996–2022). You will work with the following files:
- train.csv: Model training table with one row per month. Columns include:
  - date: Month identifier in YYYY-MM format.
  - price: Target variable (retail Colombo price for Nadu rice) for that month.
  - Feature set: Lagged exogenous and autoregressive signals at lags 1, 3, 6, 12 months, plus calendar features (year, month). All features are constructed so that they are available by the end of the prior month, avoiding look-ahead leakage. These include lags for:
    - price (price_lag1, price_lag3, price_lag6, price_lag12)
    - producer prices from Anuradhapura, Kurunegala, Polonnaruwa (…_lag1, …_lag3, …_lag6, …_lag12)
    - annual/seasonal production totals (…_lag1, …_lag3, …_lag6, …_lag12)
    - exchange rate, fuel price, monetary aggregates (M0, M1, M2, M2B) (…_lag1, …_lag3, …_lag6, …_lag12)
    - calendar features: year, month
- test.csv: Same schema as train.csv except the target (price) is omitted. Rows correspond to the evaluation months described below.
- sample_submission.csv: Template indicating the required submission format with plausible example values.

Train/test split
- Chronological split to reflect real forecasting:
  - Train period: up to and including 2020-12.
  - Test period: 2021-01 through 2022-12 (inclusive).
- Each test row contains only features computable with information up to the previous month.

Submission format
- A CSV with the following columns:
  - date: Month identifier (YYYY-MM) matching test.csv.
  - q10, q50, q90: Predicted 10th, 50th, and 90th percentiles of the price for that month.
- All prediction columns must be numeric and finite. For each row, enforce q10 ≤ q50 ≤ q90.

Evaluation
- Primary metric: Average pinball (quantile) loss across q ∈ {0.1, 0.5, 0.9} and across all test months.
  - For a true price y and prediction y_q, the pinball loss is:
    L_q(y, y_q) = max(q·(y − y_q), (q − 1)·(y − y_q))
  - The competition score is the mean of L_q over all months and over the three quantiles.
- Interpretation: Lower is better. This metric rewards calibrated uncertainty and is robust to outliers while capturing asymmetric risks.

Modeling guidance (non-binding)
- Strong baselines: Quantile regression on lagged features; gradient boosting with quantile loss; naive persistence using price_lag1 for all three quantiles.
- Advanced approaches: Distributional forecasting (e.g., quantile GBMs, quantile RNN/TFT), conformal quantile adjustment, regime-aware models.

Important notes
- All features in train/test are pre-aligned to end-of-month timestamps; you should not access future information.
- Do not attempt to reconstruct contemporaneous variables at t from the original sources; only use the provided lagged features (and any you derive that still respect t−1 availability).
- Runtime is not constrained; prioritize correctness and calibration over speed.
