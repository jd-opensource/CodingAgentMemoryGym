# OpenMLE-fast task

Task ID: `new-orders-in-manufacturing-original-index@1`

Native metric: `ManufacturingOrdersForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2730 bytes)
- `data/sample_submission.csv` (2804 bytes); columns: ["row_id", "value"]
- `data/test.csv` (2135 bytes); columns: ["row_id", "series_id", "month"]
- `data/train.csv` (14176 bytes); columns: ["series_id", "month", "value"]

## Public description

New Orders in Manufacturing — 24‑Month Multi‑Series Forecasting Challenge

Problem statement
Participants must forecast the next 24 monthly values (2023-04 to 2025-03) of the Original Index (2021=100) for four manufacturing series from Statistics Finland. Models should learn from the full historical monthly data (2005-01 to 2023-03) and produce accurate multi‑horizon forecasts for each series.

Why this is challenging
- Four related series with distinct dynamics (seasonality, cycles, structural breaks)
- A long history (18+ years) enabling both classical and modern time‑series/ML methods
- A 24‑step horizon requiring robust multi‑horizon modeling and uncertainty handling

Files provided
- train.csv: Training data in long format with columns [series_id, month, value]
  - series_id: anonymized identifiers S1..S4 (consistent across files)
  - month: YYYY-MM (string)
  - value: Original Index (2021=100), float
- test.csv: Forecasting targets (without labels) with columns [row_id, series_id, month]
  - row_id: unique key formatted as "S#|YYYY-MM" (e.g., S2|2024-10)
  - series_id: S1..S4
  - month: YYYY-MM (string) covering 24 months per series (2023-04..2025-03)
- sample_submission.csv: Example submission with columns [row_id, value]

Submission format
- CSV with columns [row_id, value]
- Must contain exactly the same set of row_id values as found in test.csv (order does not matter)
- value must be a finite real number for every row

Evaluation metric
- Mean Absolute Scaled Error (MASE) with seasonal period m = 12 (monthly data)
- Computed per series against its in‑sample seasonal naïve baseline using only the training data; then averaged across all test rows and series

Let ŷ_{i,t} be your forecast for series i at test month t, and y_{i,t} the ground truth. For each series i, define the scaling term using the training set T_i:
- d_i = mean over t in T_i with t>m of |y_{i,t} − y_{i,t−m}| (seasonal naïve in‑sample MAE)
- If d_i is zero or undefined, a small positive constant is used internally to keep the metric well‑defined.
MASE is then: mean over all i and test months t of |ŷ_{i,t} − y_{i,t}| / d_i.

Notes
- Using MASE makes results comparable across series of different scales and is robust to outliers compared to RMSE.
- You may use any time‑series or ML techniques. Strong baselines include seasonal naïve, ETS/ARIMA/state‑space models, TBATS, Prophet, gradient boosting with time features, and global deep learning models.

Important details
- The provided series are anonymized as S1..S4; do not assume real‑world labels.
- Month strings are strict YYYY-MM.
- All four series and the full history are intended for use; no subset restriction applies.
