# OpenMLE-fast task

Task ID: `amazon-stocks-2025@1`

Native metric: `AmazonStockDirectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3102 bytes)
- `data/sample_submission.csv` (38975 bytes); columns: ["Date", "Up"]
- `data/test.csv` (122172 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume", "Stock_Splits"]
- `data/train.csv` (558267 bytes); columns: ["Date", "Open", "High", "Low", "Close", "Volume", "Stock_Splits", "Up"]

## Public description

AMZN Next-Day Direction: Probabilistic Forecasting Challenge

Problem statement
Predict the probability that Amazon (AMZN) stock’s next trading day close-to-close return is positive. For each evaluation date t, you must submit a calibrated probability that Close(t+1) > Close(t).

Data description
- Source: Historical daily OHLCV with corporate action metadata across multiple regimes (1997–2025).
- Fields provided in the competition files:
  - Date: Trading date in YYYY-MM-DD format (unique per row)
  - Open, High, Low, Close: Daily price fields (split-adjusted)
  - Volume: Daily traded volume
  - Stock_Splits: Stock split ratio indicator for the date (0 if no split; positive otherwise)
  - Up (train only): Binary target, 1 if Close(t+1) > Close(t), else 0

Files
- train.csv: All features with the Up target for the training period.
- test.csv: All features for the test period (no target column).
- sample_submission.csv: Example submission file with all evaluation dates and a column named Up containing valid probabilities.

Target definition
For each row (date t), Up = 1 if Close on the next trading day is greater than Close on date t, otherwise 0. The last available trading day is excluded from evaluation because its next day does not exist.

Train/test split
- Chronological split to reflect real-world forecasting.
- Train covers the earlier period; test covers the later period. Dates are strictly ordered without overlap.
- Only train.csv contains the target column Up; test.csv does not include labels.

Submission format
- CSV with two columns: Date, Up
  - Date: Must exactly match the evaluation dates in test.csv
  - Up: A probability in [0, 1] representing P(Up = 1)
- The number of rows and the set of Date values must match test.csv exactly. Extra/missing rows or out-of-range values will result in an invalid submission.

Evaluation
- Metric: Binary cross-entropy (log loss)
  - For each evaluation row i with true label y_i ∈ {0,1} and submitted probability p_i ∈ [0,1], the score is:
    LogLoss = - (1/N) * Σ [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]
  - Probabilities are clipped to a small epsilon to avoid log(0).
- Lower is better. Well-calibrated, confident-but-correct predictions achieve lower scores.

Notes and recommendations
- Markets are non-stationary; expect regime shifts (e.g., dot-com era, 2008 GFC, COVID-19, 2022 stock split). Use robust validation and avoid leakage from the future.
- Feature engineering ideas: lagged returns, volatility measures, technical indicators (e.g., moving averages, RSI, Bollinger Bands), volume/price interactions, split-event indicators, and calendar effects.
- Modeling options: logistic regression with time-series features, gradient boosting, temporal CNN/RNN/Transformers, and ensemble methods.
- Dividends are not included because they are constant zero in this dataset and provide no signal.

Deliverables
- Submit a single CSV named however you like that follows the Submission format above. Your submission will be scored using the LogLoss metric against the held-out labels for the test period.
