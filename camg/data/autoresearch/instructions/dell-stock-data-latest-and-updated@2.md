# OpenMLE-fast task

Task ID: `dell-stock-data-latest-and-updated@2`

Native metric: `DellVolatilityRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3055 bytes)
- `data/sample_submission.csv` (5045 bytes); columns: ["Id", "log_rv10"]
- `data/test.csv` (76473 bytes); columns: ["Id", "gk_var_rollsum_5", "gk_var_rollsum_10", "gk_var_rollsum_20", "gk_var_rollsum_40", "parkinson_rollsum_5", "parkinson_rollsum_10", "parkinson_rollsum_20", "parkinson_rollsum_40", "retcc2_rollsum_5", "retcc2_rollsum_10", "retcc2_rollsum_20", "retcc2_rollsum_40", "vol_log", "vol_rollmean_10", "vol_rollstd_10", "turnover", "turnover_z10", "beta", "days_since_div", "split_regime", "dow", "dom", "month"]
- `data/train.csv` (325176 bytes); columns: ["Id", "gk_var_rollsum_5", "gk_var_rollsum_10", "gk_var_rollsum_20", "gk_var_rollsum_40", "parkinson_rollsum_5", "parkinson_rollsum_10", "parkinson_rollsum_20", "parkinson_rollsum_40", "retcc2_rollsum_5", "retcc2_rollsum_10", "retcc2_rollsum_20", "retcc2_rollsum_40", "vol_log", "vol_rollmean_10", "vol_rollstd_10", "turnover", "turnover_z10", "beta", "days_since_div", "split_regime", "dow", "dom", "month", "log_rv10"]

## Public description

Title: 10‑Day Realized Volatility Forecasting for DELL (Action‑Adjusted)

Problem statement
Forecast the next‑10‑trading‑day realized volatility of DELL using only information available up to each day t. Targets are computed from action‑adjusted OHLC data with a range‑based estimator. The task emphasizes careful time‑series processing, feature engineering, and robust modeling under corporate actions and non‑stationary regimes.

Data description
You are provided with pre‑constructed training and testing tables derived from the full daily DELL OHLCV history and corporate‑action logs. All prices are forward‑adjusted for stock splits. Feature columns include rolling range/return/volume statistics, calendar/event indicators, and static normalization using company share counts. The target is the natural log of annualized 10‑day realized volatility computed from adjusted OHLC using the Garman–Klass (GK) variance.

Files
- train.csv: One row per forecast date t with Id, features, and the target column log_rv10.
- test.csv: Same schema as train.csv but without the target. Predict log_rv10 for these Ids.
- sample_submission.csv: Example submission with columns [Id, log_rv10]. Values are plausible but random and should be replaced by your predictions.

Target construction (deterministic)
Let O_t, H_t, L_t, C_t be the forward‑adjusted OHLC for trading day t. Define the Garman–Klass one‑day variance:
  σ_GK^2(t) = 0.5·(ln(H_t/L_t))^2 − (2·ln(2)−1)·(ln(C_t/O_t))^2.
For each forecast date t, the next‑10‑trading‑day annualized realized volatility is:
  RV_10(t) = sqrt((252/10) · Σ_{k=1..10} σ_GK^2(t+k)).
The supervised learning target is:
  log_rv10(t) = ln(RV_10(t)).

Evaluation metric
Root Mean Squared Error (RMSE) on log_rv10 over the test Ids.
- RMSE on the log scale stabilizes heteroskedasticity and penalizes relative errors symmetrically.
- Predictions must be finite numerics; invalid values are rejected.

Submission format
- CSV with exactly two columns in this order: Id, log_rv10.
- Ids must exactly match those in test.csv (order independent), without duplicates.

Train/test protocol
- Chronological split: the last 20% of forecast dates are in test.csv; earlier dates are in train.csv.
- Features are constructed strictly from information up to and including day t. Labels use days [t+1, t+10]. No leakage from the future.

Starter tips (optional)
- Effective features: rolling GK/Parkinson/close‑to‑close volatilities; range ratios; turnover, turnover z‑scores; volume volatility; momentum; jump indicators; calendar/event features (days since last dividend, split regime flags).
- Baseline approaches: regularized linear models, tree‑based ensembles, or sequence models (state‑space, temporal CNNs/Transformers). Cross‑validate by time.

Integrity notes
- Targets cannot be reconstructed from test.csv alone. Focus on modeling the mapping from features to log_rv10.
- No external data is required (but feature engineering from provided columns is encouraged).
