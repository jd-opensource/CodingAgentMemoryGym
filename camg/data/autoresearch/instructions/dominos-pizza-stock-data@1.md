# OpenMLE-fast task

Task ID: `dominos-pizza-stock-data@1`

Native metric: `DPZNextDayReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2901 bytes)
- `data/sample_submission.csv` (6414 bytes); columns: ["Id", "target"]
- `data/test.csv` (12597 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
- `data/train.csv` (25927 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "target"]

## Public description

Competition: DPZ Next-Day Log-Return Forecast (OHLCV)

Problem statement
Participants must predict the next trading day’s adjusted close log return for Domino’s Pizza (DPZ) from daily OHLCV data. For each row in test.csv representing day t, the target is r_{t+1} = ln(AdjClose_{t+1} / AdjClose_t). Only information available up to and including day t may be used.

Files provided
- train.csv: Training rows for days t with columns: Id, Date, Open, High, Low, Close, Adj Close, Volume, target. The target column is the next-day adjusted close log return.
- test.csv: Test rows for days t with columns: Id, Date, Open, High, Low, Close, Adj Close, Volume. No target column is provided.
- sample_submission.csv: Submission template with columns: Id, target.

Target definition
- For a given day t, target = ln(AdjClose_{t+1} / AdjClose_t), where AdjClose_{t+1} is the adjusted close of the next trading day. The test rows are constructed so that every t has a valid next trading day within the dataset.

Train/test split
- Temporal split is used to simulate forward-in-time generalization across market regimes:
  - Train period: 2019-10-16 up to the last t whose next trading day is on or before 2020-12-31
  - Test period: 2021-01-01 to the final t for which a next trading day exists within the data
The data is sorted ascending by Date, and there is no overlap or leakage between train and test.

Evaluation
- Submissions must be a CSV with columns: Id, target
- The score is Root Mean Squared Error (RMSE) between the submitted target and the ground truth target:
  RMSE = sqrt(mean((y_pred - y_true)^2))
- RMSE on log returns is scale-invariant, symmetric for up/down errors, and emphasizes large-miss days.

Rules and guidance
- Use only information available up to day t to predict r_{t+1}. Rolling/lagged features are encouraged, but avoid any forward-looking computations that could leak information beyond day t.
- Date may be used for temporal ordering and time-based features (e.g., day-of-week), but it should not be used to infer future labels.
- You may apply any modeling approach suitable for regression on time series (e.g., linear models with regularization, tree-based models, or neural sequence models). Consider non-stationarity and regularization.

Submission format
- Required header: Id,target
- Ids must match exactly the Ids in test.csv. No extra or missing rows are allowed, and there must be no duplicate Ids.

Tips
- Feature ideas include returns and ranges derived from OHLC (e.g., log returns, close-to-open gaps, high–low range), rolling means/volatility, volume transforms, candlestick encodings, and volatility estimators (e.g., Parkinson, Garman–Klass). Ensure all features are strictly lagged.
- Due to the short horizon and limited sample size, prefer careful cross-validation (e.g., rolling windows) and conservative model complexity to avoid overfitting.
