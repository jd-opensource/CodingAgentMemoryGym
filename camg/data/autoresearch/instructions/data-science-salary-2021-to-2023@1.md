# OpenMLE-fast task

Task ID: `data-science-salary-2021-to-2023@1`

Native metric: `DataScienceSalaryRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2582 bytes)
- `data/sample_submission.csv` (40753 bytes); columns: ["row_id", "salary_in_usd"]
- `data/test.csv` (65846 bytes); columns: ["row_id", "work_year", "experience_level", "employment_type", "job_title", "company_location", "company_size"]
- `data/train.csv` (77483 bytes); columns: ["work_year", "experience_level", "employment_type", "job_title", "company_location", "company_size", "salary_in_usd"]

## Public description

Competition: Predicting Data Science Salaries (Generalization to 2023)

Problem statement
Accurately estimating total compensation for data roles helps both employers and candidates make informed decisions. In this competition, you will build a machine learning model to predict the annual total compensation in USD for a data role given structured attributes of the role and the employer.

Task
Given tabular features describing a role and its context, predict salary_in_usd for each instance in the test set.

Final data files
- train.csv: Training data including features and the target column salary_in_usd.
- test.csv: Test data including the same features as train.csv plus an identifier column row_id, but without the target.
- sample_submission.csv: A sample submission file with the required format (row_id, salary_in_usd).

Target and features
- Target: salary_in_usd (numeric, annual total compensation in USD).
- Features provided:
  - work_year (integer)
  - experience_level (categorical: EN, MI, SE, EX)
  - employment_type (categorical: FT, CT, FL, PT)
  - job_title (categorical)
  - company_location (categorical: country codes)
  - company_size (categorical: S, M, L)

Note: The original salary and salary_currency fields are excluded from the final train/test files to prevent label leakage, since salary_in_usd is derived from them.

Split strategy
- Train set comprises earlier years.
- Test set comprises the most recent year, requiring models to generalize to evolving roles and market conditions.

Evaluation metric
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the ground truth salary_in_usd values:
- RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
- The log1p transform provides a fair comparison across wide salary ranges and reduces the impact of extreme values.
- Predictions must be provided for every row_id in test.csv. Non-finite or negative predictions are treated robustly by clamping at zero prior to scoring.

Modeling guidance
- Handle categorical variables appropriately (e.g., target encoding, frequency encoding, embeddings).
- Engineer meaningful features from job titles and geographies.
- Consider interactions between experience level, employment type, company size, and work year.
- Evaluate and tune models carefully; the temporal split makes naive memorization ineffective.

Submission format
- A CSV file with columns: row_id, salary_in_usd.
- row_id must match those in test.csv exactly and appear once.
- salary_in_usd should be a numeric prediction for each row.
