# OpenMLE-fast task

Task ID: `microsoft-stock-time-series-analysis@2`

Native metric: `MicrosoftVolatilityForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2701 bytes)
- `data/sample_submission.csv` (7093 bytes); columns: ["row_id", "y"]
- `data/test.csv` (322977 bytes); columns: ["row_id", "date", "close", "open", "high", "low", "ret_1", "ret_mean_5", "ret_std_5", "rv_5", "ret_skew_5", "ret_kurt_5", "ret_mean_10", "ret_std_10", "rv_10", "ret_skew_10", "ret_kurt_10", "ret_mean_20", "ret_std_20", "rv_20", "ret_skew_20", "ret_kurt_20", "ret_mean_60", "ret_std_60", "rv_60", "ret_skew_60", "ret_kurt_60", "atr_5", "parkinson_rv_5", "gk_rv_5", "atr_10", "parkinson_rv_10", "gk_rv_10", "atr_20", "parkinson_rv_20", "gk_rv_20", "atr_60", "parkinson_rv_60", "gk_rv_60", "sma_5", "px_sma_ratio_5", "sma_10", "px_sma_ratio_10", "sma_20", "px_sma_ratio_20", "sma_60", "px_sma_ratio_60", "ema12", "ema26", "macd", "macd_signal", "macd_hist", "bb_width_20", "rsi_14", "log_vol", "vol_roc_1", "vol_z_20", "drawdown_60", "dow", "month", "quarter", "dom", "is_month_end"]
- `data/train.csv` (1220104 bytes); columns: ["row_id", "date", "close", "open", "high", "low", "ret_1", "ret_mean_5", "ret_std_5", "rv_5", "ret_skew_5", "ret_kurt_5", "ret_mean_10", "ret_std_10", "rv_10", "ret_skew_10", "ret_kurt_10", "ret_mean_20", "ret_std_20", "rv_20", "ret_skew_20", "ret_kurt_20", "ret_mean_60", "ret_std_60", "rv_60", "ret_skew_60", "ret_kurt_60", "atr_5", "parkinson_rv_5", "gk_rv_5", "atr_10", "parkinson_rv_10", "gk_rv_10", "atr_20", "parkinson_rv_20", "gk_rv_20", "atr_60", "parkinson_rv_60", "gk_rv_60", "sma_5", "px_sma_ratio_5", "sma_10", "px_sma_ratio_10", "sma_20", "px_sma_ratio_20", "sma_60", "px_sma_ratio_60", "ema12", "ema26", "macd", "macd_signal", "macd_hist", "bb_width_20", "rsi_14", "log_vol", "vol_roc_1", "vol_z_20", "drawdown_60", "dow", "month", "quarter", "dom", "is_month_end", "y"]

## Public description

Title: 10-Day Realized Volatility Forecasting for Microsoft (Regression)

Problem statement
- Given Microsoft’s historical daily OHLCV data up to an anchor trading day T, predict the log of the annualized realized volatility over the next 10 trading days (T+1 to T+10), computed from close-to-close log returns. This is a univariate time-series forecasting task focused on future volatility, not price direction.

Target definition
- Let r_t = log(Close_t) − log(Close_{t−1}).
- Realized volatility over the next 10 trading days is RV_{T+1:T+10} = sqrt(252) * sqrt( (1/10) * sum_{i=1..10} r_{T+i}^2 ).
- The prediction target is y_T = log(RV_{T+1:T+10}).

Data provided
- train.csv: Feature matrix and labels for anchor days up to the split date. Columns include an integer row_id, a timestamp date column, a rich set of time-series features built using only information available up to and including T, and the target column y (log 10-day annualized realized volatility).
- test.csv: Same schema as train.csv but without the target. Includes row_id and date along with the feature matrix for each test anchor.
- sample_submission.csv: A template containing row_id and an example y column with valid values. Replace y with your model’s predictions.

What you can use
- All engineered features in train/test were derived strictly from historical OHLCV data up to the anchor day. You are free to use these features as-is, engineer additional features from them, and train any ML model. External data is not required.

Train/test split
- Chronological split. Train anchors start from the first available date and run up to 2019-12-31. Test anchors start on 2020-01-02 and end at the last anchor for which a full 10-day future window exists within the dataset period.

Evaluation
- Submissions are evaluated by Root Mean Squared Error (RMSE) on the log volatility target:
  RMSE = sqrt( mean( (y_pred − y_true)^2 ) )
- The metric is computed over all test anchors and is deterministic and scale-aware. Using the log of volatility stabilizes variance across market regimes and ensures positivity of the implied volatility.

Submission format
- CSV with two columns and header: row_id,y
- Each row_id must appear exactly once and match those in test.csv.

Notes and constraints
- Features are computed with no look-ahead leakage: only data available up to each anchor day T was used.
- All files are provided in standard CSV format; do not add file paths in CSV fields.
- You do not need to use every feature; careful feature selection, regularization, and time-aware validation are encouraged.
- Because the 2020–2021 period contains regime shifts, models should be robust to non-stationarity.
