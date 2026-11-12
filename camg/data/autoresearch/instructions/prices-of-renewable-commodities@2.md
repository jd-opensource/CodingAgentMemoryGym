# OpenMLE-fast task

Task ID: `prices-of-renewable-commodities@2`

Native metric: `RenewableCommoditiesMacroF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4185 bytes)
- `data/sample_submission.csv` (10511 bytes); columns: ["id", "up"]
- `data/test.csv` (23230 bytes); columns: ["id", "Year", "commodity", "real_index", "nominal_index", "cpi_index"]
- `data/train.csv` (120283 bytes); columns: ["id", "Year", "commodity", "real_index", "nominal_index", "cpi_index", "up"]

## Public description

Prices of Renewable Commodities: Directional Panel Forecasting Challenge

Problem statement
You are given annual nominal and real (CPI-deflated) price indexes for 18 renewable commodities from 1900–2018, plus the US CPI index (base year 1900). Your task is to predict whether each commodity’s real price index will go up next year (vs. not go up) using only information available up to the current year. This is a binary time-series classification problem in a multi-commodity panel.

What you must predict
For each (commodity, year t) in the test set, predict the probability that its next-year real index increases: P(real_{t+1} > real_t). Submissions should contain one row per test id with columns:
- id: a unique key for (commodity, year)
- up: a probability in [0,1] that the next-year real index increases

Data provided
All files are pre-cleaned and structured in a long panel format. The dataset includes the full historical coverage with no downsampling.
- train.csv: panel rows primarily from years 1900–1997 (t), one row per (commodity, Year). Columns:
  - id, Year, commodity, real_index, nominal_index, cpi_index, up
  - up is the training label for whether real_{t+1} > real_t (1 if strictly higher, else 0)
- test.csv: panel rows primarily from years 1998–2017 (t), one row per (commodity, Year). Columns:
  - id, Year, commodity, real_index, nominal_index, cpi_index
- sample_submission.csv: correct submission format with random but valid probabilities for up.
Note: Some commodity-year observations may be unavailable in the historical record; therefore, row counts per commodity can vary while remaining within the stated horizons.

Target construction (for train)
For each commodity independently and each year t where t+1 exists:
- up(t) = 1 if real_index(t+1) > real_index(t), else 0.

Important modeling notes
- Causality: Use only information up to year t for predicting movement from t to t+1. The provided train/test construction enforces this by aligning features at year t with the label referring to the change into t+1.
- Feature engineering is up to you. Common approaches include:
  - Lagged levels and log-levels: log(real_t), log(nominal_t), log(cpi_t)
  - Lagged returns: Δlog(real_t), Δlog(nominal_t), Δlog(cpi_t)
  - Rolling statistics over lookbacks (e.g., 3/5/10 years): means, volatility, drawdowns
  - Cross-commodity context (e.g., category averages) using only information available up to year t
- The long panel format makes it straightforward to compute lags and rolling features by grouping over commodity and sorting by Year.

Evaluation
Primary metric: Macro-averaged F1 across commodities.
- Compute binary predictions by thresholding the submitted probability up at 0.5 (values are clipped to [0,1]).
- For each commodity, compute the F1 score over its test years.
- The competition score is the unweighted mean of these per-commodity F1 scores.
Rationale: Class imbalance and dynamics vary by commodity and era. Macro F1 treats commodities fairly (equal weight per commodity) and balances precision/recall for directional accuracy.

File format constraints
- Submission must contain exactly two columns: id and up.
- id values must exactly match those in test.csv.
- up must be numeric and finite; values are clipped to [0,1] for scoring.

Train/test split
- Training horizon: mostly years 1900–1997 (predict Year t+1 from Year t)
- Test horizon: mostly years 1998–2017 (predict Year t+1 from Year t)
- Rows are included only where both Year t and Year t+1 real index values exist in the source data.
No validation set is provided; use your preferred validation strategy (e.g., time-based cross-validation).

What is allowed
- Any ML approach that uses only information available up to year t to predict the movement into t+1.
- External models are allowed, but do not rely on future information beyond t for any engineered features.

Deliverables
- train.csv, test.csv, sample_submission.csv
- Submit a CSV with columns [id, up] for scoring.

Good luck! This challenge rewards careful panel feature engineering, robust handling of nonstationarity, and models that share strength across heterogeneous commodity series.
