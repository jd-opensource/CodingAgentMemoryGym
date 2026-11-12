# OpenMLE-fast task

Task ID: `fuels-futures-data@2`

Native metric: `EnergyVolatilityMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2802 bytes)
- `data/sample_submission.csv` (32373 bytes); columns: ["row_id", "next_day_log_range"]
- `data/test.csv` (180952 bytes); columns: ["row_id", "ticker", "date", "open", "high", "low", "close", "volume"]
- `data/train.csv` (3119448 bytes); columns: ["row_id", "ticker", "date", "open", "high", "low", "close", "volume", "next_day_log_range"]

## Public description

Title: Next‑Day Volatility Forecasting for Energy Futures

Problem statement
Predict the next trading day’s intraday volatility for major energy futures. Given daily OHLCV data up to and including day t for each instrument, forecast the next day’s log range:

  target = ln(High_{t+1} / Low_{t+1})

You will train on historical panel data from five liquid energy futures and predict the target for a chronologically held‑out recent period.

Data
- Instruments: WTI Crude Oil, Brent Crude Oil, Natural Gas, Heating Oil, and RBOB Gasoline.
- Frequency: Daily (business/trading days), with columns: ticker, date, open, high, low, close, volume.
- Files provided after running prepare.py:
  - train.csv: All training rows with columns [row_id, ticker, date, open, high, low, close, volume, next_day_log_range].
  - test.csv: Test rows with columns [row_id, ticker, date, open, high, low, close, volume].
  - sample_submission.csv: Sample file showing the expected submission format [row_id, next_day_log_range].

Target construction and split
- Labels are computed as ln(High_{t+1} / Low_{t+1}) using the next day’s bar for the same instrument.
- The last row of each instrument (where t+1 does not exist) is discarded.
- Strict chronological split per instrument: all rows whose label date (t+1) falls on or before 2022-12-31 are in train; rows whose label date is on or after 2023-01-01 are in test. There is no overlap.
- The test set aggregates all instruments. The index for submissions is row_id.

Submission format
- A single CSV with two columns and no header changes:
  - row_id: integer identifier supplied in test.csv.
  - next_day_log_range: your prediction (a real number) for each row_id.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on next_day_log_range, averaged uniformly across all test rows.
- Rationale: Log range is a scale‑free proxy of volatility, making errors comparable across assets with different price levels. RMSE penalizes large mistakes and is deterministic from the provided OHLC.

Modeling guidance and constraints
- You may engineer any features that use information available up to and including date t only (no peeking into t+1 or beyond).
- Examples: lagged log ranges, ATR, Parkinson/Garman–Klass measures, rolling means/volatilities, momentum or seasonality features, volume surprises, and cross‑asset same‑day factors.
- Do not use any information from the future (t+1 and later). Cross‑sectional features are allowed if restricted to the same date t.

What to submit
- Submit a file named however you like, with exactly the two columns [row_id, next_day_log_range] and one row per test row_id.

Good luck! This is a challenging, high‑signal forecasting task that rewards robust feature engineering and time‑series‑aware modeling.
