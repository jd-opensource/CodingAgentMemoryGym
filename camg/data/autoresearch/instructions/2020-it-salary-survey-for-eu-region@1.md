# OpenMLE-fast task

Task ID: `2020-it-salary-survey-for-eu-region@1`

Native metric: `SalaryPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2690 bytes)
- `data/sample_submission.csv` (12910 bytes); columns: ["row_id", "salary"]
- `data/test.csv` (91460 bytes); columns: ["row_id", "age", "gender", "city", "position", "position_base", "years_experience", "years_experience_germany", "seniority", "main_tech", "other_tech", "bonus_eur", "stocks_eur", "bonus_stocks_eur", "vacation_days", "home_office_days", "employment_status", "contract_duration", "language_work", "company_size", "company_type", "covid_lost_job", "kurzarbeit_hours", "wfh_support_eur", "stocks_option_yesno", "year"]
- `data/train.csv` (382716 bytes); columns: ["row_id", "age", "gender", "city", "position", "position_base", "years_experience", "years_experience_germany", "seniority", "main_tech", "other_tech", "salary", "bonus_eur", "stocks_eur", "bonus_stocks_eur", "vacation_days", "home_office_days", "employment_status", "contract_duration", "language_work", "company_size", "company_type", "covid_lost_job", "kurzarbeit_hours", "wfh_support_eur", "stocks_option_yesno", "year"]

## Public description

Title: EU IT Salary Prediction Challenge (2018–2020)

Problem statement:
Predict a respondent’s current yearly brutto salary (without bonus and stocks) from their profile, job, and company attributes. The data spans three annual surveys (2018–2020) with heterogeneous schemas, multilingual values, and free-text fields, requiring careful cleaning, normalization, and feature engineering.

Files provided:
- train.csv: Tabular training data with features and the target column.
- test.csv: Same feature columns as train.csv (without the target).
- sample_submission.csv: Example submission with valid random predictions for the test rows.

Target:
- salary: Current yearly brutto salary in EUR (strictly positive).

Suggested features (not exhaustive):
- Demographics: age, gender, city
- Role and seniority: position_base (role without seniority), seniority
- Experience: years_experience, years_experience_germany
- Tech stack: main_tech, other_tech
- Workplace language: language_work
- Company: company_size, company_type, contract_duration
- Work conditions: vacation_days, home_office_days, employment_status
- Compensation extras as features: bonus_eur, stocks_eur, bonus_stocks_eur, stocks_option_yesno
- COVID-19 context (2020): covid_lost_job, kurzarbeit_hours, wfh_support_eur
- Year indicator: year

Important notes:
- Features vary by year; missing values are expected. Handle them via imputation or model-specific mechanisms.
- Avoid leakage: The target is current yearly salary; do not use prior-year salary fields.
- High-cardinality features (e.g., city, tech) and multilingual values require thoughtful encoding and normalization.

Evaluation:
- Metric: Root Mean Squared Logarithmic Error (RMSLE) on the salary target.
  - RMSLE = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
  - y_pred must be non-negative. Predictions are matched to test rows via row_id.

Submission format:
- CSV with two columns: row_id and salary
  - row_id: integer identifier matching the test.csv rows
  - salary: predicted current yearly brutto salary in EUR
  - Do not include any paths in the CSV and do not add extra columns.

Train/Test split:
- The split is deterministic and stratified by year and seniority to preserve distribution across time and seniority levels.
- All years (2018–2020) are included to maximize realism and task size.

Expectations:
- Participants should apply robust data processing, schema unification, multilingual normalization, and feature engineering before training models.
- Competitive solutions may use gradient boosting, regularized linear models, and encoders for high-cardinality categories; validation and careful metric handling are essential.
