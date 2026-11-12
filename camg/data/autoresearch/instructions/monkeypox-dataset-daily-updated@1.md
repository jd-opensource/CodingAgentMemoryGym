# OpenMLE-fast task

Task ID: `monkeypox-dataset-daily-updated@1`

Native metric: `MonkeypoxForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (515 bytes)
- `data/exog_aggregates_train.csv` (92055 bytes); columns: ["Country", "Date", "hosp_known", "hosp_yes", "iso_known", "iso_yes", "travel_known", "travel_yes", "travel_no", "male_flag", "female_flag", "symptom_rash", "symptom_fever", "symptom_lymph", "symptom_headache", "timeline_count", "hosp_yes_share", "iso_yes_share", "travel_yes_share", "travel_no_share"]
- `data/sample_submission.csv` (52967 bytes); columns: ["Country", "Date", "NewConfirmed"]
- `data/test.csv` (48229 bytes); columns: ["Country", "Date"]
- `data/train.csv` (300585 bytes); columns: ["Country", "Date", "NewConfirmed"]

## Public description

Monkeypox Country-Day 21-Day Ahead Forecasting Challenge

Files in this folder
- train.csv: [Country, Date, NewConfirmed] up to 2022-08-31.
- test.csv: [Country, Date] from 2022-09-01 to 2022-09-21 (21 days per country).
- exog_aggregates_train.csv: Optional aggregated features from case-level timelines up to 2022-08-31.
- sample_submission.csv: Example with valid structure and placeholder predictions.

Submission
- Submit a CSV with columns [Country, Date, NewConfirmed] covering exactly the rows in test.csv.
