# OpenMLE-fast task

Task ID: `binance-btcusdt-candlestick@1`

Native metric: `BTCUSDTLogReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2428 bytes)
- `data/sample_submission.csv` (25727 bytes); columns: ["row_id", "target_log_return_t_plus_1"]
- `data/test.csv` (112518 bytes); columns: ["row_id", "kline_ot", "open_price", "high_price", "low_price", "close_price", "volume", "kline_ct", "quote_volume", "num_trades", "base_volume"]
- `data/train.csv` (520426 bytes); columns: ["kline_ot", "open_price", "high_price", "low_price", "close_price", "volume", "kline_ct", "quote_volume", "num_trades", "base_volume", "target_log_return_t_plus_1"]

## Public description

Title: BTC/USDT Next-Hour Log-Return Forecasting (1H OHLCV)

Problem statement:
Predict the next hour’s log-return of the BTC/USDT close price using only information available up to the current candle close. At each 1-hour timestamp t, participants must forecast r_{t+1} = log(C_{t+1} / C_t), where C_t is the close_price at time t.

Data description:
You are given consecutive 1-hour candlestick data (OHLCV and trading activity) for BTC/USDT with no missing hours. Each row corresponds to one hour and includes:
- kline_ot (ms since epoch): open time of the candle
- open_price, high_price, low_price, close_price
- volume (in BTC), quote_volume (in USDT)
- kline_ct (ms since epoch): close time of the candle
- num_trades, base_volume (taker buy base asset volume)

Target definition:
- target_log_return_t_plus_1 = log(close_price[t+1] / close_price[t])
- The last candle in the original chronology has no t+1 and is not used.

Files provided:
- train.csv: All feature columns plus the target column target_log_return_t_plus_1 for the training portion of the timeline.
- test.csv: All feature columns and a row_id column for the test portion of the timeline. No target labels are included.
- sample_submission.csv: Expected submission format with row_id and target_log_return_t_plus_1. Values are placeholders to illustrate format only.

Submission format:
- CSV file with two columns and header:
  - row_id: integer identifier matching test.csv
  - target_log_return_t_plus_1: your predicted log-return for the next hour
- The number and order of row_id must match those in test.csv exactly.

Evaluation metric:
- Primary metric: Mean Absolute Error (MAE) between the submitted predictions and the hidden ground truth on target_log_return_t_plus_1.
- MAE is computed as the mean of absolute differences |y_true - y_pred| over all test rows.
- Lower is better.

Rules and guidance:
- This is a pure forecasting task. Use only information up to and including time t to construct features for predicting r_{t+1}. Avoid any leakage from future data.
- The data are strictly chronological; the split preserves time order. Participants are encouraged to use time-aware validation.
- Typical approaches include feature engineering (rolling statistics/indicators, seasonality), linear models, tree-based models, and sequence models.

Final train/test data files for the competition:
- train.csv
- test.csv
- sample_submission.csv
