# OpenMLE-fast task

Task ID: `macro-economic-indicators-data@1_duplicate_1`

Native metric: `USEquityReturnForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (282 bytes)
- `data/sample_submission.csv` (9496 bytes); columns: ["row_id", "target"]
- `data/test.csv` (43240 bytes); columns: ["row_id", "date", "s_p_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns"]
- `data/train.csv` (184936 bytes); columns: ["row_id", "date", "s_p_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns", "target"]

## Public description

Title: Forecast 12-Month Real Total Return of U.S. Equities

Files
- train.csv
- test.csv
- sample_submission.csv

Evaluation
- Metric: Mean Absolute Error (MAE) on the target (lower is better).
- Submission format: CSV with two columns: row_id, target. Row order is not important.
