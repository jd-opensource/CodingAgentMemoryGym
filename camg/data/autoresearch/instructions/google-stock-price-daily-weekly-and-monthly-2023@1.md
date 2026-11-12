# OpenMLE-fast task

Task ID: `google-stock-price-daily-weekly-and-monthly-2023@1`

Native metric: `GoogleStockReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2853 bytes)
- `data/sample_submission.csv` (5314 bytes); columns: ["id", "target"]
- `data/test.csv` (21098 bytes); columns: ["id", "Date", "freq", "Price", "High", "Low", "Close", "Volume", "AdjClose"]
- `data/train.csv` (245104 bytes); columns: ["id", "Date", "freq", "Price", "High", "Low", "Close", "Volume", "AdjClose", "target"]

## Public description

Google Stock Multi-Frequency Next-Period Return Forecasting

Problem statement
Build a model that predicts the next-period log-return of Google’s adjusted close price across three sampling frequencies: Daily, Weekly, and Monthly. For an observation at time t, predict y = log(AdjClose_{t+1}) − log(AdjClose_t). The test set contains rows from the year following the training period; labels are withheld.

Files provided
- train.csv: Long-format table containing labeled rows from all three frequencies. Columns:
  - id: Unique identifier per row (e.g., D_YYYY-MM-DD, W_YYYY-MM-DD, M_YYYY-MM-01)
  - Date: Timestamp of the observation
  - freq: One of {D, W, M}
  - Price, High, Low, Close, Volume, AdjClose: OHLCV features (AdjClose is split/dividend adjusted)
  - target: Next-step log-return y for the given row
- test.csv: Same columns as train.csv except target is omitted. Contains only the test windows. Each row requires predicting the next-step log-return.
- sample_submission.csv: Two columns [id, target] listing all ids from test.csv with placeholder predictions.

Target definition
For each frequency independently and in chronological order, the target is computed as:
  target = log(AdjClose[t+1]) − log(AdjClose[t])
The final terminal record for each frequency (where t+1 is undefined) is excluded from both train and test.

Train/test split
Time-based split with non-overlapping windows for each frequency:
- Daily (freq = D)
  - Train: up to and including 2022-03-31
  - Test: 2022-04-01 through 2023-03-30
- Weekly (freq = W)
  - Train: up to and including 2022-03-28 (week start dates)
  - Test: 2022-04-04 through 2023-03-20
- Monthly (freq = M)
  - Train: up to and including 2022-03-01 (first calendar day of month)
  - Test: 2022-04-01 through 2023-02-01

Evaluation metric
Your submission must be a CSV with two columns [id, target], one row per id in test.csv. The score is the macro-average Mean Absolute Error (MAE) of predicted log-returns across the three frequencies:
- Compute MAE separately within each frequency’s test subset: MAE_D, MAE_W, MAE_M
- Final score = (MAE_D + MAE_W + MAE_M) / 3

Rationale
- Log-returns are scale-invariant and robust to splits/dividends.
- Macro-averaging prevents the more numerous daily rows from dominating the score, encouraging balanced performance across horizons.

Notes and recommendations
- Use all OHLCV columns; participants may engineer features (e.g., technical indicators, volatility, momentum, cross-frequency context).
- Parse Date as a proper datetime and respect chronological ordering during any time-based modeling.
- No external data is required; models such as ARIMA/ETS, gradient boosting on engineered features, or sequence models (RNN/TCN/Transformers) are applicable.
- Ensure your submission contains every id exactly once and finite numeric predictions.
