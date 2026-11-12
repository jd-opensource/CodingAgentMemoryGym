# OpenMLE-fast task

Task ID: `microsoft-stock-price-history@1`

Native metric: `MicrosoftStockMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2895 bytes)
- `data/sample_submission.csv` (18110 bytes); columns: ["row_id", "Up"]
- `data/test.csv` (196692 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Close", "Volume"]
- `data/train.csv` (810405 bytes); columns: ["row_id", "Date", "Open", "High", "Low", "Close", "Volume", "Up"]

## Public description

MSFT Next-Day Direction Prediction (Daily OHLCV)

Problem statement
Participants are asked to build a model that, for each trading day t, predicts the probability that Microsoft’s closing price on day t+1 will be higher than the close on day t. This is framed as a binary probabilistic classification task on daily OHLCV time series data.

Data description
- train.csv: Contains the historical daily records and the binary target for training. Columns:
  - row_id: Unique identifier for each row in train
  - Date: Trading date (YYYY-MM-DD)
  - Open, High, Low, Close: Daily OHLC prices
  - Volume: Daily trading volume
  - Up: Binary label, where Up = 1 if Close(t+1) > Close(t), else 0
- test.csv: Same feature schema as train.csv but without the Up column. Your task is to predict the probability of Up for each row in test.csv.
- sample_submission.csv: Example submission file demonstrating the required format. It contains:
  - row_id: Matches the row_id in test.csv
  - Up: Your predicted probability that the next day’s close is higher than the current close (values in [0, 1])

Train/test split policy
- The split is strictly chronological to mimic real forecasting and prevent leakage. The training period covers earlier dates, while the test period covers later, out-of-time dates. All labels are derived deterministically from the observed Close series as Up = 1 if Close(t+1) > Close(t), else 0.
- The last available day (which has no next-day label) is excluded from both train and test.

Target and features
- Target: Up (binary), defined from consecutive closes as above.
- Features provided: Date and OHLCV (Open, High, Low, Close, Volume). You are encouraged to engineer additional features (e.g., returns, rolling statistics, technical indicators, calendar features) using only information available up to and including day t. Do not use any t+1 information when constructing features for day t.

Evaluation
- Submissions are evaluated using Binary Log Loss (cross-entropy) between your submitted probabilities and the hidden ground truth labels in the test set:
  LogLoss = -mean( y*log(p) + (1-y)*log(1-p) ), with standard clipping to avoid log(0).
- This metric fairly rewards both accuracy and calibration of probabilistic forecasts.

Submission format
- A valid submission is a CSV file with exactly two columns and a header:
  - row_id: Must match the row_id values in test.csv exactly and appear once each
  - Up: A probability in [0, 1] for each row_id

What makes this competition challenging
- Financial time series are noisy and non-stationary. Market regimes, volatility clustering, and structural changes make generalization difficult. Robust preprocessing, careful feature engineering (returns/ratios, rolling stats), and calibrated probabilistic models are essential for strong performance.

Files you will use
- train.csv
- test.csv
- sample_submission.csv
