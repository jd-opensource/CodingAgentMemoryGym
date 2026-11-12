# OpenMLE-fast task

Task ID: `indian-company-dataset@1`

Native metric: `IndianCompanyRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (519 bytes)
- `data/sample_submission.csv` (20531 bytes); columns: ["id", "rating"]
- `data/test.csv` (97515 bytes); columns: ["id", "name", "review", "company_type", "Head_Quarters", "Company_Age", "No_of_Employee"]
- `data/train.csv` (403470 bytes); columns: ["id", "name", "review", "company_type", "Head_Quarters", "Company_Age", "No_of_Employee", "rating"]

## Public description

Competition: Predict Employer Rating from Company Attributes (Indian AmbitionBox dataset)

Public files:
- public/train.csv: Training data with features and target column 'rating'
- public/test.csv: Test data with the same features and an 'id' column (no 'rating')
- public/sample_submission.csv: Example submission with columns [id, rating]

Submission format:
- CSV with exactly two columns: [id, rating], matching ids from public/test.csv

Evaluation:
- Root Mean Squared Error (RMSE) computed on the 'rating' column
