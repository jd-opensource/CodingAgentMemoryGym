# OpenMLE-fast task

Task ID: `us-dollar-index-data@2`

Native metric: `DXYVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2561 bytes)
- `data/sample_submission.csv` (20160 bytes); columns: ["row_id", "rv10"]
- `data/test.csv` (32958 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Price"]
- `data/train.csv` (286026 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Price", "rv10"]

## Public description

Title: DXY 10‑Day Realized Volatility Forecasting

Problem statement
You are given a daily OHLC history of the US Dollar Index (DXY). For each trading day t, predict the annualized realized volatility of close‑to‑close log returns over the next 10 trading days:

RV10(t) = sqrt(252) * stdev(r_{t+1}, r_{t+2}, ..., r_{t+10}),
where r_i = ln(Price_i / Price_{i-1}). The stdev is the population standard deviation (ddof = 0) and the natural logarithm is used. This setup mirrors forward‑looking risk estimation used in practice.

Data description
- train.csv: Columns [row_id, Date, Open, High, Low, Price, rv10]. Each row is a day t with its OHLC and the target rv10 computed from future returns r_{t+1..t+10}.
- test.csv: Columns [row_id, Date, Open, High, Low, Price]. Same structure as train but without rv10. Your task is to predict rv10 for these rows.
- sample_submission.csv: Columns [row_id, rv10]. A valid example submission with random but positive values.

Notes
- Date is a trading calendar date. Rows are strictly ordered in time.
- Price corresponds to the daily close.
- The Change % field from the source data is omitted because it is derivable from Price and adds no independent information beyond returns.
- No additional data is required; you may engineer any features from the provided OHLC and Date.

Evaluation metric
Submissions are evaluated using Mean Absolute Error on log‑volatility:

MAE_log = mean( | ln(y_true) − ln(y_pred) | ),

with the following conventions:
- Natural logarithm is used.
- y_true and y_pred must be strictly positive; implementations should clip to a small epsilon (e.g., 1e-12) to avoid numerical issues.

Why this metric? Volatility is positive and heavy‑tailed; evaluating in log‑space provides a scale‑aware, robust measure that avoids domination by occasional spikes and treats relative errors more symmetrically.

Rules and guidance
- Time‑series discipline: Do not use any information from dates after t when building features for day t.
- You may use any ML approach (linear models, tree ensembles, HAR/RV, sequence models, etc.). Range‑based volatility features (e.g., from High/Low) and return‑based features are often useful.
- The task is challenging: volatility clusters and regime shifts (e.g., crisis periods) matter. Proper feature engineering and regularization are critical.

File naming and columns expected for submissions
- Submit a CSV with columns [row_id, rv10].
- row_id must exactly match those in test.csv.

Good luck and have fun forecasting DXY’s volatility!
