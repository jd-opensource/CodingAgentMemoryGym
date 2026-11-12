# OpenMLE-fast task

Task ID: `co2-ghg-emissionsdata@1`

Native metric: `CO2EmissionsForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2998 bytes)
- `data/sample_submission.csv` (39785 bytes); columns: ["Entity", "Code", "Year", "emissions"]
- `data/test.csv` (20728 bytes); columns: ["Entity", "Code", "Year"]
- `data/train.csv` (491343 bytes); columns: ["Entity", "Code", "Year", "emissions"]

## Public description

CO2 Emissions Forecasting Challenge

Background
Anthropogenic CO2 emissions are a key driver of climate change. Country-level annual emissions reflect industrial activity, energy mix, policy, and economic structure. Accurate short-horizon forecasts are valuable for monitoring progress, benchmarking, and scenario analysis.

Objective
Given each country’s historical annual CO2 emission series, forecast the next five years of emissions. You are provided with time series per country up to 2012 and must predict values for 2013–2017.

Data
- The data comprise annual country-level CO2 emissions time series derived from public sources.
- Aggregates and global/region-level series are excluded; only individual countries/territories are included.
- Train contains all available years up to and including 2012 for the selected set of countries.
- Test contains the same countries for years 2013–2017, without the target values.

Files
- train.csv: columns [Entity, Code, Year, emissions]
- test.csv: columns [Entity, Code, Year]
- sample_submission.csv: columns [Entity, Code, Year, emissions]

Target
- emissions: annual CO2 emissions (in tonnes) for a given [Entity, Code, Year].

Task details and constraints
- Time-aware split: you may use train.csv (≤2012) to predict test.csv (2013–2017). Do not use any information from future years in feature construction.
- Each row corresponds to one country-year. Entity is a human-readable name, Code is a 3-letter country code, and Year is the calendar year.
- Countries in test appear in train with historical observations.

Evaluation
Submissions are evaluated using macro-averaged symmetric mean absolute percentage error (SMAPE) computed per country across its five test years and then averaged across countries. Lower is better.

For a country c with true values y_{c,t} and predictions p_{c,t} over t ∈ {2013, …, 2017}:
- Per-year SMAPE_t = 2·|p_{c,t} − y_{c,t}| / (|p_{c,t}| + |y_{c,t}|)
- Country SMAPE_c = mean_t(SMAPE_t)
- Leaderboard score = mean_c(SMAPE_c)

Implementation details:
- If |p_{c,t}| + |y_{c,t}| = 0, that term contributes 0.
- The final score is in [0, 2].

Modeling notes
- This is a panel time-series forecasting problem. Approaches include univariate models (ARIMA/ETS/Prophet), global forecasting models (RNN/Transformer/DeepAR), gradient boosting on engineered temporal features, or hybrid hierarchical models.
- Useful features may include per-entity lags, rolling statistics, growth rates, change-point indicators, and variance-stabilizing transforms (e.g., log1p on emissions).
- Be mindful of nonstationarity, structural breaks, and heterogeneous dynamics across countries.

Submission format
- Submit a CSV with exactly the columns [Entity, Code, Year, emissions] for every row present in test.csv, in any order. Duplicates or missing rows will be rejected.

Reproducibility
- The provided sample_submission.csv contains deterministic, baseline-style predictions and demonstrates the required format.
