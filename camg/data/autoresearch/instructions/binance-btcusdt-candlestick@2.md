# OpenMLE-fast task

Task ID: `binance-btcusdt-candlestick@2`

Native metric: `BTCVolatilityForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3262 bytes)
- `data/sample_submission.csv` (25474 bytes); columns: ["row_id", "rv_24h"]
- `data/test.csv` (113106 bytes); columns: ["row_id", "kline_ot", "open_price", "high_price", "low_price", "close_price", "volume", "kline_ct", "quote_volume", "num_trades", "base_volume"]
- `data/train.csv` (530856 bytes); columns: ["row_id", "kline_ot", "open_price", "high_price", "low_price", "close_price", "volume", "kline_ct", "quote_volume", "num_trades", "base_volume", "rv_24h"]

## Public description

Title: 24h Realized Volatility Forecasting on BTC/USDT (1H OHLCV)

Problem statement
- For each 1-hour candlestick at time t, predict the next 24 hours’ realized volatility using only information available up to and including time t.
- Target definition: rv_24h(t) = sqrt(sum_{i=1..24} [log(C_{t+i} / C_{t+i-1})]^2), where C is the close_price. Labels exist only when t+24 is available.
- This is a univariate time series forecasting target with multivariate features (OHLCV, trades). The challenge is to model volatility clustering and regime shifts without leaking future information.

Data description
- Source series: 1-hour BTC/USDT candles (OHLCV + trades) from Binance, strictly hourly and contiguous.
- Feature columns per row (time t):
  - kline_ot, open_price, high_price, low_price, close_price, volume, kline_ct, quote_volume, num_trades, base_volume
- Files provided for the competition (participants may use either CSV or Excel versions):
  - train.csv / train.xlsx: features at time t plus the target column rv_24h
  - test.csv / test.xlsx: features at time t only; no target
  - sample_submission.csv: submission template with columns [row_id, rv_24h]

Indexing and identifiers
- Each row has a unique integer row_id that identifies the time t in the labeled index. The test set preserves ordering and row_id. The submission must predict rv_24h for every row_id in test.csv.

Train/test split
- Chronological split on the labeled index (no random shuffling). Approximately 80% train and 20% test, using only rows where a 24-hour label exists. The split ensures that training rows strictly precede test rows in time.

Submission format
- A CSV file with exactly two columns in this exact order:
  - row_id: integer
  - rv_24h: strictly positive real number (predicted realized volatility)
- The set of row_id must match test.csv exactly; duplicates or missing ids are not allowed.

Evaluation metric
- QLIKE loss on realized volatility, averaged over all test rows (lower is better). Let y be the true rv_24h and yhat the prediction. We compute the ratio r = (yhat^2)/(y^2), and the per-row loss L = r - log(r) - 1, which is minimized when yhat = y. The final score is mean(L) over the test set. Predictions must be positive; non-positive values will be clipped to a tiny positive epsilon internally for evaluation to ensure numerical stability.
- Rationale: QLIKE is standard in volatility forecasting; it is scale-invariant, penalizes under- and over-prediction asymmetrically in a calibrated manner, and is robust under heavy tails.

Rules and guidance
- Do not use any information beyond time t for each row in feature construction to avoid leakage (e.g., rolling features must be backward-looking only).
- You may engineer features from any provided columns and derive time-based signals (hour-of-day, day-of-week), rolling stats (e.g., past RV, realized range from high/low), and volume/trade microstructure proxies.
- The dataset is single-asset, single-frequency; robust validation should be time-based.

Files to expect
- train.csv, train.xlsx
- test.csv, test.xlsx
- sample_submission.csv

Good luck and enjoy building volatility models (HAR-RV, tree ensembles on engineered features, or sequence models are all great starting points)!
