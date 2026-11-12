# OpenMLE-fast task

Task ID: `renewable-energy-consumption-in-the-u-s@1`

Native metric: `RenewableEnergyForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (653 bytes)
- `data/sample_submission.csv` (14156 bytes); columns: ["id", "Consumption"]
- `data/test.csv` (18184 bytes); columns: ["id", "Year", "Month", "Sector", "Target"]
- `data/train.csv` (477634 bytes); columns: ["Year", "Month", "Sector", "Target", "Consumption"]

## Public description

Title: Sectoral Monthly Renewable Energy Forecasting (US, 1973–2024)

Files in this directory:
- train.csv: Historical monthly records (1973–2022) with columns [Year, Month, Sector, Target, Consumption].
- test.csv: Evaluation horizon (2023–2024) with columns [id, Year, Month, Sector, Target].
- sample_submission.csv: Example submission with [id, Consumption].

Submission format:
- A single CSV with two columns: [id, Consumption].
- Each id corresponds to one row in test.csv. Provide a prediction for every id exactly once.

Evaluation notes:
- Rows with strictly positive ground truth are evaluated; rows with zero ground truth are ignored.
