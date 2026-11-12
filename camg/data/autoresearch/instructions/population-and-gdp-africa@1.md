# OpenMLE-fast task

Task ID: `population-and-gdp-africa@1`

Native metric: `AfricaGDPRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (516 bytes)
- `data/sample_submission.csv` (6640 bytes); columns: ["row_id", "GDP"]
- `data/test.csv` (14465 bytes); columns: ["row_id", "Year", "Country", "Subregion", "Population"]
- `data/train.csv` (44849 bytes); columns: ["row_id", "Year", "Country", "Subregion", "Population", "GDP"]

## Public description

Africa GDP-from-Population Panel Regression (2000–2022)

Files provided (relative to public/):
- train.csv: training rows with [row_id, Year, Country, Subregion, Population, GDP]
- test.csv: test rows with [row_id, Year, Country, Subregion, Population] (GDP hidden)
- sample_submission.csv: example submission with [row_id, GDP]

Submission format:
- CSV with columns [row_id, GDP]; row_id must match test.csv exactly.

Evaluation:
- Root Mean Squared Logarithmic Error (RMSLE) between predictions and hidden GDP.
