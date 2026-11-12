# OpenMLE-fast task

Task ID: `stock-tweets-for-sentiment-analysis-and-prediction@1`

Native metric: `StockMoveFromTweetsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5241 bytes)
- `data/sample_submission.csv` (10944 bytes); columns: ["id", "up_probability"]
- `data/test.csv` (95305 bytes); columns: ["id", "stock", "date", "open", "high", "low", "close", "volume", "ret_1d", "ret_5d", "vol_5d", "range_d", "volume_z_20d"]
- `data/test_tweets.csv` (978309 bytes); columns: ["date", "stock", "tweet_time", "tweet"]
- `data/train.csv` (1174729 bytes); columns: ["id", "stock", "date", "open", "high", "low", "close", "volume", "ret_1d", "ret_5d", "vol_5d", "range_d", "volume_z_20d", "target"]
- `data/train_market.csv` (543164 bytes); columns: ["date", "stock", "open", "high", "low", "close", "volume"]
- `data/train_targets.csv` (1174729 bytes); columns: ["id", "stock", "date", "open", "high", "low", "close", "volume", "ret_1d", "ret_5d", "vol_5d", "range_d", "volume_z_20d", "target"]
- `data/train_tweets.csv` (16081187 bytes); columns: ["date", "stock", "tweet_time", "tweet"]

## Public description

Competition: Next-day Stock Move Classification from Tweets + OHLCV (multimodal, time-aware)

Problem statement
Given a stock and a calendar day D, predict the probability that the next trading day’s close-to-close return is positive ("up"). You must use only information available up to and including day D: the raw tweets for that stock on day D and historical market data up to D (no future information).

What you will build
Participants will build a model that ingests text signals from daily tweets and numerical signals from market prices/volume to forecast the next day’s direction. You will submit a probability for “up” for every (stock, date) in the test set.

Files provided
Train files
- train_targets.csv: One row per (stock, date) in the training period. Columns include:
  - id: unique identifier for the sample
  - stock: stock ticker (one of 25 tickers)
  - date: calendar date (YYYY-MM-DD)
  - open, high, low, close, volume: OHLCV for date D
  - ret_1d, ret_5d, vol_5d, range_d, volume_z_20d: engineered market features computed using only data up to D (see Dataset details)
  - target: 1 if close(D+1) > close(D), else 0
- train_tweets.csv: All raw tweets whose UTC calendar date falls in the training period. Columns: date (YYYY-MM-DD), stock, tweet_time (UTC timestamp), tweet (text)
- train_market.csv: Raw daily OHLCV for all stocks for dates in the training period only (no test dates)

Test files
- test.csv: One row per (stock, date) to predict. Same columns as train_targets.csv except target is withheld.
- test_tweets.csv: All raw tweets whose UTC calendar date falls in the test period. Same columns as train_tweets.csv.
- sample_submission.csv: Submission template containing id and a random but valid up_probability for every test row.

Important notes
- The test set contains only dates for which the next trading day exists; the final trading day per stock is excluded.
- Raw market data (train_market.csv) is provided only up to the end of the training period to prevent any future leakage. For the test period, per-row OHLCV and engineered features for day D are included directly in test.csv.
- Tweets are provided raw for both train and test; you may aggregate/encode them as you see fit.

Dataset details and construction
- Base sources: 80K+ tweets across 25 tickers (UTC timestamps) and daily OHLCV for the same tickers over 2021-09-30 to 2022-09-30.
- Target definition: For each (stock, date=D), target = 1 if Close(D+1) > Close(D), else 0, where D+1 is the next available trading day for that stock.
- Feature columns in train_targets.csv and test.csv are computed without lookahead:
  - ret_1d = close/close.shift(1) - 1
  - ret_5d = close/close.shift(5) - 1
  - vol_5d = rolling standard deviation of daily returns over the last 5 days
  - range_d = (high - low) / close
  - volume_z_20d = z-score of volume relative to a 20-day rolling mean/std
  Missing values from insufficient lookback are filled with 0.

Train/test split
- Chronological split with no overlap. Training period: 2021-09-30 to 2022-08-31 (inclusive). Test period: 2022-09-01 to 2022-09-29 (inclusive) for all stocks where a next trading day exists.
- All rows are aligned by the UTC calendar date of the tweets and the market date.

Submission format
- CSV with the following columns:
  - id: the identifier from test.csv
  - up_probability: your model’s predicted probability that the next day’s close is higher than day D’s close
- Probability values must be finite numbers in [0, 1]. Each id must appear exactly once.

Evaluation metric
- Macro-averaged ROC-AUC across tickers:
  1) Compute ROC-AUC for each stock separately using that stock’s test rows.
  2) Average the per-stock AUCs to form the final score.
- Why this choice: ROC-AUC is threshold-independent and robust to class imbalance. Macro-averaging across tickers ensures each stock contributes equally, preventing domination by tweet- or trading-day-rich tickers.
- Edge case handling: If a stock’s test labels contain only one class, its AUC is defined as 0.5 for averaging.

Best practices and expectations
- Prevent leakage: Engineer features using only information available up to and including day D. Do not use any data from D+1 or later when constructing features for date D.
- Text handling: Clean URLs/mentions if desired, preserve cashtags, and consider sentence embeddings, TF-IDF, or other encoding. Aggregate per (stock, date) with sensible weighting if you use intra-day timing.
- Market features: Consider richer technical indicators (RSI, MACD, rolling z-scores, volatility measures) using train_market.csv. You may recompute your own indicators for both train and test using only information up to D.
- Modeling: Any ML method is allowed. Strong baselines include gradient boosting over engineered features and multimodal architectures combining text embeddings with market signals.

Deliverables
- Submit a single CSV matching sample_submission.csv with id and up_probability.

Reproducibility
- The provided prepare.py script deterministically constructs all files from the original raw CSVs and generates a random but valid sample_submission.csv. You can re-run it to reproduce the official train/test split and files.
