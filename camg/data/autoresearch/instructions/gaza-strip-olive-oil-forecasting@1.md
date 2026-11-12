# OpenMLE-fast task

Task ID: `gaza-strip-olive-oil-forecasting@1`

Native metric: `OliveOilPriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2317 bytes)
- `data/sample_submission.csv` (858 bytes); columns: ["Date", "USD_Price"]
- `data/test.csv` (324 bytes); columns: ["Date"]
- `data/train.csv` (2314 bytes); columns: ["Date", "USD_Price"]

## Public description

Gaza Strip Olive Oil Price Forecasting (Monthly)

Problem statement
Build a model to forecast monthly olive oil prices (USD) in Gaza for a held-out future period. You are given historical monthly prices and must predict the price in USD for each month listed in test.csv. Your submission should contain a USD_Price prediction for every Date in test.csv.

Data description
- train.csv: Historical data with two columns: Date, USD_Price. Dates are monthly (on the 15th) and sorted. Date format is YYYY-MM-DD.
- test.csv: Future target months with a single column: Date. Predict USD_Price for each Date. Date format is YYYY-MM-DD.
- sample_submission.csv: Example submission with the required columns: Date, USD_Price.

Notes
- Dates are monthly and reflect real market behavior with seasonality and occasional irregularities. Any duplicates in the original source were already reconciled; each Date appears once in the provided files. Some calendar months within the overall period may be absent and are not included in test.csv.
- Targets are in price levels (USD). You may transform during modeling (e.g., logs, differences), but predictions must be submitted in USD levels.

Evaluation
Primary metric: Mean Absolute Scaled Error (MASE) with seasonal period m = 12.
- The scaling denominator is computed from the in-sample seasonal naïve forecast on the training set.
- For training values y_1, ..., y_T and m = 12, the denominator is mean(|y_t − y_{t−m}|) for t = m+1..T.
- Your score is the mean absolute error on test months divided by this denominator. Lower is better; a score < 1 outperforms the seasonal naïve baseline.

Rules and expectations
- Use any ML or time series methods. Typical approaches include SARIMA/ETS, Prophet, TBATS, state space models, gradient boosting with lag/seasonal features, and hybrids.
- Handle date parsing carefully. The data are monthly; using calendar features (month-of-year, lags, rolling statistics) is encouraged.
- Submit predictions for every Date in test.csv. Files must match the required schema exactly.
- Predictions must be numeric and finite (no NaN/Inf). Extra or missing rows are not allowed.

Files to produce for submission
- A CSV with columns: Date, USD_Price
- Include every Date from test.csv exactly once. No extra rows, missing rows, or duplicates.
