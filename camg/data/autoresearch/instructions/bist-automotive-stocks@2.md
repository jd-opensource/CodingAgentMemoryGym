# OpenMLE-fast task

Task ID: `bist-automotive-stocks@2`

Native metric: `BISTAutomotiveRankingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3972 bytes)
- `data/sample_submission.csv` (50628 bytes); columns: ["row_id", "prediction"]
- `data/test.csv` (140658 bytes); columns: ["row_id", "date", "stock_name", "open", "high", "low", "close", "adj_close", "volume", "daily_return"]
- `data/train.csv` (956070 bytes); columns: ["row_id", "date", "stock_name", "open", "high", "low", "close", "adj_close", "volume", "daily_return", "next_day_return"]

## Public description

Competition: BIST Automotive Cross-Sectional Ranking (Next-Day Return IC)

Problem statement
You are given a complete daily OHLCV panel for 8 BIST-listed automotive stocks. At the end of each trading day t, your task is to assign a score to each stock such that higher scores correspond to higher close-to-close return on the next trading day t+1. Your submission will be evaluated by the average cross-sectional Spearman rank correlation (Information Coefficient, IC) between your scores on day t and realized next-day returns on day t+1, computed per date and then averaged across all test dates.

Files provided
- train.csv: Historical panel with features and the training label next_day_return. One row represents one stock at one date t, with label equal to close-to-close return from t to t+1.
- test.csv: Panel for the test period with the same columns as train.csv except that next_day_return is not included.
- sample_submission.csv: Template with the required submission format.

Columns
Both train.csv and test.csv contain the following columns:
- row_id: Unique identifier for each row. Use this to align your predictions to rows in test.csv.
- date: Trading date t.
- stock_name: Stock identifier (categorical). All 8 stocks appear for each trading date in-sample; the test period also contains all 8 per date.
- open, high, low, close, adj_close, volume: End-of-day OHLCV features for date t.
- daily_return: The same-day close-to-close return for date t, included as an additional feature.
- next_day_return: Only in train.csv. The close-to-close return from t to t+1 that you are asked to rank and predict.

Target definition
- next_day_return = 100 * (close_{t+1} / close_t - 1), computed per stock.
- For a given date t, the evaluation compares your scores at t with the realized next_day_return observed at t+1 for the same stocks.

Submission format
- A CSV with exactly two columns:
  - row_id: Must match the row_id values in test.csv exactly (one prediction per row, no duplicates or missing rows).
  - prediction: A real-valued score. Any monotonic transformation (e.g., scaling) does not affect the metric.

Evaluation metric (primary)
- Mean Spearman rank correlation (IC) by date:
  1) For each test date d, compute Spearman rank correlation between your predictions and the true next_day_return across the 8 stocks.
  2) The final score is the simple average of these per-date correlations across all test dates.
- Numerical stability and edge cases:
  - If either vector within a date has zero variance (e.g., all equal predictions), the per-date correlation is defined as 0 for that date.
  - Non-finite values (NaN/inf) in predictions are not allowed; submissions containing them will be rejected.

Data split
- The split is strictly time-based. Training covers the earlier period; testing covers the most recent period. The dataset uses only dates where all 8 stocks are present and a well-defined next_day_return exists for each.
- No shuffling is used. There is no validation set provided; participants are encouraged to create their own time-based validation splits.

Key rules and guidance
- No leakage: Use only information available up to and including date t to build features and models. Rolling statistics must be computed with past data only.
- Cross-sectional handling: The evaluation is per-date across all 8 stocks. Cross-sectional normalization (e.g., z-scoring by date) and market-neutralization are commonly helpful.
- Modeling suggestions: Momentum/mean-reversion features, volatility and volume shocks, multi-horizon lags, calendar effects, and regularized models or gradient-boosted trees often perform well on this type of problem.

Final data files
- train.csv
- test.csv
- sample_submission.csv

What matters
- Build a robust pipeline for time-series feature engineering and modeling that generalizes under non-stationarity.
- Optimize cross-sectional ranking skill rather than absolute error or directional accuracy.
