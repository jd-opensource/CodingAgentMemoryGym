# OpenMLE-fast task

Task ID: `microsoft-stock-price2000-2023@2`

Native metric: `MsftVolatilityForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3345 bytes)
- `data/sample_submission.csv` (10961 bytes); columns: ["Id", "log_RV10"]
- `data/test.csv` (36062 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (492928 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "log_RV10"]

## Public description

Microsoft 10-Day Realized Volatility Forecasting

Problem statement
Given daily OHLCV data for Microsoft across multiple market regimes (2000–2023), predict the next-10-trading-day annualized realized volatility for each trading day t, evaluated on the log scale.
- Target: y_t = log(RV10_t)
- RV10_t = sqrt((252/10) * Σ_{i=1..10} r_{t+i}^2), where r_{t+i} = log(AdjClose_{t+i} / AdjClose_{t+i-1})
- 252 trading days/year are used for annualization.

This is a time-series regression task. Features for day t must only use information available up to and including t (no look-ahead).

Files provided
- train.csv: Training rows with raw features and the target.
  - Columns: Id, Date, Open, High, Low, Close, Adj Close, Volume, log_RV10
  - Date is formatted as YYYY-MM-DD.
- test.csv: Same schema as train.csv but without the log_RV10 column.
- sample_submission.csv: A valid example submission with columns Id,log_RV10.

Train/test split
- Chronological split.
  - Train: up to and including 2021-12-31 (all rows whose labels can be computed and occur on or before this date).
  - Test: 2022-01-03 through 2023-11-08 (inclusive). All test rows have exactly 10 future trading days within the file to define their labels; the final 10 trading days of the source timeline are excluded from labeling by construction.

What you can do
- Use the provided OHLCV and calendar information to engineer features using only information available on or before day t.
- Typical useful features:
  - Returns/momentum: past 1/2/3/5/10/20/60-day log returns; moving averages/EMAs; rolling mean/std; z-scores.
  - Range/volatility: ATR; Parkinson and Garman–Klass estimators from OHLC; rolling realized variance of past windows; intraday range (High−Low)/Open; close-in-range location.
  - Volume/liquidity: Volume and log-Volume levels and z-scores; volume momentum; price–volume interactions.
  - Calendar: day-of-week, month, year, month-end/quarter-end flags; trading-day-in-month.
- Any regression model is allowed (e.g., linear/HAR, ridge/Lasso, tree ensembles/GBMs, or sequence models). Ensure that cross-validation respects time order (e.g., forward chaining).

Submission format
- A CSV with exactly two columns and a header: Id,log_RV10
- Id must match the Id values in test.csv exactly (one row per test Id, no duplicates/missing).
- log_RV10 must be finite numeric predictions on the log-volatility scale (do not exponentiate).

Evaluation
- Metric: Root Mean Squared Error (RMSE) on the log-volatility targets.
  - RMSE = sqrt(mean_t (ŷ_t − y_t)^2)
- Rationale: The log transform stabilizes variance, emphasizes relative errors, and yields a standard, strictly proper scoring rule for volatility forecasting.

Rules and guidance
- No leakage: Any rolling/windowed features must be computed using past-only data relative to t. Do not use t+1 or beyond when building features for t.
- External data is not required; if you use any, ensure it would have been available at time t and does not introduce look-ahead bias.
- Handle numerical stability carefully (e.g., logs, standardization). Ensure predictions are finite.

Deliverable
- Submit a single CSV with columns Id and log_RV10 corresponding to the rows in test.csv.

Good luck—design robust features, control leakage, and build strong forecasters across 23 years of market regimes!
