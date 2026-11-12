# OpenMLE-fast task

Task ID: `economic-times-headlines-india-2022-to-2025@2`

Native metric: `EconomicTimesHeadlineForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3279 bytes)
- `data/sample_submission.csv` (45704 bytes); columns: ["date", "section", "count"]
- `data/test.csv` (36949 bytes); columns: ["date", "section"]
- `data/train.csv` (282072 bytes); columns: ["date", "section", "count"]

## Public description

Competition: Forecast Daily Headline Volume by Section (Economic Times India)

Problem statement
Participants must forecast the next-day headline counts for each top-level section of the Economic Times website. Given historical daily headline volumes per section, predict the counts for a held-out rolling window in 2025. This is a multi-series time-series forecasting task with strong weekly/seasonal patterns and event-driven spikes.

Files provided
- train.csv: Aggregated daily series with columns: date, section, count.
- test.csv: The rows to predict with columns: date, section. Each row requires a count prediction.
- sample_submission.csv: Example submission matching test.csv rows and format. Replace the count values with your predictions.

Target definition
- section: Derived as the first path segment after the domain in each article URL (e.g., https://economictimes.indiatimes.com/news/… -> section=news).
- count: Number of headlines published on that calendar date for the given section.
- Dates are calendar days (ISO format YYYY-MM-DD). If a section has zero headlines on a date, its count is 0.

Time windows
- Training window: 2022-01-01 to 2024-12-31 (inclusive).
- Test window: 2025-01-01 to 2025-06-11 (inclusive).
- Sections included: All top-level sections that appear at least 100 times in the training window. Test rows cover every date × section combination for these sections in the test window.

Evaluation
- Primary metric: RMSLE with equal weighting per section.
  1) For each section s, compute RMSLE_s over all its test dates:
     RMSLE_s = sqrt( mean( (log1p(y_hat) - log1p(y_true))^2 ) )
  2) The leaderboard score is the unweighted mean of RMSLE_s across all sections present in test.csv.
- Why RMSLE + per-section averaging?
  - RMSLE handles non-negative count targets and compares relative errors fairly across scales.
  - Per-section averaging prevents high-volume sections from dominating the metric.

Submission format
- CSV with columns: date, section, count
- Must contain exactly the same rows (date, section pairs) and row count as test.csv.
- The count values must be non-negative numbers (decimals are allowed and will be evaluated with log1p).

Modeling notes
- You may use classical or ML forecasting approaches, including lags and rolling statistics, per-section models, global panel models, or deep forecasting models.
- Calendar features (day-of-week, month, holidays), moving averages, and other engineered covariates are allowed.
- Using the headline text to engineer per-day features (e.g., keyword/topic volumes) is allowed, but only information available up to each prediction day should inform that day’s forecast.

File schema
- train.csv columns: date (YYYY-MM-DD), section (string), count (integer >= 0)
- test.csv columns: date (YYYY-MM-DD), section (string)
- sample_submission.csv columns: date (YYYY-MM-DD), section (string), count (non-negative number)

Tips
- Ensure your submission contains every row present in test.csv exactly once and no extras.
- Strong baselines include:
  - Naive: yesterday’s count
  - Weekly seasonal naive: count from 7 days ago
  - Rolling mean/median per weekday and per section
  - Gradient boosting or linear models with lagged features

Good luck and happy forecasting!
