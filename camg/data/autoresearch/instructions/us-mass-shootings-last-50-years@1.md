# OpenMLE-fast task

Task ID: `us-mass-shootings-last-50-years@1`

Native metric: `MassShootingCountsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3390 bytes)
- `data/sample_submission.csv` (10785 bytes); columns: ["Id", "Count"]
- `data/test.csv` (18950 bytes); columns: ["Id", "State", "Year", "Month"]
- `data/train.csv` (100202 bytes); columns: ["Id", "State", "Year", "Month", "Count"]

## Public description

Title: State–Month Mass Shooting Counts Forecasting (2016–2021)

Background
Public incident data records US mass shootings with dates and locations. Anticipating monthly incident counts at the state level can inform resource allocation and preparedness without relying on sensitive individual-level attributes.

Problem Statement
Given historical monthly counts of mass shooting incidents per US state from January 2016 through December 2020 (train), forecast the monthly counts for January–December 2021 (test) for each state. This is a hierarchical time-series forecasting task over count data with strong zero-inflation and heterogeneous dynamics across states.

Files Provided
- train.csv: State–month panel with target
  - Columns: Id, State, Year, Month, Count
- test.csv: State–month panel without target
  - Columns: Id, State, Year, Month
- sample_submission.csv: Example submission
  - Columns: Id, Count

Id Schema
Id uniquely identifies each forecasting target as "State|YYYY|MM" (e.g., "Texas|2021|03"). The order of rows in test.csv is the canonical order for submissions; your submission must use the same Ids in the same order.

Target Definition
Count is the number of recorded mass shooting incidents in the given state and calendar month. All counts are integers ≥ 0.

Train/Test Split
- Train: all states, January 2016–December 2020
- Test: the same set of states, January–December 2021
The split is strictly time-based to avoid leakage.

Submission Format
- A single CSV with columns: Id, Count
- Ids must match test.csv exactly and appear in the same order
- Count predictions must be non-negative numeric values (floats or integers); negative, NaN, or infinite values are invalid

Evaluation Metric
Mean Poisson deviance over all test rows.
- For observed y and predicted µ ≥ 0: D(y, µ) = 2 * (y * log(y/µ) - (y - µ))
- The metric averages D across all state–months in the test set
- Predictions should be non-negative; extremely small values are treated safely to avoid numerical issues
Rationale: Poisson deviance is natural for count data, penalizes relative errors appropriately (including zeros), and discourages trivial strategies.

Modeling Guidance
Participants are encouraged to apply end-to-end ML:
- Data processing: robust handling of state names, calendar features, and time ordering
- Feature engineering: month-of-year seasonality, year trend, hierarchical state effects, lag features computed using training data only (up to 2020)
- Modeling: time-series models (ARIMA/ETS), count models (Poisson/negative binomial), gradient boosting on engineered features, hierarchical forecasting, ensembles
- Evaluation: cross-validation on time blocks within 2016–2020, error analysis by state and month
External data is optional; a strong solution can be built using the provided files alone.

Important Notes
- All test states occur in the training set
- The dataset includes many months with zero incidents; build models that handle zeros gracefully
- Ensure lagged features are computed strictly from training periods to prevent test leakage
- The goal is accurate forecasts of incident counts, not classification of individual events

Deliverables
- Submit your predictions in the required CSV format (Id, Count) using the order of test.csv
- Optimize your pipeline for the Poisson deviance metric

Good luck and build responsibly.
