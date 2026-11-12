# OpenMLE-fast task

Task ID: `wages-and-education-of-young-males-dataset@1`

Native metric: `YoungMaleWageForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2469 bytes)
- `data/sample_submission.csv` (12311 bytes); columns: ["row_id", "wage"]
- `data/test.csv` (47134 bytes); columns: ["row_id", "nr", "year", "school", "exper", "union", "ethn", "maried", "health", "industry", "occupation", "residence"]
- `data/train.csv` (352843 bytes); columns: ["nr", "year", "school", "exper", "union", "ethn", "maried", "health", "wage", "industry", "occupation", "residence"]

## Public description

Panel Wage Forecast Challenge (1987 Holdout)

Problem statement
Predict each worker’s hourly wage in 1987 using information available up to 1986. The data is an 8-year panel (1980–1987) of young male workers with demographics, job characteristics, and wages recorded annually.

Data
- Train file: train.csv — rows from 1980–1986 with the target column wage present.
- Test file: test.csv — rows from 1987 with the target withheld and a row_id to identify each record.
- Sample: sample_submission.csv — example submission with random but plausible predictions.

Columns
- nr: individual identifier (useful for constructing panel features; avoid feeding directly as a feature to prevent identity memorization).
- year: calendar year (1980–1987).
- school: years of schooling.
- exper: years of experience.
- union, ethn, maried, health: categorical statuses.
- industry, occupation, residence: categorical descriptors (residence may be blank for some rows; treat blanks as a valid category).
- wage: continuous target (appears log-transformed). Present only in train.csv.
- row_id: submission key aligning test.csv and sample_submission.csv. Present only in test.csv and sample_submission.csv.

Objective and modeling hints
- Use the full panel structure (1980–1986) to forecast the 1987 wage. Construct temporal features such as lagged wages (t−1, t−2), rolling means, slopes/trends, transition indicators (industry/occupation changes), and interactions (e.g., union × industry, school × exper).
- Handle categorical variables thoughtfully (e.g., one-hot encoding with explicit treatment for blanks).
- Standardize numeric features using only training statistics to avoid leakage.

Evaluation
- Metric: Root Mean Squared Error (RMSE) computed on 1987 wage targets.
- Submission format: A CSV with two columns: row_id and wage. The row_id values must exactly match those in test.csv.

Fairness and rigor
- RMSE is appropriate for continuous outcomes and penalizes large errors, offering a precise and differentiating measure of out-of-time generalization.
- The split ensures each test individual has a complete 1980–1986 history, enabling meaningful feature engineering without peeking into 1987.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Notes
- Do not rely on the year 1987 information to build features; only use data up to 1986.
- Treat missing/blank residence entries as a dedicated category rather than dropping rows.
