# OpenMLE-fast task

Task ID: `historical-sales-data-on-daily-basis-of-a-company@2`

Native metric: `IntermittentDemandQuantileMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3870 bytes)
- `data/sample_submission.csv` (59934 bytes); columns: ["Date", "Article_ID", "Country_Code", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (14857 bytes); columns: ["Date", "Article_ID", "Country_Code"]
- `data/train.csv` (231074 bytes); columns: ["Date", "Article_ID", "Country_Code", "Sold_Units"]

## Public description

Probabilistic Intermittent-Demand Forecasting (Multi-Quantile)

Problem statement
Participants must forecast the distribution of daily online sales (Sold_Units) for each Article_ID × Country_Code series over a fixed 44‑day horizon. Forecasts must be submitted as predictive quantiles for each requested date and series. The data exhibit intermittent demand (many zeros) with occasional spikes, making calibrated uncertainty crucial.

Data description
- train.csv: Historical daily sales with columns [Date, Article_ID, Country_Code, Sold_Units]. Date is formatted as YYYY-MM-DD. All series are aligned on a complete daily calendar and missing dates are filled with Sold_Units = 0. The training window ends on 2018-12-31.
- test.csv: Forecast IDs for the evaluation window with columns [Date, Article_ID, Country_Code]. The test window spans 2019-01-01 to 2019-02-13 inclusive (44 days) for every Article_ID × Country_Code series.
- sample_submission.csv: Example submission with the required schema: [Date, Article_ID, Country_Code, q0.1, q0.5, q0.9]. Values are floats and must satisfy q0.1 ≤ q0.5 ≤ q0.9 for each row.

Task
Given train.csv, produce a submission file with quantiles {0.1, 0.5, 0.9} for Sold_Units for every row in test.csv. External data are not required. Effective solutions will leverage feature engineering (calendar effects, lags/rolling stats), models for zero-inflated counts, and/or probabilistic time-series methods (e.g., quantile regression trees/boosting, distributional count models, deep sequence models with quantile outputs).

Evaluation metric
Submissions are scored with a weighted multi-quantile pinball loss, a proper scoring rule that rewards calibrated quantile forecasts and is robust to demand spikes.

Let y be the true Sold_Units for a given row (Date, Article_ID, Country_Code), and let ŷ_q be the submitted predictive q-quantile for q ∈ {0.1, 0.5, 0.9}. The per-quantile pinball loss is
  L_q(y, ŷ_q) = { q · (y − ŷ_q), if y ≥ ŷ_q; (1−q) · (ŷ_q − y), otherwise }.
For a series s (a unique Article_ID × Country_Code), the series loss is the average of L_q across all test dates and the three quantiles. The final score is the weighted average across series, with weights proportional to each series’ total Sold_Units in the training window (normalized to sum to 1). If all series have zero training sales, uniform weights are used. Lower is better.

Important details and conventions
- Dates: Date strings are ISO formatted (YYYY-MM-DD). The training window ends at 2018-12-31. The test window covers 44 consecutive days: 2019-01-01 to 2019-02-13 inclusive.
- Targets: Sold_Units are non-negative counts. Predictions may be non-integer and must be finite.
- Submission schema: Exactly the columns [Date, Article_ID, Country_Code, q0.1, q0.5, q0.9]. Each row in test.csv must have one matching row in the submission. Quantiles must be non-decreasing per row (q0.1 ≤ q0.5 ≤ q0.9).
- Series coverage: Every Article_ID × Country_Code in test.csv appears in train.csv. Missing dates in train.csv have been filled with zeros to provide a continuous daily calendar for modeling.

Deliverables
Submit a CSV named submission.csv (or any name you prefer) with the schema of sample_submission.csv. Your score will be computed with the metric above against the hidden labels for the test window.

Why this is challenging and meaningful
- Intermittency: Many days have zero demand with occasional bursts, requiring models that can capture both the probability of zero sales and the heavy tail of nonzero days.
- Multi-series: The dataset comprises multiple products and countries with heterogeneous behavior, encouraging shared learning and series-specific features.
- Probabilistic accuracy: Optimizing quantile forecasts promotes calibrated uncertainty estimates aligned with real retail decisions.
