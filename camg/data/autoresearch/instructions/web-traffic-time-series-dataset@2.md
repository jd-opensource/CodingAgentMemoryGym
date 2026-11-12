# OpenMLE-fast task

Task ID: `web-traffic-time-series-dataset@2`

Native metric: `WebTrafficQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2442 bytes)
- `data/sample_submission.csv` (19406 bytes); columns: ["Id", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (7751 bytes); columns: ["Id", "Timestamp"]
- `data/train.csv` (66451 bytes); columns: ["Timestamp", "TrafficCount"]

## Public description

Web Traffic Probabilistic Forecasting (Quantiles)

Problem statement:
Predict future web traffic for a single website at hourly timestamps by providing calibrated quantile forecasts. Given historical observations (Timestamp, TrafficCount), forecast the 0.1, 0.5, and 0.9 quantiles for each timestamp in the test horizon.

What you are given:
- train.csv: Historical time series with columns [Timestamp, TrafficCount].
- test.csv: Future timestamps to forecast with columns [Id, Timestamp]. The order of rows defines the required prediction order.
- sample_submission.csv: Example submission file with columns [Id, q0.1, q0.5, q0.9].

Task:
- Use train.csv to fit your model and generate a submission for all rows in test.csv. For each Id in test.csv, predict the 0.1, 0.5, and 0.9 quantiles of TrafficCount.

Evaluation metric:
- Submissions are scored by mean pinball (quantile) loss averaged across the quantiles Q = {0.1, 0.5, 0.9} and across all test rows.
- For a true value y and a predicted quantile q̂ at level α ∈ (0,1), the pinball loss is: Lα(y, q̂) = max(α·(y − q̂), (α − 1)·(y − q̂)). The competition score is the mean of Lα over all test rows and over α ∈ {0.1, 0.5, 0.9}. Lower is better.
- Predictions must satisfy monotonicity per row: q0.1 ≤ q0.5 ≤ q0.9.

Data description and nuances:
- Timestamp is timezone-agnostic and roughly hourly (mostly at :30). Seasonality (intraday/weekly), spikes, and regime shifts are present.
- TrafficCount is a non-negative numeric count of web requests.
- The train/test split is purely chronological: the last 14 days of the series form the test horizon at the native timestamps. No resampling is required; model on the given timestamps.

Submission format:
- A CSV with columns [Id, q0.1, q0.5, q0.9].
- Id must exactly match those in test.csv (order and set). Each q-column must be finite numeric. Monotonicity must hold per row.

Modeling guidance (optional):
- Useful features: calendar (hour-of-day, day-of-week), lags and rolling statistics, Fourier terms, log1p transforms, change-point features, and holiday flags if you construct them from timestamps.
- Suitable models include quantile regression (e.g., gradient boosting with quantile loss), probabilistic state-space models, and sequence models (LSTM/TCN/N-BEATS) trained for quantiles.

Files provided to participants:
- train.csv
- test.csv
- sample_submission.csv

Good luck and happy forecasting!
