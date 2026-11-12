# OpenMLE-fast task

Task ID: `us-dollar-index-data@1`

Native metric: `USDollarIndexReturnMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3050 bytes)
- `data/sample_submission.csv` (22675 bytes); columns: ["row_id", "target_5d_return"]
- `data/test.csv` (33017 bytes); columns: ["Date", "Open", "High", "Low", "Price", "row_id"]
- `data/train.csv` (270736 bytes); columns: ["Date", "Open", "High", "Low", "Price", "target_5d_return"]

## Public description

Title: 5-Day Ahead US Dollar Index Return Forecasting (Regression)

Problem statement
You are given a daily time series of the US Dollar Index (DXY) with OHLC prices. For each trading day t in the test set, predict the cumulative close-to-close return over the next 5 trading days:

  target_5d_return(t) = Close[t+5] / Close[t] - 1

The target is expressed as a decimal (e.g., 0.02 = +2%, -0.015 = -1.5%). This is a univariate financial forecasting task with rich temporal structure (trends, reversals, volatility clustering, calendar effects). Strong solutions will combine careful data processing, leakage-safe feature engineering, and robust modeling.

Files provided
- train.csv: Historical data with features and the target for supervised learning.
- test.csv: Historical data for which you must predict target_5d_return.
- sample_submission.csv: A template demonstrating the expected submission format.

Data description
Each row corresponds to one trading day. Columns:
- Date: Trading date in ISO format YYYY-MM-DD.
- Open: Opening value of the index on that date (float).
- High: High value of the index on that date (float).
- Low: Low value of the index on that date (float).
- Price: Closing value of the index on that date (float). (This is the "Close").
- target_5d_return: The 5-day ahead close-to-close return (present only in train.csv).
- row_id: Unique identifier for each row in test.csv (present only in test.csv and sample_submission.csv; do not use row_id as a predictive feature).

Train/test split
- Chronological split to simulate live forecasting.
- The target is defined for all rows where the close 5 days ahead exists. The final 5 unlabeled rows are excluded from training and testing.
- Train set: earliest 85% of the labeled time series.
- Test set: latest 15% of the labeled time series.
- No shuffling; strictly time ordered.

Evaluation metric
- Mean Absolute Error (MAE) on target_5d_return.
- Lower is better.

Submission format
- CSV file with exactly the following columns and no index column:
  - row_id: integer identifier matching test.csv.
  - target_5d_return: your predicted numeric value for that row (decimal return).
- The set of row_id in your submission must exactly match those in test.csv.

Modeling notes and guidance
- You may create any features you like using only information available up to and including day t when predicting target_5d_return(t). Examples: lagged returns, moving averages, rolling volatility, OHLC ranges (e.g., High-Low, True Range), candlestick encodings, and calendar features.
- Be careful to avoid look-ahead leakage beyond day t when constructing features.
- The data are nonstationary and exhibit structural breaks (e.g., macro cycles, crises). Robust regularization and careful validation strategies (e.g., time-based CV) are recommended.

Integrity and constraints
- Do not attempt to infer any future information beyond the provided train/test split.
- Submissions must contain finite numeric predictions for all required row_id.

Good luck and happy forecasting!
