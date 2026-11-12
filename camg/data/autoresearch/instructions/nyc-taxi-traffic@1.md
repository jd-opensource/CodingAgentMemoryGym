# OpenMLE-fast task

Task ID: `nyc-taxi-traffic@1`

Native metric: `NYCTaxiSmapeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2856 bytes)
- `data/sample_submission.csv` (51969 bytes); columns: ["timestamp", "value"]
- `data/test.csv` (26890 bytes); columns: ["timestamp"]
- `data/train.csv` (231244 bytes); columns: ["timestamp", "value"]

## Public description

NYC Taxi Passenger Forecasting (30-minute) — Deterministic Track

Problem statement
You are given a univariate time series of NYC taxi passenger counts aggregated in 30-minute buckets. Your task is to forecast the next 28 days (1,344 half-hour slots) of passenger counts at the same 30-minute frequency.

Why this is challenging
- Strong multi-seasonality: daily and weekly patterns at high frequency
- Event-driven deviations (e.g., holidays) and nonstationarity
- Multi-step forecasting with error accumulation risks

Files provided
- train.csv: historical data with two columns: timestamp,value
- test.csv: the exact future timestamps (1,344 rows) to predict; one column: timestamp
- sample_submission.csv: an example of a valid submission (timestamp,value)

Target
- value: the number of taxi passengers in the corresponding 30-minute interval

Submission format
- A CSV file with exactly two columns: timestamp,value
- The timestamp column must contain exactly the timestamps provided in test.csv (order can be any, duplicates are not allowed)
- The value column contains your predicted passenger counts (non-negative numbers are recommended but not enforced)

Evaluation metric
- Primary metric: SMAPE (Symmetric Mean Absolute Percentage Error)

SMAPE is computed over all test timestamps as:
SMAPE = mean( 200 * |y_pred - y_true| / (|y_true| + |y_pred|) )

Notes:
- Numerical stability: a very small epsilon is added to the denominator in the evaluator to avoid division by zero
- Lower is better

Data details and split
- Cadence: 30-minute intervals
- Train horizon: all historical timestamps up to (and including) 2015-01-03 23:30:00
- Test horizon: 2015-01-04 00:00:00 to 2015-01-31 23:30:00 (1,344 timestamps)
- The time series is provided in local NYC time-like format (naive timestamps). Do not change timezones; preserve the given cadence and labels

Guidance and allowed techniques
- You may engineer features from the timestamp (hour-of-day, day-of-week, weekend/weekday, week-of-year, month)
- You may compute lag and rolling window statistics using only the training window to avoid leakage
- Any forecasting model is allowed (e.g., naïve, exponential smoothing/ETS, SARIMA, gradient boosting, random forests, Prophet-like models, deep learning, etc.)
- External data is not necessary; solutions should be self-contained. If you choose to use external signals, clearly document them and ensure no leakage

Best practices
- Respect chronological order: do not use future information from the test horizon while training
- Validate your pipeline for correct alignment of timestamps
- Consider multi-seasonality and holiday effects in your modeling

Deliverable
- Submit a CSV named as you wish, following the Submission format above. Your score will be computed with SMAPE against the hidden ground truth for the 1,344 test timestamps.
