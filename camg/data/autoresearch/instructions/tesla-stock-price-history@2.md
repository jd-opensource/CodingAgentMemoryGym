# OpenMLE-fast task

Task ID: `tesla-stock-price-history@2`

Native metric: `NextDayVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3275 bytes)
- `data/sample_submission.csv` (15064 bytes); columns: ["Id", "NextDayParkinsonVol"]
- `data/test.csv` (55367 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Volume"]
- `data/train.csv` (393719 bytes); columns: ["Id", "Date", "Open", "High", "Low", "Close", "Volume", "NextDayParkinsonVol"]

## Public description

Competition: Next-Day Realized Volatility Forecasting for Tesla (TSLA)

Background
Volatility is a central quantity in trading, risk management, and option pricing. Accurately forecasting short-horizon volatility helps with position sizing, hedging, and scenario analysis. This challenge focuses on predicting Tesla’s next-day realized volatility using daily OHLCV data.

Problem Statement
Given day-t information (Open, High, Low, Close, Volume) for Tesla, predict the next day’s realized volatility (t+1) using a robust high–low based proxy. This is a pure forecasting task: your features should be derived from information available up to and including day t only.

Data Description
- train.csv: Chronologically ordered daily records with columns [Id, Date, Open, High, Low, Close, Volume, NextDayParkinsonVol]. The target column NextDayParkinsonVol is the realized volatility proxy for day t+1.
- test.csv: Same format as train.csv but without the target column. Ids in test.csv identify the rows for which you must submit predictions.
- sample_submission.csv: Example submission file with columns [Id, NextDayParkinsonVol]. Use this as a template for your submission.

Target Definition
We use the Parkinson realized volatility proxy based on next-day high and low:
NextDayParkinsonVol(t) = sqrt((ln(High_{t+1}/Low_{t+1}))^2 / (4 ln 2)) = |ln(High_{t+1}/Low_{t+1})| / sqrt(4 ln 2).
This proxy reduces noise compared to close-to-close returns and depends only on the next day’s high/low.

Train/Test Split
A strict time-aware split is used to preserve forecasting integrity:
- Train: the first 85% of usable labeled samples.
- Test: the last 15% of usable labeled samples.
There is no shuffling; models must learn from past to predict future.

Evaluation Metric
Submissions are evaluated using Mean Absolute Error (MAE) between your predictions and the ground truth NextDayParkinsonVol for the test set:
MAE = mean(|y_pred − y_true|). Lower is better.
MAE is robust to outliers and appropriate for positive, heavy-tailed volatility values.

Submission Format
- File must contain exactly two columns in this order: Id and NextDayParkinsonVol.
- Ids must exactly match those provided in test.csv (same set and count, order does not matter).
- Predictions must be numeric, finite, and non-negative.

Modeling Guidance
- Avoid leakage: features for day t must not use any information from t+1 or beyond.
- Use chronological validation during development (e.g., rolling or expanding windows, walk-forward) to mimic the competition’s test regime.
- Feature engineering ideas include: rolling ranges and ATR; Garman–Klass, Rogers–Satchell, and other high–low–open–close volatility proxies at time t; lagged close returns; volatility-of-volume; range/return/volume spikes; candle pattern indicators; regime flags; non-stationarity-handling transforms.
- You may use any ML/TS model (e.g., linear models, tree ensembles, GARCH/HARCH, LSTM/TCN, Prophet-style regressors) provided the training process avoids future information.

Notes
- Date is provided to preserve chronological order. If you derive calendar features (e.g., day-of-week), ensure they do not leak future prices.
- The dataset uses the full available daily history; no subsampling is applied.
