# OpenMLE-fast task

Task ID: `suicide-rates-percentage@1`

Native metric: `SuicideDeathsForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3200 bytes)
- `data/sample_submission.csv` (12777 bytes); columns: ["country", "Year", "PredictedDeaths"]
- `data/test.csv` (5627 bytes); columns: ["country", "Year"]
- `data/train.csv` (83311 bytes); columns: ["country", "Year", "TotalDeaths"]

## Public description

Suicide Deaths Forecasting Challenge

Problem statement
Participants are tasked with forecasting the total annual number of deaths from self-harm for each country. Using historical records from 2000–2019, build models that predict country-level totals for the years 2020 and 2021. External data is not required; solutions should rely on time-series modeling and features derived from the provided training data.

Dataset
- Train file: train.csv with columns [country, Year, TotalDeaths]. Years span 2000–2019.
- Test file: test.csv with columns [country, Year]. Years include 2020–2021. The targets are hidden.

Important notes
- Data cleaning has been applied to normalize numerical formatting and remove aggregate regions (continents, global totals, income groups, etc.). The dataset focuses on sovereign countries and microstates to maintain comparability.
- There are countries with small counts and potential zeros; consider variance-stabilizing transforms (e.g., log1p) and robust modeling.
- No file paths or external references should be included in submissions—only country names and numerical predictions.

Task guidance
Participants should consider:
- Data processing: verify types, handle missing values, and confirm the country-year keys. You may create per-country time series features such as lags (t-1…t-5), differences, rolling statistics, and trend indicators.
- Feature engineering: experiment with transformations (log1p), seasonality or trend extraction, and global modeling where countries share parameters but retain identity.
- Model training: evaluate classic forecasting (ARIMA/ETS/Prophet), tree-based regressors with engineered features, or sequence models (RNN/Transformer) using pooled training across countries.
- Model evaluation: use robust validation protocols (e.g., rolling-origin per country) on the training years to simulate forecasting the last two years.

Evaluation metric
- Official leaderboard metric: SMAPE (Symmetric Mean Absolute Percentage Error), averaged over all country-year predictions in the test set.
- SMAPE is calculated as 100% × mean over i of [ 2 × |y_i − ŷ_i| ÷ (|y_i| + |ŷ_i| + ε) ], where ε is a small constant to avoid division by zero.
- This metric balances influence across countries regardless of magnitude and is stable near zero values.

Submission format
- CSV with columns [country, Year, PredictedDeaths].
- Include a prediction for every row in the test.csv file; order is not important.
- PredictedDeaths must be non-negative finite numbers.

File summary
- train.csv: Cleaned country-level series with targets for 2000–2019.
- test.csv: Country-year pairs for 2020–2021 to predict.
- sample_submission.csv: Example submission with naïve baseline predictions.

Tips for strong performance
- Hierarchical pooling: train one global model with country identity features to share signal while allowing heterogeneity.
- Robustness: design features resilient to shocks and non-stationarity; consider rolling-window validation.
- Scale handling: stabilize variance; avoid letting large-population countries dominate your model design.

Good luck, and aim for accurate, robust forecasts across all countries.
