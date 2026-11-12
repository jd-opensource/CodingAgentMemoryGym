# OpenMLE-fast task

Task ID: `stock-prices-of-the-10-largest-fast-food-companies@2`

Native metric: `RealizedVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4097 bytes)
- `data/sample_submission.csv` (55308 bytes); columns: ["row_id", "prediction"]
- `data/test.csv` (208607 bytes); columns: ["row_id", "Ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (8633332 bytes); columns: ["row_id", "Ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "target_log_rv5"]

## Public description

Competition: 5-Day Realized Volatility Forecasting (Fast-Food Giants)

Problem statement
Participants must forecast the next 5 trading days’ realized volatility for stocks of 10 fast‑food–related tickers. For each eligible ticker–date in the test period, submit a point forecast of the 5‑day ahead realized volatility target (defined below). The challenge is multi-series, strictly out‑of‑sample, and designed to reward robust modeling across assets with different scales and histories.

Data description
- Source universe: 10 tickers (fast‑food sector and related holdings). Daily OHLCV are provided per ticker as consolidated rows.
- Provided files for this competition:
  - train.csv: Modeling data containing historical rows with features and the target.
  - test.csv: Evaluation data with the same features but without the target.
  - sample_submission.csv: Example submission format with randomized predictions.

Columns
Each row corresponds to a specific (Ticker, Date).
- row_id: Unique identifier of the row; used to merge your predictions with the evaluator.
- Ticker: Stock ticker symbol.
- Date: Trading date (YYYY-MM-DD).
- Open, High, Low, Close, Adj Close, Volume: Daily OHLCV features.
- target_log_rv5 (train.csv only): The natural log of 5‑day realized volatility, defined below.

Label construction (target)
- Daily range-based variance (Parkinson): v_t = [ln(High_t / Low_t)]^2 / (4 * ln(2)).
- 5‑day realized volatility for date t: sigma_5(t) = sqrt( v_{t+1} + v_{t+2} + v_{t+3} + v_{t+4} + v_{t+5} ).
- Target used for training and evaluation: target_log_rv5(t) = ln( sigma_5(t) ).
Notes:
- Rows with undefined labels (insufficient future window or invalid High/Low) are excluded from train/test.
- Labels depend only on future High/Low; provided features are contemporaneous (t) OHLCV so you can derive any past-only features you need.

Train/test split
- Temporal split to prevent leakage.
- Train: All rows with Date strictly before 2024-01-01 (with valid target).
- Test: Rows with Date from 2024-01-01 onward, up to the last date where the 5‑day target is defined (varies by ticker).

What you can do
- You may engineer features from past data only (lags, rolling stats, technical indicators, calendar features).
- You may use cross‑asset features using histories of other tickers, provided you avoid using any information beyond date t.
- You may use any ML approach (e.g., linear models, tree ensembles, gradient boosting, GARCH/HAR variants, RNN/TCN/Transformer) as long as your pipeline respects causality.

Submission format
- A CSV file with the following columns:
  - row_id: Must exactly match the row_id values in test.csv.
  - prediction: Your forecast for target_log_rv5 (a real number; finite).
- The number of rows and row_ids must match test.csv exactly.

Evaluation metric
- Per-ticker RMSE on the log-volatility target:
  1) For each ticker s, compute RMSE_s = sqrt( mean( (prediction - target_log_rv5)^2 ) ) over all test rows of ticker s.
  2) Leaderboard score = mean_s( RMSE_s ) — the simple average across all tickers present in the test set.
Rationale: Using the natural log of realized volatility stabilizes heavy tails and creates a scale‑aware but fair objective. Averaging RMSE per ticker prevents larger or more active tickers from dominating the score.

Important details
- Handle missing/invalid values robustly in your pipeline. Nonpositive High or Low should be filtered when computing range-based measures.
- Do not use any information from dates beyond t when constructing features for row t.
- The target is evaluated in log space, so predictions can be any finite real number (negative or positive).

Deliverables available to participants
- train.csv (includes target_log_rv5)
- test.csv (no target)
- sample_submission.csv (row_id, prediction)

Tips
- Start with simple volatility baselines (e.g., rolling log-range or HAR-style features) and then extend with richer ML models.
- Consider regime shifts, volatility clustering, and differences in listing ages across tickers.

Good luck and happy modeling!
