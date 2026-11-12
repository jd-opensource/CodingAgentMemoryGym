# OpenMLE-fast task

Task ID: `apple-stock-prices-20152020@1`

Native metric: `AAPLNextDayAdjCloseForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3288 bytes)
- `data/sample_submission.csv` (2959 bytes); columns: ["date", "adjClose_next"]
- `data/test.csv` (12051 bytes); columns: ["date", "open", "high", "low", "close", "volume", "adjOpen", "adjHigh", "adjLow", "adjClose", "adjVolume", "divCash", "splitFactor"]
- `data/train.csv` (161972 bytes); columns: ["date", "open", "high", "low", "close", "volume", "adjOpen", "adjHigh", "adjLow", "adjClose", "adjVolume", "divCash", "splitFactor", "adjClose_next"]

## Public description

AAPL Next‑Day Adjusted Close Forecasting (2015–2020)

Problem statement
You are given daily OHLCV data for Apple Inc. (AAPL) from 2015-05-27 through 2020-05-22. For each trading day t, your task is to predict the next trading day’s adjusted closing price, denoted adjClose_next = adjClose at t+1. The test set provides the features observed on day t; you must forecast the adjusted close for the following trading day.

Why it’s challenging
- Regime shifts: Multiple market regimes (2018 sell-off, early-2020 COVID shock)
- Non-stationarity and heteroskedasticity
- Corporate actions: dividends and splits
- Strict time-ordering: features must not use any information from the future

Files provided
- train.csv — historical features and the target adjClose_next for model training
- test.csv — the feature rows for which you must predict adjClose_next
- sample_submission.csv — example of the expected submission format

Target and columns
- Target (to predict): adjClose_next (float), defined as the next trading day’s adjusted close relative to the row’s date.
- Key identifier: date (YYYY-MM-DD), the trading date whose features you observe. The ground-truth for that row is the adjusted close of the next trading day.
- Feature columns (available in both train and test):
  - open, high, low, close, volume
  - adjOpen, adjHigh, adjLow, adjClose, adjVolume
  - divCash, splitFactor
  Notes:
  - adjClose_next is present only in train.csv; it is not present in test.csv.
  - symbol is omitted (constant and uninformative).
  - Dates are strictly increasing with no duplicates. Next trading day refers to the next row chronologically (skips weekends/holidays automatically).

Train/test split
- Train period (feature dates): 2015-05-27 to 2019-12-31
- Test period (feature dates): 2020-01-02 to 2020-05-21
Rationale: Every test row’s target is the next trading day’s adjusted close and must exist within the provided history. The last feature date in test is chosen so that its next trading day’s adjusted close is available in the data.

Evaluation metric
Submissions are evaluated using Symmetric Mean Absolute Percentage Error (sMAPE) on adjClose_next across all test rows:
- For each row i: sMAPE_i = 200 * |y_i − ŷ_i| / (|y_i| + |ŷ_i|)
- Final score = mean_i(sMAPE_i)
Properties:
- Scale-free and symmetric between over/under-predictions
- Robust to price level changes across years
- Prices are strictly positive; nevertheless, numerical safeguards are applied during evaluation
Lower is better.

Submission format
- A CSV file with exactly two columns and a header: date, adjClose_next
- date must match the dates in test.csv (order does not matter; duplicates are not allowed)
- adjClose_next must be numeric, finite values (> 0 expected)

Modeling guidance (optional)
- Feature engineering: price/volume lags, rolling means/EMAs, volatility ranges (high−low, ATR), returns/log transforms, gaps (open − previous close), calendar effects, dividend/split indicators, adjusted vs raw spreads.
- Baselines: naive last adjusted close as next-day forecast; simple EMA-based forecasts; ARIMA/ETS; GBMs and tree ensembles; sequence models (TCN/LSTM/Transformer). Ensure no leakage by computing features using only information up to and including day t.
