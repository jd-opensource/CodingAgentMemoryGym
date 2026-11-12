# OpenMLE-fast task

Task ID: `gold-price-1979-present@2`

Native metric: `GoldVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (501 bytes)
- `data/panel_test.csv` (668137 bytes); columns: ["id", "decision_month", "currency", "rv_current", "rq_current", "downsemivol_current", "ret_mean_current", "n_obs_current", "rv_roll_5d", "rv_roll_10d", "rv_roll_21d", "rv_roll_63d", "rv_roll_126d", "m_price", "q_price", "usd_rv_current", "month_of_year"]
- `data/panel_train.csv` (1707395 bytes); columns: ["id", "decision_month", "currency", "rv_current", "rq_current", "downsemivol_current", "ret_mean_current", "n_obs_current", "rv_roll_5d", "rv_roll_10d", "rv_roll_21d", "rv_roll_63d", "rv_roll_126d", "m_price", "q_price", "usd_rv_current", "month_of_year", "rv"]
- `data/sample_submission.csv` (88137 bytes); columns: ["id", "rv"]
- `data/test.csv` (668137 bytes); columns: ["id", "decision_month", "currency", "rv_current", "rq_current", "downsemivol_current", "ret_mean_current", "n_obs_current", "rv_roll_5d", "rv_roll_10d", "rv_roll_21d", "rv_roll_63d", "rv_roll_126d", "m_price", "q_price", "usd_rv_current", "month_of_year"]
- `data/train.csv` (1707395 bytes); columns: ["id", "decision_month", "currency", "rv_current", "rq_current", "downsemivol_current", "ret_mean_current", "n_obs_current", "rv_roll_5d", "rv_roll_10d", "rv_roll_21d", "rv_roll_63d", "rv_roll_126d", "m_price", "q_price", "usd_rv_current", "month_of_year", "rv"]

## Public description

Competition: Gold Risk Across Currencies – Next-Month Realized Volatility Forecasting

Files in this folder:
- panel_train.csv: training panel with features and target 'rv'.
- panel_test.csv: test panel with the same features (no 'rv').
- train.csv, test.csv: identical copies of panel_train/panel_test for convenience.
- sample_submission.csv: template with columns ['id','rv'].

Submission: upload a CSV with columns ['id','rv'] where rv>0.
Evaluation: average per-currency RMSE on the log of rv.
