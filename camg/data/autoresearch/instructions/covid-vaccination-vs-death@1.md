# OpenMLE-fast task

Task ID: `covid-vaccination-vs-death@1`

Native metric: `CovidVaccinationMortalityForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (736 bytes)
- `data/sample_submission.csv` (73836 bytes); columns: ["row_id", "target"]
- `data/test.csv` (220470 bytes); columns: ["country", "iso_code", "date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "New_deaths", "population", "ratio", "row_id"]
- `data/train.csv` (3480068 bytes); columns: ["country", "iso_code", "date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "New_deaths", "population", "ratio", "row_id", "target"]

## Public description

Competition: Forecasting COVID-19 weekly mortality from vaccination progress (country-level panel)

Files provided
- train.csv: Training rows with features and the target column.
- test.csv: Test rows with features only (no target).
- sample_submission.csv: Example submission with the required format and randomized but valid predictions.

Submission format
- CSV with exactly two columns: row_id, target
- row_id corresponds one-to-one with the rows in test.csv (format: ISO_YYYY-MM-DD)
- target is a non-negative real number: the 7-day forward cumulative deaths per 100k population

Evaluation metric
- Country-averaged MAE: mean absolute error is computed per country over its test dates and then averaged equally across countries.
