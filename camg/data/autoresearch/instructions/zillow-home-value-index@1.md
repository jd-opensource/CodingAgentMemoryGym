# OpenMLE-fast task

Task ID: `zillow-home-value-index@1`

Native metric: `ZillowHomeValueIndexMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2572 bytes)
- `data/sample_submission.csv` (47945 bytes); columns: ["date", "state", "zhvi_pred"]
- `data/test.csv` (25403 bytes); columns: ["date", "state"]
- `data/train.csv` (567307 bytes); columns: ["date", "state", "zhvi"]

## Public description

Title: State-Level ZHVI 24-Month Forecast Challenge

Problem statement
Forecast the monthly Zillow Home Value Index (ZHVI) for every U.S. state and the District of Columbia over the next 24 months. You are given long historical monthly series per state. Your task is to build models that learn from the training period and predict the values for Jan 2024 through Dec 2025.

What you will predict
- Target: ZHVI (monthly median home value) per state.
- Horizon: 24 months (2024-01 to 2025-12).
- Scope: 51 series (50 states + District of Columbia).

Files provided
- train.csv: Tidy training data with columns [date, state, zhvi]. For each state, rows start at its first non-null observation and run through 2023-12.
- test.csv: Tidy test inputs with columns [date, state] for all state-month pairs in 2024-01 to 2025-12. Labels are hidden.
- sample_submission.csv: Example submission with columns [date, state, zhvi_pred].

Submission format
- A single CSV with columns [date, state, zhvi_pred].
- Must contain exactly one row for each state-month in the test horizon (51 × 24 = 1224 rows).
- date must be ISO-format monthly timestamps (e.g., 2024-01-01), and state must match the canonical state names used in the provided files.
- zhvi_pred must be numeric and finite. Predictions should be on the original ZHVI level scale.

Evaluation
- Metric: Mean Absolute Error (MAE), aggregated across all states and months.
  - Seasonal period m = 12. For each state, the scaling denominator is the mean absolute seasonal difference over the training period: mean(|y_t − y_{t−12}|) for months where t−12 exists.
  - If a state’s training history is too short to compute seasonal differences, the denominator falls back to mean(|y_t − y_{t−1}|) over the training period.
  - Your score is the mean MASE across all 1224 state-month pairs.
- Why MASE: It is scale-free and fair across states with different price levels, robust to heteroskedasticity, and directly compares performance to a seasonal-naive baseline.

Notes and guidance
- Use any modeling approach suitable for multi-horizon time series forecasting: e.g., SARIMA/ETS/TBATS, state-space models, Prophet, global panel models (RNNs/TCNs/Transformers), and ensembles.
- You may transform series for modeling (log, percent change, YoY, decomposition), but submitted predictions must be on the original ZHVI level scale.
- The dataset includes long historical sequences with trends, structural breaks, and modest seasonality. Careful preprocessing and robust generalization across states will improve results.
