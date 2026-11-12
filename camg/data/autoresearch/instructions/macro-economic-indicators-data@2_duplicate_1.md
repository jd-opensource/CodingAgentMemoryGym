# OpenMLE-fast task

Task ID: `macro-economic-indicators-data@2_duplicate_1`

Native metric: `MacroDrawdownAPMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2947 bytes)
- `data/sample_submission.csv` (8286 bytes); columns: ["row_id", "probability"]
- `data/test.csv` (42466 bytes); columns: ["row_id", "date", "sp_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "unnamed_13", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns", "unnamed_21", "unnamed_22", "unnamed_23", "unnamed_24"]
- `data/train.csv` (162267 bytes); columns: ["row_id", "date", "sp_comp", "dividend", "earnings", "consumer_price_index_cpi", "date_fraction", "long_interest_rate_gs10", "real_price", "real_dividend", "real_total_return_price", "real_earnings", "real_tr_scaled_earnings", "cyclically_adjusted_price_earnings_ratio_p_e10_or_cape", "unnamed_13", "cyclically_adjusted_total_return_price_earnings_ratio_tr_p_e10_or_tr_cape", "excess_cape_yield", "monthly_total_bond_returns", "real_total_bond_returns", "unnamed_21", "unnamed_22", "unnamed_23", "unnamed_24", "drawdown_20pct_24m"]

## Public description

Title: Forecast Probability of 20% Real Drawdown within 24 Months (U.S. Equities, 1871–Present)

Problem statement
You are given monthly macro/market indicators for the U.S. equity market spanning 1871 to recent years. Your task is to build a model that, for each month, estimates the probability that the real total return index will experience a peak-to-trough drawdown of at least 20% within the subsequent 24 months. Submit well-calibrated probabilities for the held-out test months.

Data description
Each row corresponds to one calendar month. Features include equity price/earnings/dividends, CPI, long-term interest rates, the real total return price series, and valuation metrics such as CAPE. All features are contemporaneous or lagged indicators. Forward-looking return fields are not included in the released competition files.

Files provided
- train.csv: Training set with features and the target label.
- test.csv: Test set with the same features (without the target).
- sample_submission.csv: A sample submission with random but valid probabilities aligned to the test set rows.

Target label
- Column name: drawdown_20pct_24m
- Definition: 1 if, starting from month t, the maximum peak-to-trough decline of the Real Total Return Price over months t..t+24 (inclusive) reaches at least -20% in real terms; 0 otherwise.

Submission format
- A CSV with the following columns:
  - row_id: Unique identifier corresponding to each row in test.csv
  - probability: Your predicted probability that drawdown_20pct_24m = 1 for that row
- The file must contain exactly one row per row_id from test.csv, with no duplicates or missing rows. Probabilities must be numeric and will be clipped to [0, 1] during scoring.

Evaluation metric
- Submissions are evaluated using Average Precision (area under the precision–recall curve, AP/PR-AUC) over the binary target. AP is appropriate for imbalanced event data and rewards models that rank true drawdown events highly while producing well-calibrated probabilities.

Recommended modeling notes
- Treat the data as a time series. Use only information available up to each prediction month; the provided features are leakage-safe. You may build additional lagged and rolling features, normalize based on the training set, and train any classification model that outputs probabilities.
- The split is chronological to emulate real-world deployment. Your model should generalize across regimes with potential structural breaks.

Important details
- The Real Total Return Price is the canonical series for both momentum-style features and the target construction.
- All dates are monthly; using time-aware cross-validation for your local validation is recommended.
- The released files avoid forward-looking indicators and exclude rows that cannot be labeled due to insufficient forward window.

Good luck building robust probability forecasts of major drawdowns across 150+ years of market history!
