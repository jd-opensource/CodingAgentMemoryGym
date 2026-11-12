# OpenMLE-fast task

Task ID: `money-sent-home@1`

Native metric: `MoneySentHomeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3150 bytes)
- `data/sample_submission.csv` (13635 bytes); columns: ["row_id", "remittance_amount"]
- `data/test.csv` (13191 bytes); columns: ["row_id", "country", "year"]
- `data/train.csv` (231050 bytes); columns: ["country", "year", "remittance_amount"]

## Public description

Competition: Global Remittance Inflow Forecasting (Country-Year Panel)

Problem statement
Participants are tasked with forecasting the absolute amount of personal remittances received by countries over time. Using historical country-year data, build models that predict future remittance inflows for each country. The task is a panel time-series forecasting problem with heterogeneous magnitudes and temporal dynamics.

Data description
- train.csv: Country-year historical records with the target variable.
  - Columns: country, year, remittance_amount
  - remittance_amount is a non-negative numeric value parsed from locale-formatted strings (e.g., thousands separators and decimal commas handled).
- test.csv: Country-year records to predict.
  - Columns: row_id, country, year
  - row_id uniquely identifies each test row and defines evaluation order.
- sample_submission.csv: Example submission file format.
  - Columns: row_id, remittance_amount
  - Values are random but valid, illustrating the expected numeric type and format.

Train/test split
- Per-country temporal split: For each country with at least 6 valid annual observations, the last 3 available years are placed in the test set; all earlier years are in the training set.
- Countries with fewer than 6 observations appear only in the training set and are excluded from the test set.
- The split is strictly future relative to each country’s training history, preventing label leakage.

Target and features
- Target: remittance_amount (absolute amount of personal remittances received by a country in a given year).
- Participants may engineer features from the training data, such as country-wise lags (1–5 years), moving averages, growth rates, volatility measures, and calendar features (year, decade bins). Hierarchical modeling by country is encouraged.

Submission format
- Submit a CSV file named arbitrarily with the following header and columns:
  - Header: row_id,remittance_amount
  - Each row must correspond exactly to a row_id in test.csv, in the same order.
  - remittance_amount must be a finite non-negative numeric value.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE) computed over all test rows.
  - Definition: RMSLE = sqrt(mean((log(1 + y_pred) − log(1 + y_true))^2)).
  - Rationale: RMSLE fairly penalizes multiplicative errors across countries with very different scales, is robust to zeros via log1p, and is standard for skewed financial flows.

Modeling considerations
- The dataset spans decades and includes zero or near-zero entries in early years, leading to heavy skew and non-stationarity.
- Effective approaches include country-specific lags, GBMs on panel features, ARIMA/ETS per country, hierarchical time-series models, or deep sequence models (RNNs/Transformers).
- No external data is required; solutions should rely solely on the provided training data.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Notes
- All values are parsed and deduplicated; rows are sorted by country then year.
- Test labels are not included in test.csv and are evaluated via a hidden ground truth mapping keyed by row_id.
