# OpenMLE-fast task

Task ID: `shopping@1`

Native metric: `PublicPayrollBenefitsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2410 bytes)
- `data/sample_submission.csv` (609900 bytes); columns: ["Id", "Benefits"]
- `data/test.csv` (2131541 bytes); columns: ["Id", "Year", "JobTitle", "BasePay", "OvertimePay", "OtherPay", "Status"]
- `data/train.csv` (4566595 bytes); columns: ["Id", "Year", "JobTitle", "BasePay", "OvertimePay", "OtherPay", "Status", "Benefits"]

## Public description

Title: Public Payroll Benefits Prediction Challenge

Problem statement
You are given anonymized public-sector payroll records. For each employee-year record, predict the annual Benefits amount using job title and pay components. The goal is to build a model that estimates Benefits with low absolute error.

Data files
- train.csv: Training data with features and the target column Benefits.
- test.csv: Test data with the same features as train.csv, except Benefits is withheld.
- sample_submission.csv: Example submission showing the required format.

Input features
- Id: Unique record identifier.
- Year: Calendar year of the record.
- JobTitle: Employee job title (text).
- BasePay: Base salary/wage.
- OvertimePay: Overtime earnings.
- OtherPay: Other earnings (allowances, premiums, etc.).
- Status: Employment status (e.g., FT/PT). May be missing for some records.

Target
- Benefits: Annual benefits cost for the record (numeric, non-negative).

Important notes
- Do not engineer features from totals that trivially combine pay and benefits (e.g., TotalPay, TotalPayBenefits); these are excluded from the provided files to prevent leakage.
- Some fields may be missing or zero. Zeros are valid values; handle missingness appropriately.
- Text normalization/encoding of JobTitle is often helpful due to high cardinality and variants.
- The test set is temporally separated to introduce mild distribution shift across years.

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the ground truth Benefits values on the test set.
- Submission format: A CSV file with exactly two columns in this order:
  - Id: matching the Id values in test.csv
  - Benefits: your predicted numeric values

Scoring details
- Predictions must be finite numbers. Non-finite values (NaN/Inf) or missing Ids are invalid.
- MAE is computed after aligning rows by Id. Lower MAE is better.

Recommended approaches
- Robust preprocessing: numeric coercion, handling missing Status, and conservative text cleaning for JobTitle.
- Feature engineering: categorical encodings, interaction terms (e.g., BasePay × Status), and year-aware scaling.
- Modeling: tree-based ensembles (GBDT/Random Forest), regularized linear models, or tabular neural networks.

Deliverables
- Submit a CSV file named however you like, but following the sample_submission.csv structure. The leaderboard will reflect your MAE score.
