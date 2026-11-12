# OpenMLE-fast task

Task ID: `20112018-salaries-for-san-francisco@1`

Native metric: `SFBenefitsRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3237 bytes)
- `data/sample_submission.csv` (1350182 bytes); columns: ["Id", "Benefits"]
- `data/test.csv` (2873544 bytes); columns: ["Id", "JobTitle", "BasePay", "OvertimePay", "OtherPay", "Year"]
- `data/train.csv` (13486027 bytes); columns: ["Id", "JobTitle", "BasePay", "OvertimePay", "OtherPay", "Year", "Benefits"]

## Public description

SF Public Benefits Cost Prediction (2011–2018)

Problem statement
- Given a San Francisco public employee-year record, predict the employer-paid Benefits (USD) for that record.
- You are provided job title (text) and cash compensation components for the year. Predict a single continuous target: Benefits.
- This is a challenging tabular regression problem with a high-cardinality text feature, temporal drift, and a heavy-tailed monetary target.

Files
- train.csv: Training data containing features and the target.
- test.csv: Test data containing the same feature columns plus Id (target withheld).
- sample_submission.csv: Sample file showing the required submission format.

Columns
- Id: Unique integer identifier for each row in train/test (test only for predictions; train also includes Id for consistency).
- JobTitle: Job title text (string). Expect thousands of unique values with a long tail.
- BasePay: Base salary component (float; may be zero or adjusted).
- OvertimePay: Overtime compensation (float; often zero; may include adjustments).
- OtherPay: Other cash compensation (float; may be zero or adjusted).
- Year: Year of the record (integer in [2011, 2018]).
- Benefits: Employer-paid benefits (float; target column present only in train.csv).

Important notes and leakage controls
- The provided train/test files exclude aggregate pay columns that are direct combinations of the target (e.g., TotalPay, TotalPayBenefits). These are intentionally removed to prevent trivial label leakage.
- Employee identifiers are not included as features to reduce memorization and encourage generalization.
- Train and test contain disjoint employees to emulate forecasting for new employees while preserving year coverage across both splits.

Submission format
- Submit a CSV with exactly two columns and header: Id, Benefits.
- Id must match the Id values in test.csv, one row per test example.
- Benefits must be valid finite numeric predictions (floats). Any non-numeric or missing values are invalid.

Evaluation
- Metric: Mean Absolute Error (MAE) on Benefits.
- For N test rows with ground truth yi and predictions pi, MAE = (1/N) * sum_i |pi − yi|.
- MAE is robust to outliers and directly measures dollar error, aligning with budgeting/planning use cases.

Modeling guidance
- Consider the long-tailed distribution of benefits. Many solutions benefit from modeling log1p(Benefits) and inverting at inference.
- JobTitle is highly informative but high-cardinality and noisy. Options include: bag-of-words or TF–IDF text features, target/frequency encoding with careful cross-validation, or pretrained text encoders.
- Year effects and interactions between pay components and seniority keywords (e.g., captain, chief, assistant, inspector, nurse, police, fire) can improve accuracy.
- Tree ensembles (e.g., Gradient Boosting/Random Forest) and regularized linear models are strong tabular baselines; neural models with text encoders can further improve performance.

Getting started
- Load train.csv, engineer features from JobTitle, and use BasePay/OvertimePay/OtherPay/Year as numeric inputs.
- Train a regression model and generate predictions for test.csv.
- Create a submission.csv with Id, Benefits and upload.
