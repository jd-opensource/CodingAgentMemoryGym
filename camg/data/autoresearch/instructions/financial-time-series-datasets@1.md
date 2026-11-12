# OpenMLE-fast task

Task ID: `financial-time-series-datasets@1`

Native metric: `FinancialForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3601 bytes)
- `data/sample_submission.csv` (27642 bytes); columns: ["row_id", "y"]
- `data/test.csv` (139525 bytes); columns: ["row_id", "series_id", "timestamp", "value", "frequency", "open", "high", "low", "close", "volume"]
- `data/train.csv` (619971 bytes); columns: ["series_id", "timestamp", "value", "frequency", "open", "high", "low", "close", "volume", "y"]

## Public description

Title: Multi-Scale Financial One-Step Forecasting (Macro-MAE on Standardized Differences)

Problem statement
You are given a heterogeneous panel of financial time series spanning intraday, daily, quarterly, and yearly frequencies across multiple assets and indicators. For each series and timestamp in the test set, predict the next-step standardized change: the one-step-ahead first difference divided by the series’ training-window difference standard deviation. The challenge is to build models that generalize across assets and sampling frequencies.

Data description
- train.csv: Training rows where the target is observed. Columns
  - series_id: Anonymous identifier for each series (e.g., S1, S2, …).
  - timestamp: Datetime in ISO-8601 format.
  - value: The primary numeric signal for the series (e.g., adjusted close, close, earnings, index value).
  - frequency: One of {intraday, daily, quarterly, yearly}.
  - Optional columns present for some series (intraday): open, high, low, close, volume.
  - y: Target label for training rows (standardized one-step differences as defined below).
- test.csv: Rows for which predictions are required. Columns
  - row_id: Unique identifier that aligns exactly with sample_submission.csv.
  - series_id, timestamp, value, frequency, and optional intraday columns (open, high, low, close, volume).
- sample_submission.csv: Example submission file with columns [row_id, y].

Target definition
For each series separately:
1) Sort by timestamp ascending and compute first differences: diff_t = value_t − value_{t−1}.
2) Compute s_series = standard deviation of the differences over that series’ training window (use ddof=1 when there are at least 2 training diffs; otherwise use a finite fallback; clamp extremely small values to a small epsilon).
3) Define the label y_t = diff_t / s_series for t ≥ the second observation of that series.

Train/test split
- Per series, split chronologically: earliest 80% of timestamps form the training window; latest 20% form the test window.
- train.csv includes only rows within the training window where y is defined (i.e., from the second timestamp onward per series).
- test.csv includes only rows within the test window where y is defined. The first test row of each series has a target because its previous timestamp lies inside the training window.
- The split and target construction are deterministic and strictly time-ordered to prevent leakage.

Evaluation metric
- Macro-averaged Mean Absolute Error (MAE) across series on the standardized targets.
  - For each series_id, compute MAE between predictions and true y on that series’ test rows.
  - The final score is the arithmetic mean of these per-series MAEs, weighting each series equally.
  - Standardization by the training-window difference stdev normalizes scale across assets and frequencies, ensuring fair comparison.

Submission format
- A CSV file with exactly two columns and no header changes: [row_id, y].
- row_id must match test.csv exactly in both values and order.
- y must be numeric and finite for every row.

Modeling guidance
- Feature engineering ideas: rolling statistics, lagged features, differencing, volatility estimates, calendar/time-of-day (for intraday), series_id embeddings, frequency-aware features.
- Modeling approaches: per-series classical models (ARIMA/ETS), gradient boosting on engineered features, state-space models, and sequence models (RNN/TCN/Transformers) over the panel.
- The intraday series includes OHLCV columns to enable more advanced features; other series provide the core value only.
